from Function.ui_function import *
from Function.api_function import *
import allure


class TestConvertUi:

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

    @allure.testcase('test_convert_ui_001 换汇页面显示sell币种的可用余额')
    def test_convert_ui_001(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("Api获得币种可用Balance"):
            number = AccountFunction.get_crypto_number(type='BTC', balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
        with allure.step("验证页面显示sell币种可用的Balance"):
            check("{} {} BTC".format(get_json(file='multiple_languages.json')['CB036'], number))

    @allure.testcase('test_convert_ui_001 换汇页面点击MAX')
    def test_convert_ui_001(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("换汇页面点击MAX"):
            click("CB177")
        with allure.step("Api获得币种可用Balance"):
            number = AccountFunction.get_crypto_number(type='BTC', balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
        with allure.step("验证换汇页面点击MAX"):
            print(poco('{}, 0.0002'.format(number)).exists())
            check('{}, 0.0002'.format(number))



