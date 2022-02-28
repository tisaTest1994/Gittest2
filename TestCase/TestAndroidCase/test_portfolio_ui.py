from Function.ui_function import *
import allure
from Function.api_common_function import *
from Function.ui_common_function import *
from TestCase.TestApiCase.test_asset import *
import datetime


class TestPortfolioUi:

    def setup_method(self):
        with allure.step("打开 app"):
            start_app(package_name)
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    def teardown(self):
        with allure.step("关闭 app"):
            stop_app(package_name)


    @allure.title('test_Portfolio_001')
    @allure.description('portfolio 页面验证 total asset value')
    def test_portfolio_001(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency
        with allure.step("通过API 获取Total Asset value"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            total_asset_value = r.json()['summary']['abs_amount']
            total_asset_value_page = add_currency_symbol(total_asset_value, self.currency, True)
            assert operate_element_app('portfolioPage', total_asset_value_page, 'check') is True, 'total_asset_value_page在页面的值是{}'.format(total_asset_value_page)

    @allure.title('test_Portfolio_002')
    @allure.description('portfolio 页面跳转进Asset Overview验证total asset value')
    def test_portfolio_002(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency
        with allure.step("通过API 获取BTC的百分比"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            print(r.json())
            total_asset_value = r.json()['summary']['abs_amount']
            print('total_asset_value：{}'.format(total_asset_value))
            total_asset_value_page = add_currency_symbol(total_asset_value, self.currency, True)
            print('total_asset_value_page：{}'.format(total_asset_value_page))
            print(operate_element_app('portfolioPage', total_asset_value_page, 'check'))
        with allure.step("点击Details"):
            operate_element_app('portfolioPage', 'Details', 'click')
            assert operate_element_app('portfolioPage', 'Asset Allocation', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('portfolioPage', 'Asset Allocation')
            assert operate_element_app('portfolioPage', total_asset_value_page, 'check') is True, 'total asset value在页面的值是{}'.format(total_asset_value_page)

    @allure.title('test_Portfolio_003')
    @allure.description('portfolio 页面跳转进Asset Overview验证5种币种的占比')
    def test_portfolio_003(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("Details"):
            operate_element_app('portfolioPage', 'Details', 'click')
        assert operate_element_app('portfolioPage', 'Asset Allocation', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('portfolioPage', 'Asset Allocation')
        with allure.step("通过API 获取6个币种的百分比"):
            r = session.request('GET', url='{}/assetstatapi/assetstat'.format(env_url), headers=headers)
            print(r.json())
            overview = r.json()['overview']
            for i in overview:
                code = i['code']
                percent = i['percent']
                print(code, percent)
                assert operate_element_app('portfolioPage', code, 'check') is True, 'code在页面的值是{}'.format(code)
                assert operate_element_app('portfolioPage', percent, 'check') is True, 'percent在页面的值是{}'.format(percent)

    @allure.title('test_Portfolio_004')
    @allure.description('portfolio 页面通过Details跳转进查看昨天Asset Value值')
    def test_portfolio_004(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("点击Details"):
            operate_element_app('portfolioPage', 'Details', 'click')
        assert operate_element_app('portfolioPage', 'Asset Allocation', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('portfolioPage', 'Asset Allocation')
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency
        with allure.step("通过API 获取Asset Value初始值"):
            r = session.request('GET', url='{}/assetstatapi/assetstat'.format(env_url), headers=headers)
            total_asset_value = r.json()['history'][0]['total_value']
            total_asset_value_page = add_currency_symbol(total_asset_value, currency=self.currency, is_symbol=True)
            print(total_asset_value_page)
            assert operate_element_app('portfolioPage', total_asset_value_page, 'check') is True, 'total asset value在页面的值是{}'.format(total_asset_value_page)
        history = r.json()['history']
        print(history)
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        print(yesterday)
        for i in history:
            date1 = i['date'].split()[0]
            print(date1)
            if date1 == str(yesterday):
                total_value= add_currency_symbol(i['total_value'], currency=self.currency, is_symbol=True)
                print('date1的值是：{}'.format(date1))
                print('total_value的值是：{}'.format(total_value))
                #要看下是不是能单独断言检查日期，因为现在运行是失败的False！=True
                assert operate_element_app('portfolioPage', date1, 'check') is True, 'date1在页面的值是{}'.format(date1)
                assert operate_element_app('portfolioPage', total_value, 'check') is True, 'total_value在页面的值是{}'.format(total_value)
            else:
                return 'yesterday该元素不等于昨天日期'

    @allure.title('test_Portfolio_005')
    @allure.description('portfolio 页面验证Portfolio页面Crypto Holdings和Cash Holdings3个数值')
    def test_portfolio_005(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = 'self.currency'
        with allure.step("通过Api获取Profolio页面Crypto Holdings"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            total_holding_value = r.json()['wallets']
            for i in total_holding_value:
                code = i['code']
                amount = i['amount']
                abs_amount = i['abs_amount']
                abs_amount = add_currency_symbol(abs_amount, currency=self.currency, is_symbol=True)
        with allure.step("向上滑动"):
            slide('up', cycle=3)
        with allure.step("向上滑动"):
            print(poco(textMatches='BTC.*').get_text())


























