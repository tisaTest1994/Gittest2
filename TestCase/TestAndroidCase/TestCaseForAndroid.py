from Function.UiFunction import *
import allure


class TestAccountUiCase:

    # 每个cases前执行
    def setup(self):
        # 打开 app
        stop_app("com.cabital.cabital_m")
        sleep(1)
        start_app("com.cabital.cabital_m")
        UiFunction.logout('')
        sleep(2)

    # 每个cases结束后
    def teardown(self):
        UiFunction.logout('')
        stop_app("com.cabital.cabital_m")
        sleep(2)

    @allure.testcase('test_account_001 使用已经注册账户登录，登录进入主页后退出')
    def test_account_001(self):
        #@allure.step()
        UiFunction.login(account='yuk3e@cabital.com', password='A!234sdfg')
        UiFunction.logout(account='yuk3e@cabital.com')

    @allure.testcase('test_account_002 使用错误密码登录')
    def test_account_001(self):
        UiFunction.login(account='yuk3e@cabital.com', password='1231441')
        print(1)
