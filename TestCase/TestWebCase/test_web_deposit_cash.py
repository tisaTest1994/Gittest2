import time

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

    @allure.title('test_web_deposit_cash_001')
    @allure.description('select deposit currency')
    def test_deposit_cash_001(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击deposit按钮，并判断是否跳转至deposit页面,默认为deposit Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_deposit')
            assert operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_CB578', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("检查默认币种，并切换币种"):
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash', 'get_value') ==\
                   'EUR', "默认币种错误"
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
            # 选择GBP
            operate_element_web(chrome_driver, 'assetPage', 'undefined-option-GBP-1')
            time.sleep(2)
            # 检查币种是否切换成功
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash', 'get_value') == \
                   'GBP', '币种未切换至GBP'
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
            # 选择EUR
            operate_element_web(chrome_driver, 'assetPage', 'undefined-option-EUR-0')
            time.sleep(2)
            # 检查币种是否切换成功
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash', 'get_value') ==\
                   'EUR', '币种未切换至EUR'
