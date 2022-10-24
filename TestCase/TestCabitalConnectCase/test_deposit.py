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
        with allure.step("获取用户VID"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'EUR' and i['deposit_methods'][0] == 'SEPA':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
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
        with allure.step("获取用户VID"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'GBP' and i['deposit_methods'][0] == 'FPS':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
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
        with allure.step("获取用户VID"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'CHF' and i['deposit_methods'][0] == 'SIC':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
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
    @allure.description('获取USD deposit 信息')
    def test_deposit_004(self, partner):
        with allure.step("获取用户VID"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'USD' and i['deposit_methods'][0] == 'SWIFT':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_vid, 'USD', 'SWIFT'), connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币USD入账信息, 入币方式SWIFT"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'USD', 'SWIFT'), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['symbol'] == 'USD', "获取账户单币入账信息, symbol返回值是{}".format(r.text)
                            assert r.json()['method'] == 'SWIFT', "获取账户单币入账信息, method返回值是{}".format(r.text)
                            assert r.json()['meta']['bound_bank_accounts'][0]['source_bank_account']['account_name'] == 'Wan yilei', "获取账户单币入账信息, account_name返回值是{}".format(r.text)
                            assert r.json()['meta']['bound_bank_accounts'][0]['source_bank_account']['account_number'] == '1234223432344236', "获取账户单币入账信息, account_number返回值是{}".format(r.text)
                            assert r.json()['meta']['bound_bank_accounts'][0]['source_bank_account']['aba_routing_number'] == '121000248', "获取账户单币入账信息, aba_routing_number返回值是{}".format(r.text)

    @allure.title('test_deposit_005')
    @allure.description('获取BRL deposit ,cpf状态为0 null，partner是latibac')
    def test_deposit_005(self, partner):
        with allure.step("获取用户VID"):
            account_vid = '0d004cd2-7c7e-4d29-bfff-2b496e5856cc'
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'BRL' and i['deposit_methods'][0] == 'PIX':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET',
                                                          url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                              account_vid, 'BRL', 'PIX'), connect_type=partner,
                                                          nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币GBP入账信息, 入币方式FPS"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'BRL', 'PIX'), headers=connect_headers)

                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA051', "获取账户单币入账信息, r.text返回值是{}".format(
                                r.text)

    @allure.title('test_deposit_006')
    @allure.description('获取BRL deposit ,cpf状态为5pass，partner是latibac')
    def test_deposit_006(self, partner):
        with allure.step("获取用户VID"):
            account_vid = '924558f6-4bbb-4f87-9165-94724e5d16cf'
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'BRL' and i['deposit_methods'][0] == 'PIX':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_vid, 'BRL', 'PIX'), connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币GBP入账信息, 入币方式FPS"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'BRL', 'PIX'), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['meta'][
                                       'account_name'] == '3RZ SERVICOS DIGITAIS LTDA', "获取账户单币入账信息, account_name返回值是{}".format(
                                r.text)
                            assert r.json()['meta']['account_number'] == '4663-9', "获取账户单币入账信息, account_number返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'bank_country'] == 'Brazil', "获取账户单币入账信息, bank_country返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'cpf'] == '123.322.238-98', "获取账户单币入账信息, cpf错误，返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'branch_code'] == '0001', "获取账户单币入账信息, branch_code'返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'tax_id'] == '32.611.536/0001-30', "获取账户单币入账信息, tax_id错误，返回值是{}".format(
                                r.text)

    @allure.title('test_deposit_007')
    @allure.description('获取BRL deposit ,cpf状态为3pass，partner是latibac')
    def test_deposit_007(self, partner):
        with allure.step("获取用户VID"):
            account_vid = 'df368955-2b9c-4af0-b8ea-8226fead4c5d'
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'BRL' and i['deposit_methods'][0] == 'PIX':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_vid, 'BRL', 'PIX'), connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币GBP入账信息, 入币方式FPS"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'BRL', 'PIX'), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['meta'][
                                       'account_name'] == '3RZ SERVICOS DIGITAIS LTDA', "获取账户单币入账信息, account_name返回值是{}".format(
                                r.text)
                            assert r.json()['meta']['account_number'] == '4663-9', "获取账户单币入账信息, account_number返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'bank_country'] == 'Brazil', "获取账户单币入账信息, bank_country返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'cpf'] == '580.143.165-92', "获取账户单币入账信息, cpf错误，返回值是{}".format(
                                r.text)
                            assert r.json()['meta'][
                                       'branch_code'] == '0001', "获取账户单币入账信息, branch_code'返回值是{}".format(r.text)
                            assert r.json()['meta'][
                                       'tax_id'] == '32.611.536/0001-30', "获取账户单币入账信息, tax_id错误，返回值是{}".format(
                                r.text)

    @allure.title('test_deposit_008')
    @allure.description('获取BRL deposit ,cpf状态为2failed，partner是latibac')
    def test_deposit_008(self, partner):
        with allure.step("获取用户VID"):
            account_vid = '044281ae-e06c-46e1-812f-74ad1ac68edc'
        with allure.step("判断partner是否支持deposit"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['symbol'] == 'BRL' and i['deposit_methods'][0] == 'PIX':
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(account_vid, 'BRL', 'PIX'), connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("获取账户单币GBP入账信息, 入币方式FPS"):
                        r = session.request('GET',
                                            url='{}/accounts/{}/balances/{}/deposit/{}'.
                                            format(connect_url, account_vid, 'BRL', 'PIX'), headers=connect_headers)

                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA051', "获取账户单币入账信息, r.text返回值是{}".format(
                                r.text)




