from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api circel 相关 testcases")
class TestUSDCApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_circel_001')
    @allure.description('USD 个人 payin')
    def test_circel_001(self):
        headers[
            'Authorization'] = "Bearer QVBJX0tFWTozMzY4OGI0ZTdjYTgzYjlmODU2ODIzNjlhZTU2OGEzZTplMWNjMWQyMGQxNThiMTUwMDU5NzI0N2ZjMmYxZTA4OQ=="
        with allure.step("payin"):
            data = {
                'trackingRef': 'CIR25EANVT',
                'beneficiaryBank': {
                    'accountNumber': '123119341897'
                },
                'amount': {
                    'amount': '3.00',
                    'currency': 'USD'
                }
            }
            r = session.request('POST', url='https://api-sandbox.circle.com/v1/mocks/payments/wire',
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 201, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_circel_002')
    @allure.description('USD 个人 payout')
    def test_circel_002(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("payout"):
            data = {
                "account_id": "700dca34-1e6f-408b-903d-e37d0fcfd615",
                "legal_entity": 1,
                "code": "USD",
                "amount": "50",
                "payment_method": "Wire",
                "bank_account_id": "dfaeabff-3d48-4e5b-9d25-950c18782998",
                "email": "external.qa@cabital.com"
            }
            r = session.request('POST', url='https://opapi.cabital.io/api/v1/operatorapi/txns/payout/create/fiat',
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_circel_003')
    @allure.description('USD 商户 payin')
    def test_circel_003(self):
        headers[
            'Authorization'] = "Bearer QVBJX0tFWTozMzY4OGI0ZTdjYTgzYjlmODU2ODIzNjlhZTU2OGEzZTplMWNjMWQyMGQxNThiMTUwMDU5NzI0N2ZjMmYxZTA4OQ=="
        with allure.step("payin"):
            data = {
                'trackingRef': 'CIR25EANVT',
                'beneficiaryBank': {
                    'accountNumber': '123119341897'
                },
                'amount': {
                    'amount': '3.00',
                    'currency': 'USD'
                }
            }
            r = session.request('POST', url='https://api-sandbox.circle.com/v1/mocks/payments/wire',
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 201, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_circel_004')
    @allure.description('USD 商户 payout')
    def test_circel_004(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("payout"):
            data = {
                "account_id": "700dca34-1e6f-408b-903d-e37d0fcfd615",
                "legal_entity": 1,
                "code": "USD",
                "amount": "20",
                "payment_method": "Wire",
                "bank_account_id": "dfaeabff-3d48-4e5b-9d25-950c18782998",
                "email": "external.qa@cabital.com"
            }
            r = session.request('POST', url='https://opapi.cabital.io/api/v1/operatorapi/txns/payout/create/fiat',
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 201, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_usdc_001')
    @allure.description('USDC 个人 ERC20 payout')
    def test_usdc_001(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("payout"):
            data = {
                "account_id": "700dca34-1e6f-408b-903d-e37d0fcfd615",
                "legal_entity": 1,
                "code": "USDC",
                "amount": "40.231231",
                "chain": "ETH",
                "address": "0x465d39f446f3EE9867B318A5bB98EF7dA796DFbA"
            }
            r = session.request('POST', url='https://opapi.cabital.io/api/v1/operatorapi/txns/payout/create/crypto',
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)