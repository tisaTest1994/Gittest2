from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api connect 相关 testcases")
class TestMobileApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_mobile_001')
    @allure.description('获取合作方配置')
    def test_mobile_001(self):
        with allure.step("获取合作方配置"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(env_url, get_json()['infinni_games'][
                'partner_id']), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['configs'] is not None, "获取合作方配置错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_002')
    @allure.description('合作方划转交易费用')
    def test_mobile_002(self):
        with allure.step("合作方划转交易费用"):
            data = {
                "amount": "50",
                "symbol": "USDT",
                "direction": "DEBIT"
            }
            r = session.request('POST', url='{}/connect/{}/transfer/fee'.format(env_url, get_json()['infinni_games'][
                'partner_id']), data=json.dumps(data), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                logger.info('返回值是{}'.format(str(r.text)))
                assert r.json()['fee']['amount'] == '0', "合作方划转交易费用错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_003')
    @allure.description('合作方划转交易 预校验')
    def test_mobile_003(self):
        with allure.step("合作方划转交易 预校验"):
            data = {
                "amount": "50",
                "symbol": "USDT",
                "direction": "DEBIT",
                "account_vid": "d9f35f7c-ec94-425d-9f66-95585457bb7d",
                "user_ext_ref": "james.lee@cabital.com"
            }
            r = session.request('POST', url='{}/connect/{}/transfer/confirm'.format(env_url, get_json()['infinni_games'][
                'partner_id']), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, "合作方划转交易 预校验错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_004')
    @allure.description('合作方划转交易')
    def test_mobile_004(self):
        with allure.step("合作方划转交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
        with allure.step("参数"):
            data = {
                "amount": "50",
                "symbol": "USDT",
                "direction": "DEBIT",
                "account_vid": "d9f35f7c-ec94-425d-9f66-95585457bb7d",
                "user_ext_ref": "james.lee@cabital.com"
            }
            r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url, get_json()['infinni_games'][
                'partner_id']), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, "合作方划转交易错误，返回值是{}".format(r.text)