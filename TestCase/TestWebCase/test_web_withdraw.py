from Function.web_function import *
from Function.web_common_function import *
from Function.api_common_function import *

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


    @allure.title('test_web_withdraw_001')
    @allure.description('select withdrawal currency')
    def test_withdraw_001(self, chrome_driver):
        account = get_json()['web'][get_json()['env']]['account']
        password = get_json()['web'][get_json()['env']]['password']
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'simple-tab-0', 'check'), '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("检查默认币种，并切换币种"):
            assert chrome_driver.find_element_by_xpath('//*[@src="../images/coin/EUR.png"]'), "默认币种错误"
            operate_element_web(chrome_driver, 'assetPage', '-drop-btn-up')
