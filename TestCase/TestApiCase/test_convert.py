from Function.api_function import *
from Function.operate_sql import *


# convert相关cases
class TestConvertApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.testcase('test_convert_001 根据id编号查询单笔交易')
    def test_convert_001(self):
        with allure.step("获得交易transaction_id"):
            transaction_id = ApiFunction.get_payout_transaction_id()
            logger.info('transaction_id 是{}'.format(transaction_id))
        with allure.step("查询单笔交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                "txn_sub_type": 6
            }
            r = session.request('GET', url='{}/txn/{}'.format(env_url, transaction_id), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "根据id编号查询单笔交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_convert_002 查询特定条件的交易')
    def test_convert_002(self):
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 100
            },
            "user_txn_sub_types": [1, 2, 3, 4, 5, 6],
            "statuses": [1, 2, 3, 4],
            "codes": ["ETH"]
        }
        with allure.step("查询特定条件的交易"):
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "获取产品列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_convert_003 查询换汇交易限制')
    def test_convert_003(self):
        with allure.step("查询换汇交易限制"):
            r = session.request('GET', url='{}/txn/cfx/restriction'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '"BTC":{"min":"0.0002"' in r.text, "获取产品列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_convert_004 换汇存在汇率差（手续费）')
    def test_convert_004(self):
        with allure.step("获取汇率对"):
            cfx_dict = get_json()['cfx_book']
        for i in cfx_dict.values():
            cryptos = i.split('-')
            r1 = session.request('GET',
                                 url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[0], cryptos[1])),
                                 headers=headers)
            logger.info('客户买入{},卖出{},我们给出的汇率是{}'.format(cryptos[0], cryptos[1], r1.json()['quote']))
            r2 = session.request('GET',
                                 url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[1], cryptos[0])),
                                 headers=headers)
            logger.info('客户买入{},卖出{},我们给出的汇率是{}'.format(cryptos[1], cryptos[0], r2.json()['quote']))
            print(float(str(1 / float(r2.json()['quote']))[:len(str(r1.json()['quote']))]), float(r1.json()['quote']))
            assert float(str(1 / float(r2.json()['quote']))[:len(str(r1.json()['quote']))]) <= float(
                r1.json()['quote']), "{}汇率对出现了问题".format(i)

    @allure.testcase('test_convert_005 超时换汇交易')
    def test_convert_005(self):
        quote = ApiFunction.get_quote('BTC-USDT')
        sell_amount = str(float(0.01) * float(quote['quote']))
        sleep(30)
        data = {
            "quote_id": quote['quote_id'],
            "quote": quote['quote'],
            "pair": 'BTC-USDT',
            "buy_amount": '0.01',
            "sell_amount": str(sell_amount),
            "major_ccy": 'BTC'
        }
        r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data), headers=headers)
        logger.info('申请换汇参数{}'.format(data))
        logger.info('超时换汇交易返回值是{}'.format(r.text))
        assert 'Price expired. Please retry your convert' in r.text, '超时换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r.text)

    @allure.testcase('test_convert_006 小于接受的最小值换汇交易')
    def test_convert_006(self):
        with allure.step("获取汇率对"):
            cfx_dict = get_json()['cfx_book']
            # 获取换汇值
            for i in cfx_dict.values():
                cryptos = i.split('-')
                with allure.step("major_ccy 是buy值，正兑换"):
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        buy_amount = random.uniform(0.0001, 0.00019)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        buy_amount = random.uniform(1, 9)
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        buy_amount = random.uniform(1, 9)
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    quote = ApiFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
                    sell_amount = str(float(buy_amount) * float(quote['quote']))
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        if len(str(sell_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[0], cryptos[1]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[0]
                    }
                    r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                        headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    assert 'invalid Amount' in r.text, '小于接受的最小值换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r.text)
                with allure.step("major_ccy 是buy值，逆兑换 "):
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        buy_amount = random.uniform(0.0001, 0.00019)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        buy_amount = random.uniform(1, 9)
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        buy_amount = random.uniform(1, 9)
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    quote = ApiFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
                    sell_amount = str(float(buy_amount) * float(quote['quote']))
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        if len(str(sell_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[1], cryptos[0]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[1]
                    }
                    r1 = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                         headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    assert 'invalid Amount' in r1.text, '小于接受的最小值换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r1.text)
                with allure.step("major_ccy 是sell值，正兑换 "):
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        sell_amount = random.uniform(0.0001, 0.00019)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        sell_amount = random.uniform(1, 9)
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        sell_amount = random.uniform(1, 9)
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:2])
                    quote = ApiFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
                    buy_amount = str(float(sell_amount) / float(quote['quote']))
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[0], cryptos[1]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[1]
                    }
                    r2 = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                         headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    assert 'invalid Amount' in r2.text, '小于接受的最小值换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r2.text)
                with allure.step("major_ccy 是sell值，逆兑换 "):
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        sell_amount = random.uniform(0.0001, 0.00019)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        sell_amount = random.uniform(1, 9)
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        sell_amount = random.uniform(1, 9)
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:2])
                    quote = ApiFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
                    buy_amount = str(float(sell_amount) / float(quote['quote']))
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        if len(str(sell_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[1], cryptos[0]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[0]
                    }
                    r3 = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                         headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    assert 'invalid Amount' in r3.text, '小于接受的最小值换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r3.text)

    @allure.testcase('test_convert_007 使用错误金额换汇交易')
    def test_convert_0087(self):
        quote = ApiFunction.get_quote('BTC-USDT')
        data = {
            "quote_id": quote['quote_id'],
            "quote": quote['quote'],
            "pair": 'BTC-USDT',
            "buy_amount": '0.01',
            "sell_amount": "11",
            "major_ccy": 'BTC'
        }
        r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data), headers=headers)
        logger.info('申请换汇参数{}'.format(data))
        assert 'amount calculation error' in r.text, '使用错误金额换汇交易错误,返回值是{}'.format(r.text)

    @allure.testcase('test_convert_008 获取换汇汇率对')
    def test_convert_008(self):
        r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'codes' in r.text, "选择的国家代码可以成功申请注册验证码失败，返回值是{}".format(r.text)

    @allure.testcase('test_convert_009 换汇交易')
    def test_convert_009(self):
        with allure.step("获取汇率对"):
            cfx_book = get_json()['cfx_book']
            for i in cfx_book.values():
                pair_dict = ApiFunction.cfx_hedging_pairs(pair=i)
                with allure.step("判断是否是直盘"):
                    if len(pair_dict.keys()) == 1:
                        with allure.step("生成货币对"):
                            pair = list(pair_dict.values())
                            pair_list = pair[0].split('-')
                            cfx_dict = [{'buy': pair_list[0], 'sell': pair_list[1], 'major_ccy': pair_list[0]},
                                        {'buy': pair_list[0], 'sell': pair_list[1], 'major_ccy': pair_list[1]},
                                        {'buy': pair_list[1], 'sell': pair_list[0], 'major_ccy': pair_list[1]},
                                        {'buy': pair_list[1], 'sell': pair_list[0], 'major_ccy': pair_list[0]}]
                            for y in cfx_dict:
                                cfx_amount = ApiFunction.cfx_random_number(y)
                                data = {
                                    "quote_id": cfx_amount['quote']['quote_id'],
                                    "quote": cfx_amount['quote']['quote'],
                                    "pair": '{}-{}'.format(cfx_amount['buy'], cfx_amount['sell']),
                                    "buy_amount": str(cfx_amount['buy_amount']),
                                    "sell_amount": str(cfx_amount['sell_amount']),
                                    "major_ccy": cfx_amount['major_ccy']
                                }
                                logger.info('发送换汇data是{}'.format(data))
                                r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                                    headers=headers)
                                logger.info('申请换汇参数{}'.format(data))
                                logger.info('换汇返回值{}'.format(r.text))
                                sleep(20)
                                with allure.step("校验状态码"):
                                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                                with allure.step("校验返回值"):
                                    assert r.json()['transaction']['transaction_id'] is not None, "获取产品列表错误，返回值是{}".format(r.text)
