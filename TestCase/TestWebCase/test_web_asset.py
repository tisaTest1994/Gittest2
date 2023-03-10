import time

from Function.web_function import *
from Function.web_common_function import *
from Function.api_common_function import *


@allure.feature("web ui asset 相关 testcases")
class TestWebAssetApi:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency

    def teardown_method(self):
        pass

    @allure.title('test_web_asset_001')
    @allure.description('查询Total Asset Value')
    def test_web_asset_001(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("通过api获得Total Asset Value数据"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            abs_amount = r.json()['summary']['abs_amount']
        with allure.step("通过页面获得Total Asset Value数据"):
            page_abs_amount = operate_element_web(chrome_driver, 'assetPage', 'assets-overview-amount', 'get_text')
        assert add_currency_symbol(str(abs_amount), currency=self.currency, is_symbol=True) == str(page_abs_amount), "Total Asset Value后端接口返回{},页面上显示{}".format(abs_amount, page_abs_amount)

    @allure.title('test_web_asset_002')
    @allure.description('查询Total Balance Value')
    def test_web_asset_002(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("通过api获得Total Balance Value数据"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            balance_list = r.json()['assets']
            for i in balance_list:
                if i['type'] == 'BALANCE':
                    abs_amount = i['abs_amount']
        with allure.step("通过页面获得Total Balance Value数据"):
            page_abs_amount = operate_element_web(chrome_driver, 'assetPage', 'assets-balance-amount', 'get_text')
        assert add_currency_symbol(str(abs_amount), currency=self.currency, is_symbol=True) == str(page_abs_amount), "Total Balance Value后端接口返回{},页面上显示{}".format(abs_amount, page_abs_amount)

    @allure.title('test_web_asset_003')
    @allure.description('检查每个币种balance的分类金额')
    def test_web_asset_003(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("通过页面获得Total Balance Value数据"):
            balance_list = ['assets-blance-table-row-0', 'assets-blance-table-row-1', 'assets-blance-table-row-2', 'assets-blance-table-row-3', 'assets-blance-table-row-4']
            for i in balance_list:
                balance_dict = {}
                a = chrome_driver.find_element_by_id(i).text.split('\n')
                balance_dict[a[0]] = a[1].split(' ')
                currency_type = list(balance_dict.keys())[0]
                time.sleep(2)
                with allure.step("通过API获得Available Balance数据"):
                    available_balance = ApiFunction.get_crypto_number(type=currency_type, balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
                with allure.step("判断API获得的Available Balance数据和页面显示的一致"):
                    assert str(balance_dict[currency_type][1]) == add_currency_symbol(str(available_balance), currency=self.currency), "币种：{}，API获得Available Balance是{},页面上的Available Balance是{}".format(a[0], available_balance, balance_dict[currency_type][1])
                with allure.step("通过API获得Frozen Balance数据"):
                    frozen_balance = ApiFunction.get_crypto_number(type=currency_type, balance_type='BALANCE_TYPE_FROZEN', wallet_type='BALANCE')
                with allure.step("判断API获得的Frozen Balance数据和页面显示的一致"):
                    assert str(balance_dict[currency_type][2]) == add_currency_symbol(str(frozen_balance), currency=self.currency), "币种：{}，API获得Frozen Balance是{},页面上的Frozen Balance是{}".format(a[0], frozen_balance, balance_dict[currency_type][2])
                with allure.step("通过API获得Total Balance数据"):
                    total_balance = Decimal(available_balance) + Decimal(frozen_balance)
                with allure.step("判断API获得的Total Balance数据和页面显示的一致"):
                    assert str(balance_dict[currency_type][0]) == add_currency_symbol(str(total_balance), currency=self.currency), "币种：{}，API获得Total Balance是{},页面上的Total Balance是{}".format(a[0], total_balance, balance_dict[currency_type][0])

    @allure.title('test_web_asset_004')
    @allure.description('查询Total Saving Amount')
    def test_web_asset_004(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("通过api获得Total Saving Amount数据"):
            r = session.request('GET', url='{}/earn/products/summary'.format(env_url), headers=headers)
        with allure.step("通过页面获得Total Asset Value数据"):
            page_abs_amount = operate_element_web(chrome_driver, 'assetPage', 'assets-earn-amount', 'get_text')
        assert add_currency_symbol(str(r.json()['total_holding']), currency=self.currency, is_symbol=True) == str(page_abs_amount), "Total Saving Amount后端接口返回{},页面上显示{}".format(str(r.json()['total_holding']), page_abs_amount)

    @allure.title('test_web_asset_005')
    @allure.description('查询flexible Savings数据')
    def test_web_asset_005(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击flexible Savings Button"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_savingstype_Flexible')
        with allure.step("通过页面获得flexible Savings数据"):
            flexible_list = ['assets-flexiable-table-row-0', 'assets-flexiable-table-row-1', 'assets-flexiable-table-row-2']
            for i in flexible_list:
                flexible_dict = {}
                a = chrome_driver.find_element_by_id(i).text.split('\n')
                flexible_dict[a[0]] = a[1].split(' ')
                currency_type = list(flexible_dict.keys())[0]
                with allure.step("通过API获得flexible Savings数据"):
                    r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
                    for y in r.json():
                        if y['code'] == currency_type:
                            with allure.step("验证7d apy"):
                                assert str(y['apy_7d']) + '%' == flexible_dict[currency_type][0], 'API获得的7天平均利息是{},Page获得的7天平均利息是{}'.format(str(y['apy_7d']) + '%', flexible_dict[currency_type][0])
                            r = session.request('GET', url='{}/earn/products/{}/summary'.format(env_url, y['product_id']), headers=headers)
                            with allure.step("验证Saving Amount"):
                                assert add_currency_symbol(r.json()['total_holding']['amount'], currency=currency_type) == flexible_dict[currency_type][1], 'API获得的Saving Amount是{},Page获得的Saving Amount是{}'.format(r.json()['total_holding']['amount'], flexible_dict[currency_type][1])
                            with allure.step("验证Accruing Amount"):
                                assert add_currency_symbol(r.json()['accruing_amount']['amount'], currency=currency_type) == flexible_dict[currency_type][2], 'API获得的Accruing Amount是{},Page获得的Accruing Amount是{}'.format(r.json()['accruing_amount']['amount'], flexible_dict[currency_type][2])
                            with allure.step("验证Yesterday Interest"):
                                if r.json()['today_yield']['amount'] == '-1':
                                    assert flexible_dict[currency_type][3] == '--', 'Page获得的Yesterday Interest是{}'.format(flexible_dict[currency_type][3])
                                else:
                                    assert add_currency_symbol(r.json()['today_yield']['amount'], currency=currency_type) == flexible_dict[currency_type][3], 'API获得的Yesterday Interest是{},Page获得的Yesterday Interest是{}'.format(r.json()['today_yield']['amount'], flexible_dict[currency_type][3])
                            with allure.step("验证Subscribe Today"):
                                assert add_currency_symbol(r.json()['subscribing_amount']['amount'], currency=currency_type) == flexible_dict[currency_type][4], 'API获得的Subscribe Today是{},Page获得的Subscribe Today是{}'.format(r.json()['subscribing_amount']['amount'], flexible_dict[currency_type][4])
                            with allure.step("验证Redeeming"):
                                assert add_currency_symbol(r.json()['redeeming_amount']['amount'], currency=currency_type) == flexible_dict[currency_type][5], 'API获得的Redeeming是{},Page获得的Redeeming是{}'.format(r.json()['redeeming_amount']['amount'], flexible_dict[currency_type][5])

    # @allure.title('test_web_asset_006 查询flexible Savings数据')
    # def test_web_asset_006(self):
    #     with allure.step("点击Fixed Savings"):
    #         operate_element(chrome_driver, 'assetPage', 'simple-tab-1')
    #         print(get_element_text(chrome_driver, 'assetPage', 'assets-fixed-table'))