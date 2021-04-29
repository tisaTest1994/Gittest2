from Function.api_function import *
from run import *
from Function.log import *
import allure
from decimal import *
from time import sleep


# convert相关cases
class TestConvertApi:

    @allure.testcase('test_convert_001 根据id编号查询单笔交易')
    def test_convert_001(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获得交易transaction_id"):
            transaction_id = AccountFunction.get_payout_transaction_id()
            logger.info('transaction_id 是{}'.format(transaction_id))
        with allure.step("查询单笔交易"):
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
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
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
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询换汇交易限制"):
            r = session.request('GET', url='{}/txn/cfx/restriction'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '{"restrictions":{"BTC":{"min":"0.0002","max":"-1"},"ETH":{"min":"0.006","max":"-1"},"EUR":{"min":"10","max":"-1"},"GBP":{"min":"10","max":"-1"},"USDT":{"min":"10","max":"-1"}}}' in r.text, "获取产品列表错误，返回值是{}".format(
                    r.text)

    @allure.testcase('test_convert_004 换汇存在汇率差（手续费）')
    def test_convert_004(self):
        List = ['BTC-ETH', 'BTC-USDT', 'BTC-GBP', 'BTC-EUR', 'ETH-USDT', 'ETH-GBP', 'ETH-EUR', 'USDT-GBP',
                'USDT-EUR']
        for i in List:
            cryptos = i.split('-')
            r1 = session.request('GET',
                                  url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[0], cryptos[1])),
                                  headers=headers)
            logger.info('客户买入{},卖出{},我们给出的汇率是{}'.format(cryptos[0], cryptos[1], r1.json()['quote']))
            r2 = session.request('GET',
                                  url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[1], cryptos[0])),
                                  headers=headers)
            logger.info('客户买入{},卖出{},我们给出的汇率是{}'.format(cryptos[1], cryptos[0], str(1 / float(r2.json()['quote']))[
                                                                                :len(str(r1.json()['quote']))]))
            assert float(str(1 / float(r2.json()['quote']))[:len(str(r1.json()['quote']))]) <= float(
                r1.json()['quote']), "{}汇率对出现了问题".format(i)

    @allure.testcase('test_convert_05 换汇交易')
    def test_convert_05(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("换汇交易"):
            List = ['BTC-ETH', 'BTC-USDT', 'BTC-EUR', 'ETH-USDT', 'ETH-EUR', 'USDT-EUR']
            # 获取换汇值
            for i in List:
                cryptos = i.split('-')
                with allure.step("major_ccy 是buy值，正兑换"):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = AccountFunction.get_crypto_number(account=email['email'],
                                                                                      password=email['password'],
                                                                                      crypto_type=cryptos[0])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = AccountFunction.get_crypto_number(account=email['email'],
                                                                                       password=email['password'],
                                                                                       crypto_type=cryptos[1])
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        buy_amount = random.uniform(0.01, 0.19)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        buy_amount = random.uniform(10, 30.10)
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        buy_amount = random.uniform(10, 30.10)
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
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
                                                         str(sell_amount).split('.')[1][:2])
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
                    assert "'status': 5," not in r.text, '换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r.text)
                    sleep(5)
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        buy_amount_wallet_balance_latest = AccountFunction.get_crypto_number(account=email['email'], password=email['password'], crypto_type=cryptos[0])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = AccountFunction.get_crypto_number(account=email['email'], password=email['password'], crypto_type=cryptos[1])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                               buy_amount_wallet_balance,
                                                                                               buy_amount,
                                                                                               buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                                 sell_amount_wallet_balance,
                                                                                                 sell_amount,
                                                                                                 sell_amount_wallet_balance_latest))
                    assert Decimal(buy_amount_wallet_balance) + Decimal(buy_amount) == Decimal(buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[0], buy_amount_wallet_balance, buy_amount, buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance) - Decimal(sell_amount) == Decimal(sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[1], sell_amount_wallet_balance, sell_amount, sell_amount_wallet_balance_latest)
                with allure.step("major_ccy 是buy值，逆兑换 "):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = AccountFunction.get_crypto_number(account=email['email'],
                                                                                      password=email['password'],
                                                                                      crypto_type=cryptos[1])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = AccountFunction.get_crypto_number(account=email['email'],
                                                                                       password=email['password'],
                                                                                       crypto_type=cryptos[0])
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        buy_amount = random.uniform(0.01, 0.19)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        buy_amount = random.uniform(10, 30.10)
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:6])
                    else:
                        buy_amount = random.uniform(10, 30.10)
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
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
                                                         str(sell_amount).split('.')[1][:2])
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
                    assert "'status': 5," not in r1.text, '换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r1.text)
                    sleep(5)
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        buy_amount_wallet_balance_latest = AccountFunction.get_crypto_number(account=email['email'], password=email['password'], crypto_type=cryptos[1])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = AccountFunction.get_crypto_number(account=email['email'], password=email['password'], crypto_type=cryptos[0])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                               buy_amount_wallet_balance,
                                                                                               buy_amount,
                                                                                               buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                                 sell_amount_wallet_balance,
                                                                                                 sell_amount,
                                                                                                 sell_amount_wallet_balance_latest))
                    assert Decimal(buy_amount_wallet_balance) + Decimal(buy_amount) == Decimal(buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[1], buy_amount_wallet_balance, buy_amount, buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance) - Decimal(sell_amount) == Decimal(sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[0], sell_amount_wallet_balance, sell_amount, sell_amount_wallet_balance_latest)
                with allure.step("major_ccy 是sell值，正兑换 "):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = AccountFunction.get_crypto_number(account=email['email'],
                                                                                      password=email['password'],
                                                                                      crypto_type=cryptos[0])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = AccountFunction.get_crypto_number(account=email['email'],
                                                                                       password=email['password'],
                                                                                       crypto_type=cryptos[1])
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        sell_amount = random.uniform(0.01, 0.19)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        sell_amount = random.uniform(10, 30.10)
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        sell_amount = random.uniform(10, 30.10)
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:2])
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
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
                                                        str(buy_amount).split('.')[1][:2])
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
                    assert "'status': 5," not in r2.text, '换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r2.text)
                    sleep(5)
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        buy_amount_wallet_balance_latest = AccountFunction.get_crypto_number(account=email['email'], password=email['password'], crypto_type=cryptos[0])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = AccountFunction.get_crypto_number(account=email['email'], password=email['password'], crypto_type=cryptos[1])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                               buy_amount_wallet_balance,
                                                                                               buy_amount,
                                                                                               buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                                 sell_amount_wallet_balance,
                                                                                                 sell_amount,
                                                                                                 sell_amount_wallet_balance_latest))
                    assert Decimal(buy_amount_wallet_balance) + Decimal(buy_amount) == Decimal(buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[0], buy_amount_wallet_balance, buy_amount, buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance) - Decimal(sell_amount) == Decimal(sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[1], sell_amount_wallet_balance, sell_amount, sell_amount_wallet_balance_latest)
                with allure.step("major_ccy 是sell值，逆兑换"):
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        buy_amount_wallet_balance = AccountFunction.get_crypto_number(account=email['email'],
                                                                                      password=email['password'],
                                                                                      crypto_type=cryptos[1])
                    with allure.step('获取没换汇前buy货币钱包中可用数量'):
                        sell_amount_wallet_balance = AccountFunction.get_crypto_number(account=email['email'],
                                                                                       password=email['password'],
                                                                                       crypto_type=cryptos[0])
                    if cryptos[0] == 'BTC' or cryptos[0] == 'ETH':
                        sell_amount = random.uniform(0.01, 0.19)
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:8])
                    elif cryptos[0] == 'USDT':
                        sell_amount = random.uniform(10, 30.10)
                        if len(str(sell_amount).split('.')[1]) >= 6:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:6])
                    else:
                        sell_amount = random.uniform(10, 30.10)
                        if len(str(sell_amount).split('.')[1]) >= 2:
                            sell_amount = '{}.{}'.format(str(sell_amount).split('.')[0],
                                                         str(sell_amount).split('.')[1][:2])
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
                    buy_amount = str(float(sell_amount) / float(quote['quote']))
                    if cryptos[1] == 'BTC' or cryptos[1] == 'ETH':
                        if len(str(buy_amount).split('.')[1]) >= 8:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                         str(buy_amount).split('.')[1][:8])
                    elif cryptos[1] == 'USDT':
                        if len(str(buy_amount).split('.')[1]) >= 6:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                         str(buy_amount).split('.')[1][:6])
                    else:
                        if len(str(buy_amount).split('.')[1]) >= 2:
                            buy_amount = '{}.{}'.format(str(buy_amount).split('.')[0],
                                                        str(buy_amount).split('.')[1][:2])
                    data = {
                        "quote_id": quote['quote_id'],
                        "quote": quote['quote'],
                        "pair": '{}-{}'.format(cryptos[1], cryptos[0]),
                        "buy_amount": str(buy_amount),
                        "sell_amount": str(sell_amount),
                        "major_ccy": cryptos[0]
                    }
                    r3 = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data), headers=headers)
                    logger.info('申请换汇参数{}'.format(data))
                    assert "'status': 5," not in r3.text, '换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r3.text)
                    sleep(5)
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        buy_amount_wallet_balance_latest = AccountFunction.get_crypto_number(account=email['email'], password=email['password'], crypto_type=cryptos[1])
                    with allure.step('获取没换汇后buy货币钱包中可用数量'):
                        sell_amount_wallet_balance_latest = AccountFunction.get_crypto_number(account=email['email'], password=email['password'], crypto_type=cryptos[0])
                    logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[1],
                                                                                               buy_amount_wallet_balance,
                                                                                               buy_amount,
                                                                                               buy_amount_wallet_balance_latest))
                    logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[0],
                                                                                                 sell_amount_wallet_balance,
                                                                                                 sell_amount,
                                                                                                 sell_amount_wallet_balance_latest))
                    assert Decimal(buy_amount_wallet_balance) + Decimal(buy_amount) == Decimal(buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cryptos[1], buy_amount_wallet_balance, buy_amount, buy_amount_wallet_balance_latest)
                    assert Decimal(sell_amount_wallet_balance) - Decimal(sell_amount) == Decimal(sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cryptos[0], sell_amount_wallet_balance, sell_amount, sell_amount_wallet_balance_latest)

    @allure.testcase('test_convert_06 超时换汇交易')
    def test_convert_06(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            quote = AccountFunction.get_quote('BTC-USDT')
            sell_amount = str(float(0.01) * float(quote['quote']))
            data = {
                "quote_id": quote['quote_id'],
                "quote": quote['quote'],
                "pair": 'BTC-USDT',
                "buy_amount": '0.01',
                "sell_amount": str(sell_amount),
                "major_ccy": 'BTC'
            }
            sleep(20)
            r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data), headers=headers)
            logger.info('申请换汇参数{}'.format(data))
            logger.info('超时换汇交易返回值是{}'.format(r.text))
            assert 'CFXTXN000012:invalid Rate' in r.text, '超时换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r.text)

    @allure.testcase('test_convert_07 小于接受的最小值换汇交易')
    def test_convert_07(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("换汇交易"):
            List = ['BTC-ETH', 'BTC-USDT', 'BTC-GBP', 'BTC-EUR', 'ETH-USDT', 'ETH-GBP', 'ETH-EUR', 'USDT-GBP',
                    'USDT-EUR']
            # 获取换汇值
            for i in List:
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
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
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
                    assert 'CFXTXN000013' in r.text, '小于接受的最小值换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r.text)
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
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
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
                    assert 'CFXTXN000013' in r1.text, '小于接受的最小值换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r1.text)
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
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[0], cryptos[1]))
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
                    assert 'CFXTXN000013' in r2.text, '小于接受的最小值换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r2.text)
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
                    quote = AccountFunction.get_quote('{}-{}'.format(cryptos[1], cryptos[0]))
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
                    assert 'CFXTXN000013' in r3.text, '小于接受的最小值换汇交易错误，申请参数是{}. 返回结果是{}'.format(data, r3.text)

    @allure.testcase('test_convert_08 使用错误金额换汇交易')
    def test_convert_08(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            quote = AccountFunction.get_quote('BTC-USDT')
            data = {
                "quote_id": quote['quote_id'],
                "quote": quote['quote'],
                "pair": 'BTC-USDT',
                "buy_amount": '0.01',
                "sell_amount": "11",
                "major_ccy": 'BTC'
            }
            r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data), headers=headers)
            print(r.text)
            logger.info('申请换汇参数{}'.format(data))