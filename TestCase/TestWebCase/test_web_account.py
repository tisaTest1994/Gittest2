from Function.web_function import *
from Function.api_function import *


class TestWebAccountApi:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()
        self.driver = webFunction.launch_web(self.web_url)
        webFunction.login_web(self.driver)

    def teardown_method(self):
        webFunction.logout_web(self.driver)
        self.driver.close()

    @allure.title('test_web_account_001 ')
    def test_web_account_001(self):
        pass
    def test_web_account_002(self):
        webFunction.Account_setting(self.driver)
        webFunction.change_password(self.driver)

    @allure.testcase('test_web_account_Setting_003 ')
    def test_web_account_003(self):
        webFunction.Account_setting(self.driver)
        webFunction.edit_accountname(self.driver)

    @allure.testcase('test_web_account_Setting_004 ')
    def test_web_account_Setting_004(self,account=get_json()['web'][get_json()['env']]['account'], code=get_json()['web'][get_json()['env']]['code']):
        webFunction.Account_setting(self.driver)
        with allure.step("点击修改disable"):
            text = get_element_text(self.driver, 'AccountSetPage', 'account-change-mfa-trigger')
            if text == 'Disable':
                operate_element(self.driver, 'AccountSetPage', 'account-change-mfa-trigger', type='click')
        with allure.step("输入邮箱验证码"):
            operate_element(self.driver, 'AccountSetPage', 'mailcode', type='clean')
            operate_element(self.driver, 'AccountSetPage', 'mailcode', type='input', input=code)
        with allure.step("获取MFA验证码"):
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
        with allure.step("输入google验证码"):
            operate_element(self.driver, 'AccountSetPage', 'disable-gauth-code', type='clean')
            operate_element(self.driver, 'AccountSetPage', 'disable-gauth-code', type='input', input=mfaVerificationCode)
        with allure.step("点击Confirm"):
            operate_element(self.driver, 'AccountSetPage', 'update-gauth-btn-submit', type='click')











