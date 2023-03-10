from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api convert 相关 testcases")
class TestConvertApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_convert_001')
    @allure.description('根据id编号查询单笔交易')
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
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "根据id编号查询单笔交易错误，返回值是{}".format(r.text)

    @allure.title('test_convert_002')
    @allure.description('查询特定条件的交易')
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
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "获取产品列表错误，返回值是{}".format(r.text)

    @allure.title('test_convert_003')
    @allure.description('查询换汇交易限制')
    def test_convert_003(self):
        with allure.step("查询换汇交易限制"):
            r = session.request('GET', url='{}/txn/cfx/restriction'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['restrictions']['BRL'] == {"min": "50", "max": "1000000"}, "BRL换汇限制错误，接口返回值是{}".format(
                    r.json()['restrictions']['BRL'])
                assert r.json()['restrictions']['BTC'] == {"min": "0.0002", "max": "5"}, "BTC换汇限制错误，接口返回值是{}".format(
                    r.json()['restrictions']['BTC'])
                assert r.json()['restrictions']['CHF'] == {"min": "10", "max": "200000"}, "CHF换汇限制错误，接口返回值是{}".format(
                    r.json()['restrictions']['CHF'])
                assert r.json()['restrictions']['ETH'] == {"min": "0.002", "max": "100"}, "ETH换汇限制错误，接口返回值是{}".format(
                    r.json()['restrictions']['ETH'])
                assert r.json()['restrictions']['EUR'] == {"min": "10", "max": "200000"}, "EUR换汇限制错误，接口返回值是{}".format(
                    r.json()['restrictions']['EUR'])
                assert r.json()['restrictions']['USDT'] == {"min": "10", "max": "200000"}, "USDT换汇限制错误，接口返回值是{}".format(
                    r.json()['restrictions']['USDT'])
                assert r.json()['restrictions']['VND'] == {"min": "250000",
                                                           "max": "5000000000"}, "VND换汇限制错误，接口返回值是{}".format(
                    r.json()['restrictions']['VND'])
                assert r.json()['restrictions']['USD'] == {"min": "10", "max": "200000"}, "USDT换汇限制错误，接口返回值是{}".format(
                    r.json()['restrictions']['USD'])

    @allure.title('test_convert_004')
    @allure.description('换汇存在汇率差（手续费）')
    def test_convert_004(self):
        with allure.step("获取汇率对"):
            for i in ApiFunction.get_cfx_list():
                cryptos = i.split('-')
                r1 = session.request('GET',
                                     url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[0], cryptos[1])),
                                     headers=headers)
                logger.info('客户买入{},卖出{},我们给出的汇率是{}'.format(cryptos[0], cryptos[1], r1.json()['quote']))
                r2 = session.request('GET',
                                     url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[1], cryptos[0])),
                                     headers=headers)
                logger.info('客户买入{},卖出{},我们给出的汇率是{}'.format(cryptos[1], cryptos[0], r2.json()['quote']))
                assert Decimal(str(1 / float(r2.json()['quote']))) <= Decimal(r1.json()['quote']), "{}汇率对出现了问题".format(i)

    @allure.title('test_convert_005')
    @allure.description('超时换汇交易')
    def test_convert_005(self):
        headers['Accept-Language'] = 'zh-TW'
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
        assert r.json()['code'] == '106001', '超时换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r.text)

    @allure.title('test_convert_006')
    @allure.description('小于接受的最小值换汇交易')
    def test_convert_006(self):
        cfx_dict = ApiFunction.get_cfx_list()
        # 获取换汇值
        for i in cfx_dict:
            cryptos = i.split('-')
            with allure.step("major_ccy 是buy值，正兑换"):
                while 1 < 2:
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
                    if r.json()['code'] == '106013':
                        break
            with allure.step("major_ccy 是buy值，逆兑换 "):
                while 1 < 2:
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
                    r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                         headers=headers)
                    if r.json()['code'] == '106013':
                        break
            with allure.step("major_ccy 是sell值，正兑换 "):
                while 1 < 2:
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
                    r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data),
                                        headers=headers)
                    if r.json()['code'] == '106013':
                        break
            with allure.step("major_ccy 是sell值，逆兑换 "):
                while 1 < 2:
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
                    r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data), headers=headers)
                    if r.json()['code'] == '106013':
                        break

    @allure.title('test_convert_007')
    @allure.description('使用错误金额换汇交易')
    def test_convert_007(self):
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

    @allure.title('test_convert_008')
    @allure.description('获取换汇汇率对')
    def test_convert_008(self):
        r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'codes' in r.text, "选择的国家代码可以成功申请注册验证码失败，返回值是{}".format(r.text)

    @allure.title('test_convert_009')
    @allure.description('换汇交易')
    def test_convert_009(self):
        for i in ApiFunction.get_cfx_list():
            with allure.step("正向币种对，major_ccy 是buy值"):
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    transaction = ApiFunction.cfx_random(i, i.split('-')[0])
                    sleep(10)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                        transaction['data']['buy_amount']) == Decimal(
                        buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[0], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                        buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                        transaction['data']['sell_amount']) == Decimal(
                        sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[1], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                        sell_amount_wallet_balance_latest)
            with allure.step("正向币种对，major_ccy 是sell值"):
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    transaction = ApiFunction.cfx_random(i, i.split('-')[1])
                    sleep(10)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                        transaction['data']['buy_amount']) == Decimal(
                        buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[0], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                        buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                        transaction['data']['sell_amount']) == Decimal(
                        sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[1], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                        sell_amount_wallet_balance_latest)
            with allure.step("反向币种对，major_ccy 是buy值"):
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    transaction = ApiFunction.cfx_random('{}-{}'.format(i.split('-')[1], i.split('-')[0]),
                                                         i.split('-')[1])
                    sleep(10)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                        transaction['data']['buy_amount']) == Decimal(
                        buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[1], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                        buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                        transaction['data']['sell_amount']) == Decimal(
                        sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[0], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                        sell_amount_wallet_balance_latest)
            with allure.step("反向币种对，major_ccy 是sell值"):
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    transaction = ApiFunction.cfx_random('{}-{}'.format(i.split('-')[1], i.split('-')[0]),
                                                         i.split('-')[0])
                    sleep(10)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                        transaction['data']['buy_amount']) == Decimal(
                        buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[1], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                        buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                        transaction['data']['sell_amount']) == Decimal(
                        sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                        i.split('-')[0], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                        sell_amount_wallet_balance_latest)
