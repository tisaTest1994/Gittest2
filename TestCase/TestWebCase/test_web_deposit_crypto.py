from Function.web_function import *
from Function.web_common_function import *
from Function.api_common_function import *


@allure.feature("web ui deposit crypto 相关 testcases")
class TestWebDeposit:
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

    @allure.title('test_web_deposit_crypto_001')
    @allure.description('select deposit currency')
    def test_deposit_crypto_001(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击deposit按钮，并判断是否跳转至deposit页面,默认为deposit Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_deposit')
            assert operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_CB578', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至deposit crypto"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_CB067')
            assert operate_element_web(chrome_driver, '', 'Select deposit currency', 'check'),\
                '未切换至deposit crypto'
            time.sleep(1)
        with allure.step("检查默认币种"):
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash', 'get_value') ==\
                   'BTC', "默认币种错误"
        with allure.step("切换至ETH，并检查对应network"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
            # 选择ETH
            operate_element_web(chrome_driver, 'assetPage', 'undefined-option-ETH')
            time.sleep(2)
            assert chrome_driver.find_element_by_xpath('//div/img[@src="../images/coin/ETH.png"]'), '币种未切换至ETH'
            # 检查network是否正确
            assert operate_element_web(chrome_driver, 'assetPage', 'crypto-payment-method', 'get_value') == 'ERC20',\
                'network错误'
        with allure.step("切换至USDT，并检查对应network"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
            # 选择USDT
            operate_element_web(chrome_driver, 'assetPage', 'undefined-option-USDT')
            time.sleep(2)
            assert chrome_driver.find_element_by_xpath('//div/img[@src="../images/coin/USDT.png"]'), '币种未切换至USDT'
            # 检查network是否正确
            assert operate_element_web(chrome_driver, 'assetPage', 'crypto-payment-method', 'get_value') == 'ERC20',\
                'network错误'
        with allure.step("切换至BTC，并检查对应network"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
            # 选择BTC
            operate_element_web(chrome_driver, 'assetPage', 'undefined-option-BTC')
            time.sleep(2)
            assert chrome_driver.find_element_by_xpath('//div/img[@src="../images/coin/BTC.png"]'), '币种未切换至BTC'
            # 检查network是否正确
            assert operate_element_web(chrome_driver, 'assetPage', 'crypto-payment-method', 'get_value') == 'BTC', 'network错误'
