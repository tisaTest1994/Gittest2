from Function.ui_function import *
from Function.api_function import *
import allure


class TestPLUi:

    # 每个cases前执行
    def setup(self):
        # 打开 app
        start_app(package_name)
        # 登录 app
        UiFunction.login(account=email['email'], password=email['password'])

    # 每个cases结束后
    def teardown(self):
        # 关闭 app
        stop_app(package_name)

    @allure.testcase('test_pl_ui_001 查询所有交易信息')
    def test_pl_ui_001(self):
        with allure.step("进入首页"):
            click('CB214')
