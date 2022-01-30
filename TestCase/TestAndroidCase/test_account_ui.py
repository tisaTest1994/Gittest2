from Function.ui_function import *
import allure
from Function.api_common_function import *


class TestAccountUi:

    def setup_method(self):
        with allure.step("打开 app"):
            start_app(package_name)

    def teardown(self):
        with allure.step("关闭 app"):
            stop_app(package_name)

    @allure.title('test_account_001')
    @allure.description('使用已经注册账户登录，登录进入主页后退出')
    @pytest.fixture(scope='session')
    def test_account_001(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
            sleep(5)
        with allure.step("登出"):
            UiFunction.logout()
            sleep(3)

    @allure.title('test_account_002')
    @allure.description('注册新账号')
    def test_account_002(self):
        with allure.step("判断升级提示"):
            if operate_element_app('welcomePage', 'Later', type='check', wait_time_max=10):
                operate_element_app('welcomePage', 'Later')
        with allure.step("先判断是否已经登录，判断升级提示"):
            if operate_element_app('portfolioPage', 'Portfolio', type='check'):
                return True
            else:
                with allure.step("开始注册流程"):
                    operate_element_app('signupPage', 'Sign Up')
                    sleep(3)
                # assert断言进入注册页面
                with allure.step("检查是否到达Sign Up 页面"):
                    assert operate_element_app('signupPage', 'Sign up with email',type='check'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Sign up with email')
                with allure.step("输入邮箱"):
                    text(generate_email())
                with allure.step("勾选协议"):
                    operate_element_app('signupPage', 'rule box')
                with allure.step("点击发送验证码"):
                    operate_element_app('signupPage', "Send Verification Code", type='click')
                with allure.step("检查是否到达输入邮箱验证码页面"):
                    assert operate_element_app('signupPage', 'Verify your email', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Verify your email')
                # with allure.step("Resend"):
                #     operate_element_app('signupPage', "Resend", type='click')
                with allure.step("输入邮箱验证码"):
                    text(get_json()['web'][get_json()['env']]['code'])
                # assert断言Next按钮可点击
                with allure.step("点击Next"):
                    operate_element_app('signupPage', "Next", type='click')
                with allure.step("断言进入设置密码页面"):
                    assert operate_element_app('signupPage', 'Set login password', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Set login password')
                with allure.step("设置密码"):
                    operate_element_app('signupPage', 'password', type='input', input_string=get_json()['web'][get_json()['env']]['password'])
                with allure.step("点击Confirm Password"):
                    operate_element_app('signupPage', "Confirm Password", type='click')
                with allure.step("断言进入设置密码页面"):
                    assert operate_element_app('signupPage', 'Total Assert Value', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Total Assert Value')














