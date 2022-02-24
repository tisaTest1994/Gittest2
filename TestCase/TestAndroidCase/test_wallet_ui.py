from Function.ui_function import *
import allure
from Function.api_common_function import *
from TestCase.TestApiCase.test_asset import *
from Function.ui_function import *
import datetime


class TestWalletUi:

    def setup_method(self):
        with allure.step("打开 app"):
            start_app(package_name)
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    def teardown(self):
        with allure.step("关闭 app"):
            stop_app(package_name)

    @allure.title('test_account_001')
    @allure.description('使用已经注册账户登录，登录进入主页后退出')
    def test_account_001(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
            sleep(5)
            assert False, '123'
        with allure.step("登出"):
            UiFunction.logout()
            sleep(3)

    @allure.title('test_wallet_001')
    @allure.description('wallet页面验证 Total Balance')
    def test_wallet_001(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        operate_element_app('walletPage', 'Wallet', 'click')
        sleep(2)
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency
        with allure.step("通过api获得Total Balance数据"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            print(r.json())
            balance_list = r.json()['assets']
            print(balance_list)
            for i in balance_list:
                if i['type'] == 'BALANCE':
                    abs_amount = i['abs_amount']
                    print(abs_amount)
            total_balance_value_page = add_currency_symbol(abs_amount, currency=self.currency, is_symbol=True)
            print(total_balance_value_page)
            assert operate_element_app('walletPage', total_balance_value_page, 'check') is True, 'total_balance_value_page在页面的值是{}'.format(total_balance_value_page)


