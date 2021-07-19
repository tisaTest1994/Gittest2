from run import *
from Function.ui_function import *
import allure


class TestAccountUiCase:

    # 每个cases前执行
    def setup(self):
        # 打开 app
        start_app("com.cabital.cabital.debug")
        sleep(20)

    # 每个cases结束后
    def teardown(self):
        stop_app("com.cabital.cabital.debug")
        sleep(2)

    @allure.testcase('test_account_001 使用已经注册账户登录，登录进入主页后退出')
    def test_account_001(self):
        with allure.step("登录"):
            UiFunction.login(account=email['email'], password=email['password'])
            sleep(20)

