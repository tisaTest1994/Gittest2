from Function.ui_function import *
from Function.api_function import *
import allure


class TestPortfolioUi:

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

    @allure.testcase('test_pl_ui_001 隐藏页面金额')
    def test_portfolio_ui_001(self):
        with allure.step("修改以美元为单位显示货币金额"):
            UiFunction.choose_display_currency()
        with allure.step('确认保护显示金额关闭状态'):
            if exists(Template("{}/portfolio_eyes_close.png".format(get_photo()))) is False:
                touch(Template("{}/portfolio_eyes_close.png".format(get_photo())))
        with allure.step('关闭显示金额状态'):
            touch(Template("{}/portfolio_eyes_open.png".format(get_photo())))
        with allure.step('检查*号'):
            check('{}\n{}\nGet started\nCrypto'.format(get_ui_text('CB277'), '******'))

    @allure.testcase('test_pl_ui_002 确认首页USD显示报价')
    def test_portfolio_ui_002(self):
        with allure.step("修改以美元为单位显示货币金额"):
            UiFunction.choose_display_currency()
        with allure.step("首页获得数字货币报价"):
            headers['X-Currency'] = 'USD'
            params = {
                'codes': 'BTC,ETH'
            }
            r = requests.request('GET', url='{}/marketstat/public/tickers'.format(env_url), params=params, headers=headers)
            quote = {}
            for i in r.json():
                if i['code'] == 'BTC':
                    quote['BTC'] = i['abs_amount']
                elif i['code'] == 'ETH':
                    quote['ETH'] = i['abs_amount']
        with allure.step("检查BTC报价"):
            check('{} {}\n${}'.format('BTC', get_ui_text('CB347'), quote['BTC']), type=1)
        with allure.step("检查ETH报价"):
            check('{} {}\n${}'.format('ETH', get_ui_text('CB347'), quote['ETH']), type=1)

    @allure.testcase('test_pl_ui_003 确认首页EUR显示报价')
    def test_portfolio_ui_003(self):
        with allure.step("修改以欧元为单位显示货币金额"):
            UiFunction.choose_display_currency(type='EUR')
        with allure.step("首页获得数字货币报价"):
            headers['X-Currency'] = 'EUR'
            params = {
                'codes': 'BTC,ETH'
            }
            r = requests.request('GET', url='{}/marketstat/public/tickers'.format(env_url), params=params, headers=headers)
            quote = {}
            for i in r.json():
                if i['code'] == 'BTC':
                    quote['BTC'] = i['abs_amount']
                elif i['code'] == 'ETH':
                    quote['ETH'] = i['abs_amount']
        with allure.step("检查BTC报价"):
            check('{} {}\n€{}'.format('BTC', get_ui_text('CB347'), quote['BTC']), type=1)
        with allure.step("检查ETH报价"):
            check('{} {}\n€{}'.format('ETH', get_ui_text('CB347'), quote['ETH']), type=1)
