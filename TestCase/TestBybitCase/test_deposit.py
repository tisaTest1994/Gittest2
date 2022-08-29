from Function.api_function import *
from Function.operate_sql import *


# 账户操作相关--账户入币信息
class TestDepositApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup(self):
        ApiFunction.add_headers()

    @allure.title('test_deposit_001')
    @allure.description('账户操作相关-获取账户单币入账信息, 入币方式缺失，使用默认')
    def test_deposit_001(self):
        with allure.step("测试用户的account_id"):
            account_id_list = ['cd7e353b-6f4c-45db-bdd5-78bdc13a53c7', 'c328af6a-c523-4032-9181-0596c7db6db7', 'bacf2b3e-6599-44f4-adf6-c4c13ff40946']
        for account_id in account_id_list:
            with allure.step("获得法币list"):
                cash_list = ApiFunction.get_config_info(type='cash')
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
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(30)
                        sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                            url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                                account_id, i, ''), nonce=nonce)
                        connect_header['ACCESS-SIGN'] = sign
                        connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_header['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币入账信息, 入币方式缺失，使用默认"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(self.url, account_id, i, ''), headers=connect_header)
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

    @allure.title('test_deposit_002')
    @allure.description('账户操作相关--获取账户单币入账信息，入币方式SEPA')
    def test_deposit_002(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7'
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
                    connect_header['ACCESS-SIGN'] = sign
                    connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_header['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式Faster Payments"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i,
                                                                                           'SEPA'),
                                        headers=connect_header)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                if i == 'BRL':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA019', "获取账户BRL单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                elif i == 'CHF':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA014', "获取账户CHF单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                elif i == 'EUR':
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['meta'] is not None, "获取账户EUR单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                elif i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA014', "获取账户GBP单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                elif i == 'VND':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == 'PA050', "获取账户VND单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                        assert r.json()['message'] == 'This currency only supports ATM card deposit method on Cabital.', "获取账户VND单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)

    @allure.title('test_deposit_003')
    @allure.description('账户操作相关--获取账户单币入账信息，权限校验')
    def test_deposit_003(self):
        with allure.step("测试用户的account_id"):
            account_id_list = ['cd7e353b-6f4c-45db-bdd5-78bdc13a53c7', 'c328af6a-c523-4032-9181-0596c7db6db7',
                               'bacf2b3e-6599-44f4-adf6-c4c13ff40946']
        for account_id in account_id_list:
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
                        connect_header['ACCESS-SIGN'] = sign
                        connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_header['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币入账信息, 入币方式Faster Payments"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i,
                                                                                               'FPS'),
                                            headers=connect_header)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    if i == 'BRL':
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA019', "获取账户单币入账信息, BRL入币方式Faster Payments错误，返回值是{}".format(r.text)
                    elif i == 'CHF':
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA014', "获取账户单币入账信息, CHF入币方式Faster Payments错误，返回值是{}".format(r.text)
                    elif i == 'EUR':
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA014', "获取账户单币入账信息, EUR入币方式Faster Payments错误，返回值是{}".format(r.text)
                    elif i == 'GBP':
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['meta'] is not None, "获取账户单币入账信息, GBP入币方式Faster Payments错误，返回值是{}".format(r.text)

    @allure.title('test_deposit_004')
    @allure.description('账户操作相关--获取账户单币入账信息，入币方式SIC校验')
    def test_deposit_004(self):
        with allure.step("测试用户的account_id"):
            account_id_list = ['cd7e353b-6f4c-45db-bdd5-78bdc13a53c7', 'c328af6a-c523-4032-9181-0596c7db6db7',
                               'bacf2b3e-6599-44f4-adf6-c4c13ff40946']
        for account_id in account_id_list:
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
                        connect_header['ACCESS-SIGN'] = sign
                        connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_header['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币入账信息, 入币方式SIC"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(self.url, account_id, i, 'SIC'), headers=connect_header)
                    if i == 'BRL':
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA019', "获取账户BRL单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                    elif i == 'CHF':
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['meta'] is not None, "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                    elif i == 'EUR' or i == 'GBP':
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA014', "获取账户单币入账信息, EUR入币方式Faster Payments错误，返回值是{}".format(
                                r.text)

    @allure.title('test_deposit_004')
    @allure.description('账户操作相关--获取账户单币入账信息，币种错误校验')
    def test_deposit_004(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                    account_id, 'abc', 'SIC'), nonce=nonce)
            connect_header['ACCESS-SIGN'] = sign
            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_header['ACCESS-NONCE'] = nonce
        with allure.step("获取账户单币入账信息, 入币方式SIC"):
            r = session.request('GET',
                                url='{}/accounts/{}/balances/{}/deposit/{}'.
                                format(self.url, account_id, 'abc', 'SIC'), headers=connect_header)
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA019', "获取账户BRL单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
            with allure.step("校验返回值"):
                assert r.json()['message'] == 'invalid symbol', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)

    @allure.title('test_deposit_005')
    @allure.description('账户操作相关--获取账户单币入账信息，CHF入币方式SIC')
    def test_deposit_005(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                    account_id, 'CHF', 'SIC'), nonce=nonce)
            connect_header['ACCESS-SIGN'] = sign
            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_header['ACCESS-NONCE'] = nonce
        with allure.step("获取账户单币CHF入账信息, 入币方式SIC"):
            r = session.request('GET',
                                url='{}/accounts/{}/balances/{}/deposit/{}'.
                                format(self.url, account_id, 'CHF', 'SIC'), headers=connect_header)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['meta']['account_name'] == 'Cabital Fintech (LT) UAB', "获取账户单币入账信息, account_name返回值是{}".format(r.text)
                assert r.json()['meta']['iban'] == 'CH7408799927511421001', "获取账户单币入账信息, iban返回值是{}".format(r.text)
                assert r.json()['meta']['ref_code'] == 'G79S3E', "获取账户单币入账信息,ref_code返回值是{}".format(r.text)
                assert r.json()['meta']['bic'] == 'INCOCHZZ', "获取账户单币入账信息, bic返回值是{}".format(r.text)
                assert r.json()['meta']['bank_name'] == 'InCore\xa0Bank\xa0AG', "获取账户单币入账信息, bank_name返回值是{}".format(r.text)
                assert r.json()['meta']['bank_address'] == 'Wiesenstrasse\xa017,\xa0Schlieren,\xa08952', "获取账户单币入账信息, bank_address错误，返回值是{}".format(r.text)
                assert r.json()['meta']['bank_country'] == 'Switzerland', "获取账户单币入账信息, bank_country返回值是{}".format(r.text)

    @allure.title('test_deposit_006')
    @allure.description('账户操作相关--获取账户单币入账信息，EUR入币方式SEPA')
    def test_deposit_006(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                    account_id, 'EUR', 'SEPA'), nonce=nonce)
            connect_header['ACCESS-SIGN'] = sign
            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_header['ACCESS-NONCE'] = nonce
        with allure.step("获取账户单币EUR入账信息, 入币方式SEPA"):
            r = session.request('GET',
                                url='{}/accounts/{}/balances/{}/deposit/{}'.
                                format(self.url, account_id, 'EUR', 'SEPA'), headers=connect_header)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['meta']['account_name'] == 'Cabital Fintech (LT) UAB', "获取账户单币入账信息, account_name返回值是{}".format(r.text)
                assert r.json()['meta']['iban'] == 'CH1808799927511379814', "获取账户单币入账信息, iban返回值是{}".format(r.text)
                assert r.json()['meta']['ref_code'] == 'G79S3E', "获取账户单币入账信息,ref_code返回值是{}".format(r.text)
                assert r.json()['meta']['bic'] == 'INCOCHZZXXX', "获取账户单币入账信息, bic返回值是{}".format(r.text)
                assert r.json()['meta']['bank_name'] == 'InCore Bank AG', "获取账户单币入账信息, bank_name返回值是{}".format(r.text)
                assert r.json()['meta']['bank_address'] == 'Wiesenstrasse 17', "获取账户单币入账信息, bank_address错误，返回值是{}".format(r.text)
                assert r.json()['meta']['bank_country'] == 'Switzerland', "获取账户单币入账信息, bank_country返回值是{}".format(r.text)

    @allure.title('test_deposit_007')
    @allure.description('账户操作相关--获取账户单币入账信息，GBP入币方式Faster Payments')
    def test_deposit_007(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                    account_id, 'GBP', 'FPS'), nonce=nonce)
            connect_header['ACCESS-SIGN'] = sign
            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_header['ACCESS-NONCE'] = nonce
        with allure.step("获取账户单币GBP入账信息, 入币方式Faster Payments"):
            r = session.request('GET',
                                url='{}/accounts/{}/balances/{}/deposit/{}'.
                                format(self.url, account_id, 'GBP', 'FPS'), headers=connect_header)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['meta']['account_name'] == 'Cabital Fintech (LT) UAB', "获取账户单币入账信息, account_name返回值是{}".format(r.text)
                assert r.json()['meta']['account_number'] == '00003157', "获取账户单币入账信息, account_number返回值是{}".format(r.text)
                assert r.json()['meta']['ref_code'] == 'G79S3E', "获取账户单币入账信息,ref_code返回值是{}".format(r.text)
                assert r.json()['meta']['sort_code'] == '040541', "获取账户单币入账信息,sort_code返回值是{}".format(r.text)
                assert r.json()['meta']['bank_name'] == 'BCB Payments Ltd', "获取账户单币入账信息, bank_name返回值是{}".format(r.text)
                assert r.json()['meta']['bank_address'] == '5 Merchant Square London', "获取账户单币入账信息, bank_address错误，返回值是{}".format(r.text)
                assert r.json()['meta']['bank_country'] == 'United Kingdom', "获取账户单币入账信息, bank_country返回值是{}".format(r.text)