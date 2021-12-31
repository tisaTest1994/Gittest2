from Function.web_function import *
from Function.api_function import *


class TestCassApi:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()
        self.driver = webFunction.launch_web(self.web_url)
        webFunction.login_web(self.driver)

    def teardown_method(self):
        webFunction.logout_web(self.driver)
        self.driver.close()

    @allure.testcase('test_web_asset_001 查询Total Asset Value')
    def test_web_asset_001(self):
        with allure.step("通过api获得Total Asset Value数据"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            abs_amount = r.json()['summary']['abs_amount']
        with allure.step("通过页面获得Total Asset Value数据"):
            page_abs_amount = get_element_text(self.driver, 'assetPage', 'assets-overview-amount')
        assert '$' + str(abs_amount) == str(page_abs_amount), "Total Asset Value后端接口返回{},页面上显示{}".format(abs_amount, page_abs_amount)

    @allure.testcase('test_web_asset_002 查询Total Balance Value')
    def test_web_asset_002(self):
        with allure.step("通过api获得Total Balance Value数据"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            balance_list = r.json()['assets']
            for i in balance_list:
                if i['type'] == 'BALANCE':
                    abs_amount = i['abs_amount']
        with allure.step("通过页面获得Total Balance Value数据"):
            page_abs_amount = get_element_text(self.driver, 'assetPage', 'assets-balance-amount')
        assert '$' + str(abs_amount) == str(page_abs_amount), "Total Balance Value后端接口返回{},页面上显示{}".format(abs_amount, page_abs_amount)

    @allure.testcase('test_web_asset_003 检查每个币种balance的分类金额')
    def test_web_asset_003(self):
        with allure.step("通过页面获得Total Balance Value数据"):
            balance_list = ['assets-blance-table-row-0', 'assets-blance-table-row-1', 'assets-blance-table-row-2', 'assets-blance-table-row-3', 'assets-blance-table-row-4']
            for i in balance_list:
                balance_dict = {}
                a = self.driver.find_element_by_id(i).text.split('\n')
                balance_dict[a[0]] = a[1].split(' ')
                currency_type = list(balance_dict.keys())[0]
                with allure.step("通过API获得Available Balance数据"):
                    available_balance = ApiFunction.get_crypto_number(type=currency_type, balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
                with allure.step("判断API获得的Available Balance数据和页面显示的一致"):
                    assert str(available_balance) == str(balance_dict[currency_type][1]), "API获得Available Balance是{},页面上的Available Balance是{}".format(available_balance, balance_dict[currency_type][1])
                with allure.step("通过API获得Frozen Balance数据"):
                    frozen_balance = ApiFunction.get_crypto_number(type=currency_type, balance_type='BALANCE_TYPE_FROZEN', wallet_type='BALANCE')
                with allure.step("判断API获得的Frozen Balance数据和页面显示的一致"):
                    assert str(frozen_balance) == str(balance_dict[currency_type][2]), "API获得Frozen Balance是{},页面上的Frozen Balance是{}".format(frozen_balance, balance_dict[currency_type][2])
                with allure.step("通过API获得Total Balance数据"):
                    total_balance = Decimal(available_balance) + Decimal(frozen_balance)
                with allure.step("判断API获得的Total Balance数据和页面显示的一致"):
                    page_total_balance = Decimal(balance_dict[currency_type][1]) + Decimal(balance_dict[currency_type][2])
                    assert str(total_balance) == str(page_total_balance), "API获得Total Balance是{},页面上的Total Balance是{}".format(total_balance, page_total_balance)

    @allure.testcase('test_web_asset_004 查询Total Saving Amount')
    def test_web_asset_004(self):
        with allure.step("通过api获得Total Saving Amount数据"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            balance_list = r.json()['assets']
            for i in balance_list:
                if i['type'] == 'SAVING':
                    saving_amount = i['abs_amount']
                elif i['type'] == 'SAVING-FIX':
                    saving_fix_amount = i['abs_amount']
            abs_amount = Decimal(saving_amount) + Decimal(saving_fix_amount)
        with allure.step("通过页面获得Total Asset Value数据"):
            page_abs_amount = get_element_text(self.driver, 'assetPage', 'assets-earn-amount')
        assert '$' + str(abs_amount) == str(page_abs_amount), "Total Saving Amount后端接口返回{},页面上显示{}".format(abs_amount, page_abs_amount)

    @allure.testcase('test_web_asset_005 查询flexible Savings数据')
    def test_web_asset_005(self):
        with allure.step("通过页面获得flexible Savings数据"):
            flexible_list = ['assets-flexiable-table-row-0', 'assets-flexiable-table-row-1', 'assets-flexiable-table-row-2']
            for i in flexible_list:
                flexible_dict = {}
                a = self.driver.find_element_by_id(i).text.split('\n')
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
                                assert r.json()['total_holding']['amount'] == flexible_dict[currency_type][1], 'API获得的Saving Amount是{},Page获得的Saving Amount是{}'.format(r.json()['total_holding']['amount'], flexible_dict[currency_type][1])
                            with allure.step("验证Accruing Amount"):
                                assert r.json()['accruing_amount']['amount'] == flexible_dict[currency_type][2], 'API获得的Accruing Amount是{},Page获得的Accruing Amount是{}'.format(r.json()['accruing_amount']['amount'], flexible_dict[currency_type][2])
                            with allure.step("验证Yesterday Interest"):
                                assert r.json()['today_yield']['amount'] == flexible_dict[currency_type][3], 'API获得的Yesterday Interest是{},Page获得的Yesterday Interest是{}'.format(r.json()['today_yield']['amount'], flexible_dict[currency_type][3])
                            with allure.step("验证Subscribe Today"):
                                assert r.json()['subscribing_amount']['amount'] == flexible_dict[currency_type][4], 'API获得的Subscribe Today是{},Page获得的Subscribe Today是{}'.format(r.json()['subscribing_amount']['amount'], flexible_dict[currency_type][4])
                            with allure.step("验证Redeeming"):
                                assert r.json()['redeeming_amount']['amount'] == flexible_dict[currency_type][5], 'API获得的Redeeming是{},Page获得的Redeeming是{}'.format(r.json()['redeeming_amount']['amount'], flexible_dict[currency_type][5])





