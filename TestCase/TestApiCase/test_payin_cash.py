from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api pay in cash相关 testcases")
class TestPayInCashApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_pay_in_cash_001')
    @allure.description('获得法币充值币种')
    def test_pay_in_cash_001(self):
        with allure.step("充值币种"):
            r = session.request('GET', url='{}/pay/deposit/ccy/{}'.format(env_url, 'fiat'), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                for i in get_json()['cash_list']:
                    assert i in str(r.json()['fiat']), "获得法币充值币种错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_cash_002')
    @allure.description('获得全部货币充值币种')
    def test_pay_in_cash_002(self):
        with allure.step("充值币种"):
            r = session.request('GET', url='{}/pay/deposit/ccy/{}'.format(env_url, ''), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                for i in get_json()['crypto_list']:
                    assert i in str(r.json()['crypto']), "获得法币充值币种错误，返回值是{}".format(r.text)
                for i in get_json()['cash_list']:
                    assert i in str(r.json()['fiat']), "获得法币充值币种错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_cash_004')
    @allure.description('GBP法币充值账户信息')
    def test_pay_in_cash_004(self):
        with allure.step("GBP法币充值账户"):
            r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'GBP', 'Faster Payments'),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['bank_accounts'][0][
                           'account_name'] == 'Cabital Fintech (LT) UAB', "GBP法币充值账户信息错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_cash_005')
    @allure.description('EUR法币充值账户信息')
    def test_pay_in_cash_005(self):
        with allure.step("EUR法币充值账户信息"):
            r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'EUR', 'SEPA'), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['bank_accounts'][0][
                           'account_name'] == 'Cabital Fintech (LT) UAB', "EUR法币充值账户信息错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_cash_006')
    @allure.description('CHF法币充值账户信息')
    def test_pay_in_cash_006(self):
        with allure.step("CHF法币充值账户信息"):
            r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'CHF', 'SIC'), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['bank_accounts'][0][
                           'account_name'] == 'Cabital Fintech (LT) UAB', "CHF法币充值账户信息错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_cash_007')
    @allure.description('BRL法币充值账户信息')
    def test_pay_in_cash_007(self):
        with allure.step("BRL法币充值账户信息"):
            r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'BRL', 'PIX'), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                logger.info(r.json())
                assert r.json()['bank_accounts'][0][
                           'account_name'] == '3RZ SERVICOS DIGITAIS LTDA', "BRL法币充值账户信息错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_cash_008')
    @allure.description('Plaid 转出币种限制')
    def test_pay_in_cash_008(self):
        with allure.step("Plaid 转出币种限制"):
            balance_list = get_json()['cash_list']
            for i in balance_list:
                if i != 'CHF' and i != 'BRL' and i != 'VND':
                    r = session.request('GET', url='{}/pay/plaid/limit/{}'.format(env_url, i), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['min'] == '1', "Plaid 转出币种限制最小值错误，返回值是{}".format(r.text)
                    assert r.json()['max'] == '5', "Plaid 转出币种限制最大值错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_cash_009')
    @allure.description('BRL 创造pay in bank account数据')
    def test_pay_in_cash_009(self):
        with allure.step("切换账号"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("增加headers验证"):
            order_id = uuid.uuid1()
        with allure.step("BRL pay in数据"):
            data = {
                "currencyCode": "BRL",
                "method": "BankAccount",
                "orderType": "deposit",
                "requisite": {
                    "account": "101112345",
                    "bankCompe": "033",
                    "bankIspb": "90400888",
                    "bankName": "Banco Santander (Brasil) S.A. (033)",
                    "branch": "1234",
                    "holderDocument": "976.111.142-99",
                    "holderName": "Richard Wan",
                    "isSavings": False
                },
                "userData": [
                    {
                        "birthday": "2022-03-10",
                        "cpfCnpj": "976.111.142-99",
                        "document": "976.111.142-99",
                        "documentExpiry": "2025-01-01",
                        "documentType": "passport",
                        "fullName": "Richard Wan"
                    }
                ],
                "userEmail": get_json()['email']['payout_email'],
                "userPhone": "+5511987654311",
                "userType": "personal",
                "value": "12.00"
            }
            r = session.request('POST',
                                url='{}/Partner/Orders/{}'.format(get_json()['sandbox']['BRL']['url'], order_id),
                                data=(data), auth=(get_json()['sandbox']['BRL']['username'],
                                                   get_json()['sandbox']['BRL']['password']))
            print(r.text)

    @allure.title('test_pay_in_cash_010')
    @allure.description('BRL 创造pay in PixKey数据')
    def test_pay_in_cash_010(self):
        with allure.step("切换账号"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("增加headers验证"):
            order_id = uuid.uuid1()
        with allure.step("BRL pay in数据"):
            data = {
                "currencyCode": "BRL",
                "method": "PixKey",
                "requisite": {
                    "keyType": "cpf",
                    "key": "976.111.142-99"
                },
                "orderType": "deposit",
                "userData": [
                    {
                        "cpfCnpj": "976.111.142-99",
                        "fullName": "Richard Wan"
                    }
                ],
                "userEmail": get_json()['email']['payout_email'],
                "userNotify": False,
                "userPhone": "+5511987654311",
                "userType": "personal",
                "value": "15.00"
            }
            r = session.request('POST',
                                url='{}/Partner/Orders/{}'.format(get_json()['sandbox']['BRL']['url'], order_id),
                                data=data, auth=(get_json()['sandbox']['BRL']['username'],
                                                   get_json()['sandbox']['BRL']['password']))
            print(r.text)

    # @allure.title('test_pay_in_cash_011')
    # @allure.description('GBP法币充值账户信息')
    # def test_pay_in_cash_011(self):
    #     with allure.step("GBP法币充值账户"):
    #         r = session.request('GET', url='{}/pay/deposit/{}'.format(env_url, 'USD'),
    #                             headers=headers)
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert r.json()['bank_accounts'][0][
    #                        'account_name'] == 'Cabital Fintech (LT) UAB', "GBP法币充值账户信息错误，返回值是{}".format(r.text)
    #
    # @allure.title('test_pay_in_cash_011')
    # @allure.description('GBP法币充值账户信息')
    # def test_pay_in_cash_004(self):
    #     with allure.step("GBP法币充值账户"):
    #         r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'USD', 'SWIFT'),
    #                             headers=headers)
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert r.json()['bank_accounts'][0][
    #                        'account_name'] == 'Cabital Fintech (LT) UAB', "GBP法币充值账户信息错误，返回值是{}".format(r.text)