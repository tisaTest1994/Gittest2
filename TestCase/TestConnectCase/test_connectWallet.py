from Function.api_function import *
from Function.operate_sql import *


# Connect相关cases
class TestConnectWalletApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.testcase('test_connect_wallet_001 获取账户可用余额列表(有资金）')
    def test_connect_wallet_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['balances'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
        with allure.step("判断提供给bybit的和我们自用的值一致"):
            balance_list = ApiFunction.balance_list()
            for i in balance_list:
                mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE',
                                                               wallet_type='BALANCE')
                for y in r.json()['balances']:
                    if y['code'] == i:
                        bybit_balance = y['balances']
                        assert float(mobile_balance) == float(bybit_balance), '币种{}判断提供给bybit的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(
                            i, mobile_balance, bybit_balance)

    @allure.testcase('test_connect_wallet_002 账户可用余额列表(无资金）')
    def test_connect_wallet_002(self):
        with allure.step("测试用户的account_id"):
            account_id = '3853a783-3a36-4713-b62a-c44960a9ed9d'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['balances'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
        with allure.step("匹配header"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc07@test.com',
                                                                                 password='A!234sdfg')
        with allure.step("判断提供给bybit的和我们自用的值一致"):
            balance_list = ApiFunction.balance_list()
            for i in balance_list:
                mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE',
                                                               wallet_type='BALANCE')
                for y in r.json()['balances']:
                    if y['code'] == i:
                        bybit_balance = y['balances']
                        assert float(mobile_balance) == float(bybit_balance), '币种{}判断提供给bybit的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(
                            i, mobile_balance, bybit_balance)

    @allure.testcase('test_connect_wallet_003 获取账户可用余额单币(有资金）')
    def test_connect_wallet_003(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得balance list"):
            balance_list = ApiFunction.balance_list()
        with allure.step("循环获取单币种"):
            for i in balance_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}'.format(account_id, i),
                                                        nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("账户可用余额列表"):
                    r = session.request('GET', url='{}/api/v1/accounts/{}/balances/{}'.format(self.url, account_id, i),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['balance'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
                with allure.step("通过mobile接口获取金额"):
                    mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE',
                                                                   wallet_type='BALANCE')
                with allure.step("获取的金额和通过mobile接口获取的金额对比"):
                    assert float(mobile_balance) == float(r.json()['balance'][
                        'balances']), '币种{}判断提供给bybit的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(
                        i, mobile_balance, r.json()['balance']['balances'])

    @allure.testcase('test_connect_wallet_004 获取账户可用余额单币(无资金）')
    def test_connect_wallet_004(self):
        with allure.step("测试用户的account_id"):
            account_id = '3853a783-3a36-4713-b62a-c44960a9ed9d'
        with allure.step("获得balance list"):
            balance_list = ApiFunction.balance_list()
        with allure.step("循环获取单币种"):
            for i in balance_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}'.format(account_id, i),
                                                        nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("账户可用余额列表"):
                    r = session.request('GET', url='{}/api/v1/accounts/{}/balances/{}'.format(self.url, account_id, i),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['balance'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
                with allure.step("匹配header"):
                    headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc07@test.com',
                                                                                         password='A!234sdfg')
                with allure.step("通过mobile接口获取金额"):
                    mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE',
                                                                   wallet_type='BALANCE')
                with allure.step("获取的金额和通过mobile接口获取的金额对比"):
                    assert float(mobile_balance) == float(r.json()['balance'][
                        'balances']), '币种{}判断提供给bybit的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(
                        i, mobile_balance, r.json()['balance']['balances'])

    @allure.testcase('test_connect_wallet_005 获取账户单币入账信息, 入币方式缺失，使用默认')
    def test_connect_wallet_005(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息"):
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                            account_id, i, ''), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式缺失，使用默认"):
                    r = session.request('GET',
                                        url='{}/api/v1/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id,
                                                                                                  i, ''),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    if i == 'GBP':
                        assert r.json()['method'] == 'FPS', "账户可用余额列表错误，返回值是{}".format(r.text)
                    elif i == 'EUR':
                        assert r.json()['method'] == 'SEPA', "账户可用余额列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_wallet_006 获取账户单币入账信息, 入币方式SEPA')
    def test_connect_wallet_006(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息"):
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                            account_id, i, 'SEPA'), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式SEPA"):
                    r = session.request('GET',
                                        url='{}/api/v1/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id,
                                                                                                  i, 'SEPA'),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                if i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == '500', "获取账户单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                elif i == 'EUR':
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['meta'] is not None, "获取账户单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                        bank_accounts = r.json()['meta']
                    with allure.step("moblie接口一致性查询"):
                        with allure.step("EUR法币充值账户"):
                            r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'EUR', 'SEPA'),
                                                headers=headers)
                            with allure.step("状态码和返回值"):
                                logger.info('状态码是{}'.format(str(r.status_code)))
                                logger.info('返回值是{}'.format(str(r.text)))
                            with allure.step("校验状态码"):
                                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                            with allure.step("校验返回值"):
                                assert r.json()['bank_accounts'] is not None, "EUR法币充值账户错误，返回值是{}".format(r.text)
                                bank_accounts_mobile = r.json()['bank_accounts'][0]
                                del bank_accounts_mobile['header']
                                assert bank_accounts_mobile == bank_accounts, "moblie接口一致性查询错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_wallet_007 获取账户单币入账信息, 入币方式Faster Payments')
    def test_connect_wallet_007(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息, 入币方式Faster Payments"):
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                            account_id, i, 'FPS'), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式Faster Payments"):
                    r = session.request('GET',
                                        url='{}/api/v1/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id,
                                                                                                  i, 'FPS'),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                if i == 'EUR':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == '500', "获取账户单币入账信息, 入币方式Faster Payments错误，返回值是{}".format(r.text)
                elif i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['meta'] is not None, "获取账户单币入账信息, 入币方式Faster Payments错误，返回值是{}".format(r.text)
                        bank_accounts = r.json()['meta']
                    with allure.step("moblie接口一致性查询"):
                        with allure.step("EUR法币充值账户"):
                            r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'GBP',
                                                                                              'Faster Payments'),
                                                headers=headers)
                            with allure.step("状态码和返回值"):
                                logger.info('状态码是{}'.format(str(r.status_code)))
                                logger.info('返回值是{}'.format(str(r.text)))
                            with allure.step("校验状态码"):
                                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                            with allure.step("校验返回值"):
                                assert r.json()['bank_accounts'] is not None, "EUR法币充值账户错误，返回值是{}".format(r.text)
                                bank_accounts_mobile = r.json()['bank_accounts'][0]
                                del bank_accounts_mobile['header']
                                assert bank_accounts_mobile == bank_accounts, "moblie接口一致性查询错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_wallet_008 账户转换货币')
    def test_connect_wallet_008(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
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
                                with allure.step("获得换汇前buy币种balance金额"):
                                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(
                                        type=cfx_amount['buy'])
                                with allure.step('获得换汇前sell币种balance金额'):
                                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(
                                        type=cfx_amount['sell'])
                                with allure.step("验签"):
                                    unix_time = int(time.time())
                                    nonce = generate_string(30)
                                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                                        url='/api/v1/accounts/{}/conversions'.format(
                                                                            account_id), nonce=nonce,
                                                                        body=json.dumps(data))
                                    connect_headers['ACCESS-SIGN'] = sign
                                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                    connect_headers['ACCESS-NONCE'] = nonce
                                with allure.step("账户可用余额列表"):
                                    r = session.request('POST', url='{}/api/v1/accounts/{}/conversions'.format(self.url,
                                                                                                               account_id),
                                                        data=json.dumps(data), headers=connect_headers)
                                with allure.step("校验状态码"):
                                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                                with allure.step("校验返回值"):
                                    assert r.json()['transaction_id'] is not None, "换汇错误，返回值是{}".format(r.text)
                                    assert r.json()['status'] == 'Success', "换汇错误，返回值是{}".format(r.text)
                                sleep(10)
                                with allure.step("获得换汇后buy币种balance金额"):
                                    buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(
                                        type=cfx_amount['buy'])
                                with allure.step("获得换汇后sell币种balance金额"):
                                    sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(
                                        type=cfx_amount['sell'])
                                logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cfx_amount['buy'],
                                                                                              buy_amount_wallet_balance_old,
                                                                                              cfx_amount['buy_amount'],
                                                                                              buy_amount_wallet_balance_latest))
                                logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cfx_amount['sell'],
                                                                                                sell_amount_wallet_balance_old,
                                                                                                cfx_amount[
                                                                                                    'sell_amount'],
                                                                                                sell_amount_wallet_balance_latest))
                                assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                                    cfx_amount['buy_amount']) == Decimal(
                                    buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                                    cfx_amount['buy'], buy_amount_wallet_balance_old, cfx_amount['buy_amount'],
                                    buy_amount_wallet_balance_latest)
                                assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                                    cfx_amount['sell_amount']) == Decimal(
                                    sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                                    cfx_amount['sell'], sell_amount_wallet_balance_old, cfx_amount['sell_amount'],
                                    sell_amount_wallet_balance_latest)
                    else:
                        with allure.step("生成货币对"):
                            pair_list = i.split('-')
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
                                with allure.step("获得换汇前buy币种balance金额"):
                                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(
                                        type=cfx_amount['buy'])
                                with allure.step('获得换汇前sell币种balance金额'):
                                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(
                                        type=cfx_amount['sell'])
                                with allure.step("验签"):
                                    unix_time = int(time.time())
                                    nonce = generate_string(30)
                                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                                        url='/api/v1/accounts/{}/conversions'.format(
                                                                            account_id), nonce=nonce,
                                                                        body=json.dumps(data))
                                    connect_headers['ACCESS-SIGN'] = sign
                                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                    connect_headers['ACCESS-NONCE'] = nonce
                                with allure.step("账户可用余额列表"):
                                    r = session.request('POST', url='{}/api/v1/accounts/{}/conversions'.format(self.url,
                                                                                                               account_id),
                                                        data=json.dumps(data), headers=connect_headers)
                                with allure.step("校验状态码"):
                                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                                with allure.step("校验返回值"):
                                    assert r.json()['transaction_id'] is not None, "换汇错误，返回值是{}".format(r.text)
                                    assert r.json()['status'] == 'Success', "换汇错误，返回值是{}".format(r.text)
                                sleep(10)
                                with allure.step("获得换汇后buy币种balance金额"):
                                    buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(
                                        type=cfx_amount['buy'])
                                with allure.step("获得换汇后sell币种balance金额"):
                                    sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(
                                        type=cfx_amount['sell'])
                                logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cfx_amount['buy'],
                                                                                              buy_amount_wallet_balance_old,
                                                                                              cfx_amount['buy_amount'],
                                                                                              buy_amount_wallet_balance_latest))
                                logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cfx_amount['sell'],
                                                                                                sell_amount_wallet_balance_old,
                                                                                                cfx_amount[
                                                                                                    'sell_amount'],
                                                                                                sell_amount_wallet_balance_latest))
                                assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                                    cfx_amount['buy_amount']) == Decimal(
                                    buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                                    cfx_amount['buy'], buy_amount_wallet_balance_old, cfx_amount['buy_amount'],
                                    buy_amount_wallet_balance_latest)
                                assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                                    cfx_amount['sell_amount']) == Decimal(
                                    sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                                    cfx_amount['sell'], sell_amount_wallet_balance_old, cfx_amount['sell_amount'],
                                    sell_amount_wallet_balance_latest)

    @allure.testcase('test_convert_009 账户划转列表')
    def test_convert_009(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cbb4568f-ee69-4701-83d4-a6975a852c58'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/transfers'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['pagination_response'] is not None, "账户划转列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_convert_010 账户划转详情')
    def test_convert_010(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/transfers/{}'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/transfers'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['pagination_response'] is not None, "账户划转列表错误，返回值是{}".format(r.text)