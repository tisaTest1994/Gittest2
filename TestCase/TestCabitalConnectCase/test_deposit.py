from Function.api_function import *
from Function.operate_sql import *


# 账户操作相关--账户入币信息
class TestDepositApi:

    # 初始化class
    def setup(self):
        ApiFunction.add_headers()

    @allure.title('test_deposit_001')
    @allure.description('获取EUR deposit 信息')
    def test_deposit_001(self, partner):
        with allure.step("获取用户的所有账户余额"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'EUR' and i['deposit_methods'][0] == 'SEPA':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(30)
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_vid, 'EUR', 'SEPA'), connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币EUR入账信息, 入币方式SEPA"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'EUR', 'SEPA'), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['meta'][
                                       'account_name'] == 'Cabital Fintech (LT) UAB', "获取账户单币入账信息, account_name返回值是{}".format(
                                r.text)
                            assert r.json()['meta']['iban'] == 'CH1808799927511379814', "获取账户单币入账信息, iban返回值是{}".format(
                                r.text)
                            assert r.json()['meta']['ref_code'] == '8VVSNP', "获取账户单币入账信息,ref_code返回值是{}".format(r.text)
                            assert r.json()['meta']['bic'] == 'INCOCHZZXXX', "获取账户单币入账信息, bic返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'bank_name'] == 'InCore Bank AG', "获取账户单币入账信息, bank_name返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'bank_address'] == 'Wiesenstrasse 17', "获取账户单币入账信息, bank_address错误，返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'bank_country'] == 'Switzerland', "获取账户单币入账信息, bank_country返回值是{}".format(r.text)

    @allure.title('test_deposit_002')
    @allure.description('获取GBP deposit 信息')
    def test_deposit_002(self, partner):
        with allure.step("获取用户的所有账户余额"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'GBP' and i['deposit_methods'][0] == 'FPS':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(30)
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_vid, 'GBP', 'FPS'), connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币EUR入账信息, 入币方式SEPA"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'GBP', 'FPS'), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['meta'][
                                       'account_name'] == 'Cabital Fintech (LT) UAB', "获取账户单币入账信息, account_name返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'account_number'] == '00003157', "获取账户单币入账信息, account_number返回值是{}".format(
                                r.text)
                            assert r.json()['meta']['ref_code'] == '8VVSNP', "获取账户单币入账信息,ref_code返回值是{}".format(r.text)
                            assert r.json()['meta']['sort_code'] == '040541', "获取账户单币入账信息,sort_code返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'bank_name'] == 'BCB Payments Ltd', "获取账户单币入账信息, bank_name返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'bank_address'] == '5 Merchant Square London', "获取账户单币入账信息, bank_address错误，返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'bank_country'] == 'United Kingdom', "获取账户单币入账信息, bank_country返回值是{}".format(
                                r.text)

    @allure.title('test_deposit_003')
    @allure.description('获取CHF deposit 信息')
    def test_deposit_003(self, partner):
        with allure.step("获取用户的所有账户余额"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'CHF' and i['deposit_methods'][0] == 'SIC':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(30)
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_vid, 'CHF', 'SIC'), connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币EUR入账信息, 入币方式SEPA"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'CHF', 'SIC'), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['meta']['account_name'] == 'Cabital Fintech (LT) UAB', "获取账户单币入账信息, account_name返回值是{}".format(
                                r.text)
                            assert r.json()['meta']['iban'] == 'CH7408799927511421001', "获取账户单币入账信息, iban返回值是{}".format(
                                r.text)
                            assert r.json()['meta']['ref_code'] == '8VVSNP', "获取账户单币入账信息,ref_code返回值是{}".format(r.text)
                            assert r.json()['meta']['bic'] == 'INCOCHZZ', "获取账户单币入账信息, bic返回值是{}".format(r.text)
                            assert r.json()['meta']['bank_name'] == 'InCore\xa0Bank\xa0AG', "获取账户单币入账信息, bank_name返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'bank_address'] == 'Wiesenstrasse\xa017,\xa0Schlieren,\xa08952', "获取账户单币入账信息, bank_address错误，返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'bank_country'] == 'Switzerland', "获取账户单币入账信息, bank_country返回值是{}".format(r.text)

    @allure.title('test_deposit_004')
    @allure.description('获取GBP deposit 信息')
    def test_deposit_004(self, partner):
        with allure.step("获取用户的所有账户余额"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'GBP' and i['deposit_methods'][0] == 'FPS':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(30)
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_vid, 'GBP', 'FPS'), connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币GBP入账信息, 入币方式FPS"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'GBP', 'FPS'), headers=connect_headers)
                        with allure.step("校验状态码"):
                            print(r.text)
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['meta'][
                                       'account_name'] == 'Cabital Fintech (LT) UAB', "获取账户单币入账信息, account_name返回值是{}".format(
                                r.text)
                            assert r.json()['meta']['ref_code'] == '8VVSNP', "获取账户单币入账信息,ref_code返回值是{}".format(r.text)
                            assert r.json()['meta']['account_number'] == '00003157', "获取账户单币入账信息, account_number返回值是{}".format(r.text)
                            assert r.json()['meta']['sort_code'] == '040541', "获取账户单币入账信息, sort_code返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'bank_name'] == 'BCB Payments Ltd', "获取账户单币入账信息, bank_name返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'bank_address'] == '5 Merchant Square London', "获取账户单币入账信息, bank_address错误，返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'bank_country'] == 'United Kingdom', "获取账户单币入账信息, bank_country返回值是{}".format(r.text)
