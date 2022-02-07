from Function.web_common_function import *
from Function.api_function import *
import allure


class webFunction:

    @staticmethod
    def launch_web(url):
        # os.path.abspath()获得绝对路径
        path = os.path.abspath(os.path.dirname(__file__))
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        # 指定浏览器的分辨率
        options.add_argument('--window-size=1920,1080')
        # 无界面运行
        # options.add_argument('--headless')
        # 判断运行环境
        if 'mac' in str(platform.platform()):
            driver = WebChrome(executable_path=path + "/../Resource/chromedriver_mac", chrome_options=options)
        else:
            driver = WebChrome(executable_path=path + "/../Resource/chromedriver_liunx", chrome_options=options)
        driver.get(url)
        return driver

    @staticmethod
    def login_web(account=get_json()['web'][get_json()['env']]['account'], password=get_json()['web'][get_json()['env']]['password']):
        with allure.step("确定打开登录页面"):
            assert operate_element_web('loginPage', 'signinForm', type='check'), '未打开登录页面'
        with allure.step("输入账号"):
            operate_element_web('loginPage', 'username', type='delete')
            operate_element_web('loginPage', 'username', type='input', input_string=account)
        with allure.step("输入密码"):
            operate_element_web('loginPage', 'sign_password_input', type='delete')
            operate_element_web('loginPage', 'sign_password_input', type='input', input_string=password)
        with allure.step("点击log in"):
            operate_element_web('loginPage', 'login_login')
            sleep(2)
        with allure.step("确定已经登录成功到首页"):
            assert operate_element_web('assetPage', 'Cabital Logo', type='check'), '未成功登录'
            sleep(2)

    # 登出 Web
    @staticmethod
    def logout_web():
        with allure.step("点击登出"):
            operate_element_web('assetPage', 'header-btn-hi-nickname')
            assert operate_element_web('assetPage', 'dialog_forgetpassword')

    # 注册 web
    @staticmethod
    def signup_web():
        test_account = generate_email()

        email_code = get_json()['web'][get_json()['env']]['code']
        pword = get_json()['web'][get_json()['env']]['password']
        password = get_json()['web'][get_json()['env']]['password']
        with allure.step("确定打开登录页面"):
            assert operate_element_web('loginPage', 'signinForm', type='check'), '未打开登录页面'
        with allure.step("填写注册信息"):
            # 点击signup按钮，跳转至signup页面
            operate_element_web('loginPage', "login_gotosignup")
            # 输入账号
            operate_element_web('signupPage', "signup_form_password_email", "input", test_account)
            # 点击发送验证码
            operate_element_web('signupPage', "signup_sendcode")
            # 输入验证码
            operate_element_web('signupPage', "mailcode", "input", email_code)
            # 输入密码
            operate_element_web('signupPage', "signup_form_password_input", "input", password)
            # 勾选复选框
            operate_element_web('signupPage', "signup_termschk")
            # 点击注册按钮
            operate_element_web('signupPage', "signup_registernow")
            time.sleep(2)
        with allure.step("确定注册成功"):
            account_name = test_account.split('@')
            operate_element_web("AccountSetPage", "mainpage_menu_account")
            assert operate_element_web("AccountSetPage", "account-nickname", "get_text") == \
                account_name[0], "注册失败"


