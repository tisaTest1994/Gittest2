from Function.ui_function import *
import allure


class TestAccountUi:

    # 每个cases前执行
    def setup(self):
        # 打开 app
        start_app(package_name)

    # 每个cases结束后
    def teardown(self):
        stop_app(package_name)
        sleep(2)

    @allure.testcase('test_account_001 使用已经注册账户登录，登录进入主页后退出')
    def test_account_001(self):
        with allure.step("登录"):
            UiFunction.login(account=email['email'], password=email['password'])
            sleep(5)
        with allure.step("登出"):
            UiFunction.logout()
            sleep(3)

