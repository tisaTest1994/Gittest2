from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api circle 相关 testcases")
class TestUSDCApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_circle_001')
    @allure.description('USD 个人 payin')
    def test_circle_001(self):
        headers[
            'Authorization'] = "Bearer QVBJX0tFWTozMzY4OGI0ZTdjYTgzYjlmODU2ODIzNjlhZTU2OGEzZTplMWNjMWQyMGQxNThiMTUwMDU5NzI0N2ZjMmYxZTA4OQ=="
        with allure.step("payin"):
            data = {
                'trackingRef': 'CIR25EANVT',
                'beneficiaryBank': {
                    'accountNumber': '123119341897'
                },
                'amount': {
                    'amount': '23.00',
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

    @allure.title('test_circle_002')
    @allure.description('USD 个人 payout')
    def test_circle_002(self):
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

    @allure.title('test_circle_003')
    @allure.description('USD 商户 payin')
    def test_circle_003(self):
        headers[
            'Authorization'] = "Bearer QVBJX0tFWTozMzY4OGI0ZTdjYTgzYjlmODU2ODIzNjlhZTU2OGEzZTplMWNjMWQyMGQxNThiMTUwMDU5NzI0N2ZjMmYxZTA4OQ=="
        with allure.step("payin"):
            data = {
                'trackingRef': 'CIR2JN4JRH',
                'beneficiaryBank': {
                    'accountNumber': '123373874035'
                },
                'amount': {
                    'amount': '300.00',
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

    @allure.title('test_circle_004')
    @allure.description('USD 商户 payout')
    def test_circle_004(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("payout"):
            data = {
                "account_id": "a27f5914-9416-48be-bf56-bc9eeac18a64",
                "legal_entity": 1,
                "code": "USD",
                "amount": "130",
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

    @allure.title('test_circle_005')
    @allure.description('验证从circle 处获得payin的数据')
    def test_circle_005(self):
        headers[
            'Authorization'] = "Bearer QVBJX0tFWTozMzY4OGI0ZTdjYTgzYjlmODU2ODIzNjlhZTU2OGEzZTplMWNjMWQyMGQxNThiMTUwMDU5NzI0N2ZjMmYxZTA4OQ=="
        with allure.step("check"):
            circle_id = '8d9b4217-3a2e-40f7-a6a8-94b65fb8fd4d'
            r = session.request('GET', url='https://api-sandbox.circle.com/v1/payments/{}'.format(circle_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_circle_006')
    @allure.description('验证从circle 处获得payout的数据')
    def test_circle_006(self):
        headers[
            'Authorization'] = "Bearer QVBJX0tFWTozMzY4OGI0ZTdjYTgzYjlmODU2ODIzNjlhZTU2OGEzZTplMWNjMWQyMGQxNThiMTUwMDU5NzI0N2ZjMmYxZTA4OQ=="
        with allure.step("check"):
            circle_id = '87bc6a99-c8da-46ba-a0cc-bad89e75903b'
            r = session.request('GET', url='https://api-sandbox.circle.com/v1/payouts/{}'.format(circle_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

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
                "amount": "40.22",
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

    @allure.title('test_usdc_002')
    @allure.description('USDC 商户 ERC20 payout')
    def test_usdc_002(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("payout"):
            data = {
                "account_id": "a27f5914-9416-48be-bf56-bc9eeac18a64",
                "legal_entity": 1,
                "code": "USDC",
                "amount": "41.22",
                "chain": "ETH",
                "address": "0x60CB212F15dcEf185240d43C4e162C730fA8a9C2"
            }
            r = session.request('POST', url='https://opapi.cabital.io/api/v1/operatorapi/txns/payout/create/crypto',
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)


