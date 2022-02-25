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


    @allure.title('test_wallet_001')
    @allure.description('wallet页面验证 Total Balance')
    def test_wallet_001(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        operate_element_app('walletPage', 'Wallet', 'click')
        sleep(1)
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency
        with allure.step("通过api获得Total Balance数据"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            balance_list = r.json()['assets']
            for i in balance_list:
                if i['type'] == 'BALANCE':
                    abs_amount = i['abs_amount']
            total_balance_value_page = add_currency_symbol(abs_amount, currency=self.currency, is_symbol=True)
            print(total_balance_value_page)
            assert operate_element_app('walletPage', total_balance_value_page, 'check') is False, 'total_balance_value_page在页面的值是{}'.format(total_balance_value_page)

    @allure.title('test_wallet_002')
    @allure.description('wallet页面验证 5个币种total Balance,Available,Processing')
    def test_wallet_002(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        operate_element_app('walletPage', 'Wallet', 'click')
        sleep(2)
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency
        with allure.step("通过api获得Available Processing Balance数据"):
            r = session.request('GET', url='{}/core/account/wallets?type=BALANCE'.format(env_url), headers=headers)
            balance_list = r.json()
            print(balance_list)
            balances1=[]
            list_code=['BTC', 'ETH', 'USDT', 'GBP', 'EUR', 'CHF']
            for i in balance_list:
                code = i['code']
                balances = i['balances']
                print(code)
                for j in balances:
                    if code in list_code:
                        balances = j['amount']
                        balances1.append(balances)
                print(balances1)
                total_balance = float(balances1[-1]) + float(balances1[-2])
                total_balance = float('%.8f' % total_balance)
                total_balance=add_comma_number(total_balance)
                print(total_balance)
                assert operate_element_app('walletPage', total_balance, 'check') is False, '{}total_balance在页面的值是{}不等于Available+Processing之和'.format(code, total_balance)

    @allure.title('test_wallet_003')
    @allure.description('wallet页面验证 5个币种total Balance,Available,Processing')
    def test_wallet_003(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("进入Wallet"):
            operate_element_app('walletPage', 'Wallet', 'click')
        sleep(1)
        with allure.step("进入Deposit"):
            operate_element_app('walletPage', 'Deposit', 'click')
            assert operate_element_app('walletPage', 'How would you like to deposit?', 'check') is True,'没有进入Deposit页面！'
        with allure.step("充值BTC"):
            operate_element_app('walletPage', 'I want to transfer in cryptocurrencies I am already holding.', 'click')
            assert operate_element_app('walletPage', 'Select Crypto', 'check') is True,'没有进入Deposit页面！'



