from Function.web_function import *
from Function.api_function import *


class TestWebTransactionApi:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()
        self.driver = webFunction.launch_web(self.web_url)
        webFunction.login_web(self.driver)
        operate_element(self.driver, 'assetPage', 'header-desktop-menu-item-CB284')

    def teardown_method(self):
        webFunction.logout_web(self.driver)
        self.driver.close()

    @allure.title('test_web_transaction_001 查看单独币种的交易记录')
    def test_web_transaction_001(self):
        for i in ApiFunction.balance_list():
            with allure.step("通过api获得某个币种的交易记录"):
                data = {
                    "pagination_request": {
                        "page_no": 1,
                        "page_size": 20
                    },
                    "user_txn_sub_types": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                    "statuses": [1, 2, 3, 4],
                    "codes": [i]
                }
                with allure.step("查询特定条件的交易"):
                    r = session.request('POST', url='{}/txn/query/web'.format(env_url), data=json.dumps(data),
                                        headers=headers)
                    transaction_info_api = r.json()['transactions'][0]
                    print(transaction_info_api)
            with allure.step("通过页面获得某个币种的交易记录"):
                with allure.step("清除搜索记录"):
                    operate_element(self.driver, 'transactionPage', 'transaction-filter-currency', type='clear')
                with allure.step("搜索特定币种"):
                    operate_element(self.driver, 'transactionPage', 'transaction-filter-currency', type='input', input=i)
                    sleep(1)
                with allure.step("点击指定币种"):
                    operate_element(self.driver, 'transactionPage', 'undefined-option-item-{}'.format(i))
                sleep(10)

    @allure.title('test_web_transaction_002 查看某交易类型的交易记录')
    def test_web_transaction_002(self):
        for i in get_json()['transaction_type'].keys():
            with allure.step("通过api获得某个币种的交易记录"):
                data = {
                    "pagination_request": {
                        "page_no": 1,
                        "page_size": 20
                    },
                    "user_txn_sub_types": [int(i)],
                    "statuses": [1, 2, 3, 4],
                    "codes": []
                }
                with allure.step("查询特定条件的交易"):
                    r = session.request('POST', url='{}/txn/query/web'.format(env_url), data=json.dumps(data),
                                        headers=headers)
                    if r.json()['transactions'] != []:
                        transaction_info_api = r.json()['transactions'][0]
                        print(transaction_info_api)
                        with allure.step("通过页面获得某个币种的交易记录"):
                            with allure.step("清除搜索记录"):
                                operate_element(self.driver, 'transactionPage', 'transaction-filter-types', type='delete')
                            with allure.step("搜索特定币种"):
                                operate_element(self.driver, 'transactionPage', 'transaction-filter-types', type='input', input="undefined-option-CB307-2")
                                sleep(1)
                            with allure.step("点击指定币种"):
                                operate_element(self.driver, 'transactionPage', 'undefined-option-item-{}'.format(i))
                            sleep(10)