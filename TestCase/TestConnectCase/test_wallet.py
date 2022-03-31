from Function.api_function import *
from Function.operate_sql import *


# Connect相关cases
class TestWalletApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_wallet_001 获取账户可用余额列表(有资金）')
    def test_wallet_001(self):
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
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
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
                        assert float(mobile_balance) == float(
                            bybit_balance), '币种{}判断提供给bybit的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(
                            i, mobile_balance, bybit_balance)

    @allure.title('test_wallet_002 获取账户可用余额单币(有资金）')
    def test_wallet_002(self):
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
                    r = session.request('GET', url='{}/accounts/{}/balances/{}'.format(self.url, account_id, i),
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

    @allure.title('test_wallet_003 获取账户单币入账信息, 入币方式缺失，使用默认')
    def test_wallet_003(self):
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
                    r = session.request('GET', url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i, ''), headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    if i == 'GBP':
                        assert r.json()['method'] == 'Faster Payments', "账户可用余额列表错误，返回值是{}".format(r.text)
                    elif i == 'EUR':
                        assert r.json()['method'] == 'SEPA', "账户可用余额列表错误，返回值是{}".format(r.text)
                    elif i == 'CHF':
                        assert r.json()['method'] == 'SIC', "账户可用余额列表错误，返回值是{}".format(r.text)

    @allure.title('test_wallet_004 获取账户单币入账信息, 入币方式SEPA')
    def test_wallet_004(self):
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
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id,
                                                                                                  i, 'SEPA'),
                                        headers=connect_headers)
                if i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
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

    @allure.title('test_wallet_005 获取账户单币入账信息, 入币方式Faster Payments')
    def test_wallet_005(self):
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
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i, 'FPS'),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                if i == 'EUR':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式Faster Payments错误，返回值是{}".format(r.text)
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

    @allure.title('test_wallet_006 获取账户单币入账信息, 入币方式SIC')
    def test_wallet_006(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息"):
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_id, i, 'SIC'), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式SIC"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i, 'SIC'),
                                        headers=connect_headers)
                if i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                elif i == 'EUR':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                elif i == 'CHF':
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['meta'] is not None, "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                        bank_accounts = r.json()['meta']
                    with allure.step("moblie接口一致性查询"):
                        with allure.step("CHF法币充值账户"):
                            r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'CHF', 'SIC'),
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