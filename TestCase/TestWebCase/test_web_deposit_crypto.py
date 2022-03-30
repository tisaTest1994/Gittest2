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
            assert operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_Deposit Cash', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至deposit crypto"):
            sleep(2)
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_Deposit Crypto')
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

    @allure.title('test_web_deposit_crypto_002')
    @allure.description('Deposit信息检查（crypto）')
    def test_deposit_crypto_002(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击deposit按钮，并判断是否跳转至deposit页面,默认为deposit Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_deposit')
            assert operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_Deposit Cash', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至deposit Crypto"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_Deposit Crypto')
        with allure.step("从metadata接口获取已开启的币种信息"):
            currency_metadata = session.request('GET', url='{}/core/metadata'.format(env_url), headers=headers)
            currency_list_metadata = currency_metadata.json()['currencies']
            currency_all_metadata = currency_list_metadata.keys()
        with allure.step("从接口获取币种信息,如在metada中关闭，则去除"):
            crypto = session.request('GET', url='{}/pay/deposit/ccy/crypto'.format(env_url), headers=headers)
            crypto_list = crypto.json()['crypto']
            crypto_all = []
            for i in range(0, len(crypto_list)):
                if crypto_list[i]['name'] in currency_all_metadata:
                    crypto_all.append(crypto_list[i]['name'])
        with allure.step("从接口获取Deposit信息并验证正确性"):
            for j in range(0, len(crypto_all)):
                with allure.step("切换币种"):
                    print(crypto_all[j])
                    operate_element_web(chrome_driver, 'assetPage', 'assets-deposit-cash-drop-btn-up')
                    operate_element_web(chrome_driver, 'assetPage', 'undefined-option-{}'.format(crypto_all[j]))
                with allure.step("从接口获取Deposit信息"):
                    r = session.request('GET',
                                        url='{}/pay/deposit/addresses?code={}'.format(env_url, crypto_all[j]),
                                        headers=headers)
                    deposit_info = r.json()[0]
                    address = deposit_info['address']
                with allure.step("判断信息是否在页面上显示"):
                    assert operate_element_web(chrome_driver, '', address,
                                               'check'), '当前币种是{}, {}显示的信息与接口返回信息不符'.format(crypto_all[j],
                                                                                            address)

