from Function.ui_function import *
from Function.api_function import *
import allure


class TestPortfolioUi:

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
            headers['X-Currency'] = 'EUR'
        with allure.step("首页获得数字货币报价"):
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
        headers['X-Currency'] = 'USD'
        with allure.step("检查BTC报价"):
            check('{} {}\n€{}'.format('BTC', get_ui_text('CB347'), quote['BTC']), type=1)
        with allure.step("检查ETH报价"):
            check('{} {}\n€{}'.format('ETH', get_ui_text('CB347'), quote['ETH']), type=1)

    @allure.testcase('test_pl_ui_004 USD显示下确认total asset value金额')
    def test_portfolio_ui_004(self):
        with allure.step("修改以美元为单位显示货币金额"):
            UiFunction.choose_display_currency()
        with allure.step("查询钱包所有币种详细金额以及报价，以美元价格返回"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            abs_amount = r.json()['summary']['abs_amount']
        with allure.step("校验"):
            assert add_comma_number(abs_amount) in poco(get_ui_text('CB407')).parent().attr('name'), '总金额是{},页面显示是{}'.format(add_comma_number(abs_amount), poco(get_ui_text('CB407')).parent().attr('name'))

    @allure.testcase('test_pl_ui_005 EUR显示下确认total asset value金额')
    def test_portfolio_ui_005(self):
        with allure.step("修改以美元为单位显示货币金额"):
            UiFunction.choose_display_currency(type='EUR')
        with allure.step("查询钱包所有币种详细金额以及报价，以美元价格返回"):
            headers['X-Currency'] = 'EUR'
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            abs_amount = r.json()['summary']['abs_amount']
            headers['X-Currency'] = 'USD'
        with allure.step("校验"):
            assert add_comma_number(abs_amount) in poco(get_ui_text('CB407')).parent().attr('name'), '总金额是{},页面显示是{}'.format(add_comma_number(abs_amount), poco(get_ui_text('CB407')).parent().attr('name'))

    @allure.testcase('test_pl_ui_006 EUR显示下确认total asset value金额')
    def test_portfolio_ui_006(self):
        with allure.step("修改以美元为单位显示货币金额"):
            UiFunction.choose_display_currency(type='EUR')
        with allure.step("查询钱包所有币种详细金额以及报价，以美元价格返回"):
            headers['X-Currency'] = 'EUR'
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            abs_amount = r.json()['summary']['abs_amount']
            headers['X-Currency'] = 'USD'
        with allure.step("校验"):
            assert add_comma_number(abs_amount) in poco(get_ui_text('CB407')).parent().attr('name'), '总金额是{},页面显示是{}'.format(add_comma_number(abs_amount), poco(get_ui_text('CB407')).parent().attr('name'))

    @allure.testcase('test_pl_ui_007 检查投资分布情况')
    def test_portfolio_ui_007(self):
        with allure.step("点击View进入asset页面"):
            click('CB407')
        with allure.step("检查Asset页面元素"):
            check('CB031')
        with allure.step("查询每个币种当前资产市值"):
            sleep(5)
            r = session.request('GET', url='{}/assetstatapi/assetstat'.format(env_url), headers=headers)
            asset = r.json()['overview']
        with allure.step("校验数字货币占比的百分比"):
            for i in asset:
                check(i['percent'])
                check(i['code'])

    @allure.testcase('test_pl_ui_008 检查asset value')
    def test_portfolio_ui_008(self):
        with allure.step("点击View进入asset页面"):
            click('CB407')
        with allure.step("检查Asset value页面元素"):
            check('CB032')
        with allure.step("向上滑动"):
            slide('up')
        with allure.step("检查曲线可选择日期"):
            click('30d')
            click('90d')
            click('6M')
            click('1Y')
        with allure.step("检查显示买入卖出点"):
            check('CB180')
            check('CB181')

    @allure.testcase('test_pl_ui_009 检查首页p/l数据')
    def test_portfolio_ui_009(self):
        with allure.step("获取p/l数据"):
            with allure.step("进入首页"):
                click('CB214')
                sleep(2)
            r = session.request('GET', url='{}/assetstatapi/asset_pl_detail'.format(env_url), headers=headers)
            holding_percent = r.json()['profit_loss_overview']['profit_loss_holding']['percent']
            today_percent = r.json()['profit_loss_overview']['profit_loss_today']['percent']
        with allure.step("检查首页数据"):
            poco(holding_percent).click()
