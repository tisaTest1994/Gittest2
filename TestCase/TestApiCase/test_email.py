from Function.api_function import *
from Function.operate_sql import *


@allure.feature("email 相关 testcases")
class TestEmailApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers(account=get_json()['email']['payout_email'])

    @allure.title('test_email_001')
    @allure.description('忘记密码并且验证code')
    def test_email_001(self):
        with allure.step("改变测试账号"):
            account = get_json()['email']['payout_email']
        with allure.step("发忘记密码邮件"):
            code = ApiFunction.get_verification_code('FORGET_PASSWORD', account)
        with allure.step("验证忘记密码邮件"):
            ApiFunction.verify_verification_code('FORGET_PASSWORD', account, code)

    @allure.title('test_email_002')
    @allure.description('开启MFA且验证code')
    def test_email_002(self):
        with allure.step("改变测试账号"):
            account = get_json()['email']['payout_email']
        with allure.step("开启MFA且验证code"):
            code = ApiFunction.get_verification_code('ENABLE_MFA', account)
        with allure.step("开启MFA且验证code"):
            ApiFunction.verify_verification_code('ENABLE_MFA', account, code)

    @allure.title('test_email_003')
    @allure.description('关闭MFA且验证code')
    def test_email_003(self):
        with allure.step("改变测试账号"):
            account = get_json()['email']['payout_email']
        with allure.step("关闭MFA且验证code"):
            code = ApiFunction.get_verification_code('DISABLE_MFA', account)
        with allure.step("关闭MFA且验证code"):
            ApiFunction.verify_verification_code('DISABLE_MFA', account, code)

    @allure.title('test_email_004')
    @allure.description('MFA且验证code')
    def test_email_004(self):
        with allure.step("改变测试账号"):
            account = get_json()['email']['payout_email']
        with allure.step("MFA且验证code"):
            code = ApiFunction.get_verification_code('MFA_EMAIL', account)
        with allure.step("MFA且验证code"):
            ApiFunction.verify_verification_code('MFA_EMAIL', account, code)
