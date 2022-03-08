from Function.web_function import *
from Function.web_common_function import *
from Function.api_common_function import *


@allure.feature("web ui log in 相关 testcases")
class TestWebLogin:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency

    def teardown_method(self):
        pass

    @allure.title('test_web_login_001')
    @allure.description('登录账号')
    def test_login_001(self, chrome_driver):
        account = get_json()['web'][get_json()['env']]['account']
        password = get_json()['web'][get_json()['env']]['password']
        with allure.step("输入登录账号"):
            operate_element_web(chrome_driver, 'loginPage', 'username', 'delete')
            operate_element_web(chrome_driver, 'loginPage', 'username', 'input', input_string=account)
        with allure.step("输入登录密码"):
            operate_element_web(chrome_driver, 'loginPage', 'sign_password_input', 'delete')
            operate_element_web(chrome_driver, 'loginPage', 'sign_password_input', 'input', input_string=password)
        with allure.step("点击sign in"):
            operate_element_web(chrome_driver, 'loginPage', 'login_login')
            sleep(2)
        with allure.step("确定已经登录成功到首页"):
            assert operate_element_web(chrome_driver, 'assetPage', 'Cabital Logo', 'check'), '未成功登录'
            sleep(2)

    @allure.title('test_web_login_002')
    @allure.description('重置密码')
    def test_login_002(self, chrome_driver):
        account = "yanting.huang@cabital.com"
        password = "123456Hyt"
        email_code = get_json()['web'][get_json()['env']]['code']
        new_pword = '123456Test'
        with allure.step("确认弹出重置密码框"):
            operate_element_web(chrome_driver, 'loginPage', 'login_forgotpw')
            assert operate_element_web(chrome_driver, 'loginPage', 'dialog_forgetpassword_email_input', 'check'), '未弹出重置密码框'
        with allure.step("输入需要重置密码账号"):
            operate_element_web(chrome_driver, 'loginPage', 'dialog_forgetpassword_email_input', 'input',
                                input_string=account)
        with allure.step("输入邮箱验证码"):
            operate_element_web(chrome_driver, 'loginPage', 'mailcode', 'input', email_code)
        with allure.step("输入新密码"):
            operate_element_web(chrome_driver, 'loginPage', 'dialog_forgetpassword_password_input', 'input', new_pword)
        with allure.step("点击comfirm按钮，确认修改密码"):
            operate_element_web(chrome_driver, 'loginPage', 'dialog_forgetpassword_confirm')
            time.sleep(2)
        with allure.step("用新密码登录账号"):
            with allure.step("输入账号"):
                operate_element_web(chrome_driver, 'loginPage', 'username', 'delete')
                operate_element_web(chrome_driver, 'loginPage', 'username', 'input', input_string=account)
            with allure.step("输入密码"):
                operate_element_web(chrome_driver, 'loginPage', 'sign_password_input', 'delete')
                operate_element_web(chrome_driver, 'loginPage', 'sign_password_input', 'input', input_string=new_pword)
            with allure.step("点击sign in"):
                operate_element_web(chrome_driver, 'loginPage', 'login_login')
                sleep(2)
            with allure.step("确定已经登录成功到首页"):
                assert operate_element_web(chrome_driver, 'assetPage', 'Cabital Logo', 'check'), '未成功登录'
                sleep(2)
        with allure.step("再把密码改回成默认，保证脚本重复使用"):
            # 登出账号
            operate_element_web(chrome_driver, 'assetPage', 'header-btn-hi-nickname')
            operate_element_web(chrome_driver, 'assetPage', 'header-btn-user-signout')
            # 把账号密码改回城默认
            operate_element_web(chrome_driver, 'loginPage', 'login_forgotpw')
            assert operate_element_web(chrome_driver, 'loginPage', 'login_forgotpw', 'check'), '未弹出重置密码框'
            operate_element_web(chrome_driver, 'loginPage', 'dialog_forgetpassword_email_input', 'input',
                                input_string=account)
            operate_element_web(chrome_driver, 'loginPage', 'mailcode', 'input', email_code)
            operate_element_web(chrome_driver, 'loginPage', 'dialog_forgetpassword_password_input', 'input', password)
            operate_element_web(chrome_driver, 'loginPage', 'dialog_forgetpassword_confirm')

    @allure.title('test_web_login_003')
    @allure.description('Log in with Bybit')
    def test_login_003(self, chrome_driver):
        account = get_json()['web'][get_json()['env']]['account']
        password = get_json()['web'][get_json()['env']]['password']
        with allure.step("点击Log in with Bybit，跳转至bybit登录页面"):
            operate_element_web(chrome_driver, 'loginPage', 'login_partner')
            assert operate_element_web(chrome_driver, 'BybitPage', 'log-newui-head-title', 'check')
        with allure.step("输入电子邮箱"):
            operate_element_web(chrome_driver, 'BybitPage', 'username', 'input', account)
        with allure.step("输入登录密码"):
            operate_element_web(chrome_driver, 'BybitPage', 'password', 'input', password)
        with allure.step("点击继续"):
            operate_element_web(chrome_driver, 'BybitPage', 'log-newui-footer-submit')
            sleep(2)
        with allure.step("检查用bybit登录成功"):
            assert operate_element_web(chrome_driver, 'assetPage', 'Cabital Logo', 'check'), '未成功登录'
            sleep(2)
