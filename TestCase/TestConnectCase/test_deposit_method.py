from Function.api_function import *
from Function.operate_sql import *


# 账户操作相关--账户入币信息
class TestDepositMethodApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_deposit_method_001')
    @allure.description('账户操作相关-获取账户单币入账信息, 入币方式缺失，使用默认')
    def test_deposit_method_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("从metadata接口获取已开启的币种信息"):
            fiat_metadata = session.request('GET', url='{}/core/metadata'.format(env_url), headers=headers)
            fiat_list_metadata = fiat_metadata.json()['currencies']
            fiat_all_metadata = fiat_list_metadata.keys()
        with allure.step("如在metada中关闭，则去除"):
            for i in range(0, len(cash_list)):
                if cash_list[i] not in fiat_all_metadata:
                    cash_list.remove(cash_list[i])
        with allure.step("获取账户单币入账信息"):
            for i in cash_list:
                if i != 'BRL':
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
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(self.url, account_id, i, ''), headers=connect_headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "当前币种为{}，http状态码不对，目前状态码是{}".format(i, r.status_code)
                    with allure.step("校验返回值"):
                        if i == 'GBP':
                            assert r.json()['method'] == 'Faster Payments', "币种{}的入币信息错误，返回值是{}".format(i, r.text)
                        elif i == 'EUR':
                            assert r.json()['method'] == 'SEPA', "币种{}的入币信息错误，返回值是{}".format(i, r.text)
                        elif i == 'CHF':
                            assert r.json()['method'] == 'SIC', "币种{}的入币信息错误，返回值是{}".format(i, r.text)

    @allure.title('test_deposit_method_002')
    @allure.description('账户操作相关--获取账户单币入账信息，入币方式SEPA')
    # 和mobile接口一致性检查不通过
    def test_deposit_method_002(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息, 入币方式SEPA"):
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
                with allure.step("获取账户单币入账信息, 入币方式Faster Payments"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i,
                                                                                           'SEPA'),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                if i == 'BRL':
                    break
                elif i == 'CHF':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA019', "获取账户单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                elif i == 'EUR':
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['meta'] is not None, "获取账户单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                elif i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA019', "获取账户单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                        # bank_accounts = r.json()['meta']
                    # with allure.step("moblie接口一致性查询"):
                    #     with allure.step("EUR法币充值账户"):
                    #         r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'GBP',
                    #                                                                           'Faster Payments'),
                    #                             headers=headers)
                    #         with allure.step("状态码和返回值"):
                    #             logger.info('状态码是{}'.format(str(r.status_code)))
                    #             logger.info('返回值是{}'.format(str(r.text)))
                    #         with allure.step("校验状态码"):
                    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    #         with allure.step("校验返回值"):
                    #             assert r.json()['bank_accounts'] is not None, "EUR法币充值账户错误，返回值是{}".format(r.text)
                    #             bank_accounts_mobile = r.json()['bank_accounts'][0]
                    #             del bank_accounts_mobile['header']
                    #             assert bank_accounts_mobile == bank_accounts, "moblie接口一致性查询错误，返回值是{}".format(r.text)

    @allure.title('test_deposit_method_003')
    @allure.description('账户操作相关--获取账户单币入账信息，入币方式Faster Payments')
    # 和mobile接口一致性检查不通过
    def test_deposit_method_003(self):
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
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i,
                                                                                           'FPS'),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                if i == 'BRL':
                    break
                elif i == 'CHF':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA019', "获取账户单币入账信息, 入币方式Faster Payments错误，返回值是{}".format(r.text)
                elif i == 'EUR':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA019', "获取账户单币入账信息, 入币方式Faster Payments错误，返回值是{}".format(r.text)
                elif i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['meta'] is not None, "获取账户单币入账信息, 入币方式Faster Payments错误，返回值是{}".format(r.text)
                        # bank_accounts = r.json()['meta']
                    # with allure.step("moblie接口一致性查询"):
                    #     with allure.step("EUR法币充值账户"):
                    #         r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'GBP',
                    #                                                                           'Faster Payments'),
                    #                             headers=headers)
                    #         with allure.step("状态码和返回值"):
                    #             logger.info('状态码是{}'.format(str(r.status_code)))
                    #             logger.info('返回值是{}'.format(str(r.text)))
                    #         with allure.step("校验状态码"):
                    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    #         with allure.step("校验返回值"):
                    #             assert r.json()['bank_accounts'] is not None, "EUR法币充值账户错误，返回值是{}".format(r.text)
                    #             bank_accounts_mobile = r.json()['bank_accounts'][0]
                    #             del bank_accounts_mobile['header']
                    #             assert bank_accounts_mobile == bank_accounts, "moblie接口一致性查询错误，返回值是{}".format(r.text)

    @allure.title('test_deposit_method_004')
    @allure.description('账户操作相关--获取账户单币入账信息，入币方式SIC')
    # 和mobile接口一致性检查不通过
    def test_deposit_method_004(self):
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
                                                            account_id, i, 'SIC'), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式SIC"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.
                                        format(self.url, account_id, i, 'SIC'), headers=connect_headers)
                if i == 'BRL':
                    break
                elif i == 'CHF':
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['meta'] is not None, "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                elif i == 'EUR':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA019', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                elif i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA019', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                        # bank_accounts = r.json()['meta']
                    # with allure.step("moblie接口一致性查询"):
                    #     with allure.step("CHF法币充值账户"):
                    #         r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'CHF', 'SIC'),
                    #                             headers=headers)
                    #         with allure.step("状态码和返回值"):
                    #             logger.info('状态码是{}'.format(str(r.status_code)))
                    #             logger.info('返回值是{}'.format(str(r.text)))
                    #         with allure.step("校验状态码"):
                    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    #         with allure.step("校验返回值"):
                    #             assert r.json()['bank_accounts'] is not None, "EUR法币充值账户错误，返回值是{}".format(r.text)
                    #             bank_accounts_mobile = r.json()['bank_accounts'][0]
                    #             del bank_accounts_mobile['header']
                    #             assert bank_accounts_mobile == bank_accounts, "moblie接口一致性查询错误，返回值是{}".format(r.text)
