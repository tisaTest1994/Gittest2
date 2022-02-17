from Function.web_function import *
from Function.web_common_function import *
from Function.api_common_function import *


@allure.feature("web ui transactions 相关 testcases")
class TestWebWithdraw:
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

    @allure.title('test_web_transactions_001')
    @allure.description('币种切换')
    def test_transactions_001(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("切换至transactions页面"):
            operate_element_web(chrome_driver, 'transactionPage', 'mainpage_menu_transaction')
        with allure.step("切换至BTC·,并检查页面显示"):
            operate_element_web(chrome_driver, 'transactionPage', 'transaction-filter-currency-drop-btn-up')
            operate_element_web(chrome_driver, 'transactionPage', 'transaction-filter-currency-option-item-BTC')
            # 判断是否有数据
            if operate_element_web(chrome_driver, 'transactionPage', 'transaction-table-row-0', 'check') is False:
                pass
            else:
                chrome_driver.find_element_by_xpath('//*[@id="transaction-table-row-0"]/td/span').text
