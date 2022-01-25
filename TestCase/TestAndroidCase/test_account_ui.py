from Function.ui_function import *
import allure


class TestAccountUi:

    def setup_method(self):
        with allure.step("打开 app"):
            start_app(package_name)

    def teardown(self):
        with allure.step("关闭 app"):
            stop_app(package_name)

    @allure.title('test_account_001')
    @allure.description('使用已经注册账户登录，登录进入主页后退出')
    def test_account_001(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
            sleep(5)
        with allure.step("登出"):
            UiFunction.logout()
            sleep(3)

