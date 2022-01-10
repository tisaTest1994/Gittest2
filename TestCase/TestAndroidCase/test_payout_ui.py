from Function.ui_function import *
from Function.api_function import *
import allure


class TestPayOutUi:

    # 每个cases前执行
    def setup(self):
        # 打开 app
        start_app(package_name)
        # 登录 app
        UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])

    # 每个cases结束后
    def teardown(self):
        # 关闭 app
        stop_app(package_name)

    @allure.title('test_payout_001 测试iban账号')
    def test_payout_001(self):
        for i in get_json()['iban_list']:
            iban = i
        print(iban)



