from Function.web_function import *
from Function.web_common_function import *
from Function.api_common_function import *


@allure.feature("web ui withdraw crypto 相关 testcases")
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

    @allure.title('test_web_withdraw_crypto_001')
    @allure.description('select withdrawal currency并检查对应network')
    def test_withdraw_crypto_001(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            time.sleep(5)
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'), '页面切换失败'
        with allure.step("检查默认币种"):
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change',
                                       'get_value') == 'BTC', '默认币种显示错误'
        with allure.step("切换至ETH，并检查对应network"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
            # 选择ETH
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-ETH-1')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change',
                                       'get_value') == 'ETH', '币种切换失败'
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-method-radio0',
                                       'get_value') == 'ERC20', '错误'
        with allure.step("切换至USDT，并检查对应network"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
            # 选择USDT
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-USDT-2')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change',
                                       'get_value') == 'USDT', '币种切换失败'
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-method-radio0',
                                       'get_value') == 'ERC20', '错误'
        with allure.step("切换至BTC，并检查对应network"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
            # 选择BTC
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-BTC-0')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change',
                                       'get_value') == 'BTC', '币种切换失败'
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-method-radio0',
                                       'get_value') == 'BTC', '错误'

    @allure.title('test_web_withdraw_crypto_002')
    @allure.description('BTC:withdrawal address格式校验')
    def test_withdraw_crypto_002(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'), '页面切换失败'
        with allure.step("BTC withdrawal address格式校验：特殊字符"):
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input', '@')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input', '!')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input', '#')
            # 判断是是否输入成功
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'get_value') ==\
                   '', '错误：特殊字符输入成功'
        with allure.step("BTC withdrawal address格式校验：无效地址"):
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input', '123zxc')
            # 输入提现金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0.001')
            # 点击Next：Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'click_withdraw_confirm_crypto')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "amount": "0.001",
                    "code": "BTC",
                    "address": "123zxc",
                    "method": "BTC"
                }
                r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                    data=json.dumps(data1), headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("BTC withdrawal address格式校验：有效地址"):
            # 清空withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'delete')
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input',
                                'tb1qn8fymr49zljfkvgsuhg3572fnfkljuga550asm')
            # 点击Next：Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'click_withdraw_confirm_crypto')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailcode-label', 'check'),\
                '未弹出认证框'

    @allure.title('test_web_withdraw_crypto_003')
    @allure.description('ETH:withdrawal address格式校验')
    def test_withdraw_crypto_003(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'), '页面切换失败'
        with allure.step("切换至ETH"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
            # 选择ETH
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-ETH-1')
        with allure.step("ETH withdrawal address格式校验：无效地址"):
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input',
                                '1111111111111111111111111111111111111111')
            # 输入提现金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0.02')
            # 点击Next：Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'click_withdraw_confirm_crypto')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "amount": "0.02",
                    "code": "ETH",
                    "address": "1111111111111111111111111111111111111111",
                    "method": "ERC20"
                }
                r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                    data=json.dumps(data1), headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("ETH withdrawal address格式校验：有效地址"):
            # 清空withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'delete')
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input',
                                '0x0C5816f5a381209164861B57Ddd8B257a9fbC50a')
            # 点击Next：Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'click_withdraw_confirm_crypto')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailcode-label', 'check'),\
                '未弹出认证框'

    @allure.title('test_web_withdraw_crypto_004')
    @allure.description('USDT:withdrawal address格式校验')
    def test_withdraw_crypto_004(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'), '页面切换失败'
        with allure.step("切换至USDT"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
            # 选择USDT
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-USDT-2')
        with allure.step("USDT withdrawal address格式校验：无效地址"):
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input',
                                '1111111111111111111111111111111111111111')
            # 输入提现金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '40')
            # 点击Next：Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'click_withdraw_confirm_crypto')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "amount": "40",
                    "code": "USDT",
                    "address": "1111111111111111111111111111111111111111",
                    "method": "ERC20"
                }
                r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                    data=json.dumps(data1), headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("USDTwithdrawal address格式校验：有效地址"):
            # 清空withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'delete')
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input',
                                '0x0C5816f5a381209164861B57Ddd8B257a9fbC50a')
            # 点击Next：Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'click_withdraw_confirm_crypto')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailcode-label', 'check'),\
                '未弹出认证框'

    @allure.title('test_web_withdraw_crypto_005')
    @allure.description('BTC:withdrawal amount格式及限额校验')
    def test_withdraw_crypto_005(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'), '页面切换失败'
        with allure.step("输入的值小于最小提现金额<0.001"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0.0006')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount-helper-text',
                                       'get_text') == 'Minimum: 0.001', '最小限额提示信息未显示'
        with allure.step("输入的值大于最大可提现金额（available balance）"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '2000000')
            assert 'Insufficient Amount' in\
                   operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount-helper-text',
                                       'get_text'), '最大限额提示信息未显示'
        with allure.step("输入符合要求的提现金额"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0.001')
            assert 'Available Balance' in operate_element_web(chrome_driver, 'assetPage',
                                                              'assets-withdraw-crypto-amount-helper-text', 'get_text'),\
                '提示信息未显示错误'

    @allure.title('test_web_withdraw_crypto_006')
    @allure.description('ETH:withdrawal amount格式及限额校验')
    def test_withdraw_crypto_006(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'),\
                '页面切换失败'
        with allure.step("切换至ETH"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
            # 选择ETH
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-ETH-1')
        with allure.step("输入的值小于最小提现金额<0.02"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0.01')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount-helper-text',
                                       'get_text') == 'Minimum: 0.02', '最小限额提示信息未显示'
        with allure.step("输入的值大于最大可提现金额（available balance）"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '2000000')
            assert 'Insufficient Amount' in\
                   operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount-helper-text',
                                       'get_text'), '最大限额提示信息未显示'
        with allure.step("输入符合要求的提现金额"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0.02')
            assert 'Available Balance' in operate_element_web(chrome_driver, 'assetPage',
                                                              'assets-withdraw-crypto-amount-helper-text', 'get_text'),\
                '提示信息未显示错误'

    @allure.title('test_web_withdraw_crypto_007')
    @allure.description('USDT:withdrawal amount格式及限额校验')
    def test_withdraw_crypto_007(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'),\
                '页面切换失败'
        with allure.step("切换至USDT"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
            # 选择USDT
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-USDT-2')
        with allure.step("输入的值小于最小提现金额<40"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '39')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount-helper-text',
                                       'get_text') == 'Minimum: 40', '最小限额提示信息未显示'
        with allure.step("输入的值大于最大可提现金额（available balance）"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '2000000')
            assert 'Insufficient Amount' in\
                   operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount-helper-text',
                                       'get_text'), '最大限额提示信息未显示'
        with allure.step("输入符合要求的提现金额"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '40')
            assert 'Available Balance' in operate_element_web(chrome_driver, 'assetPage',
                                                              'assets-withdraw-crypto-amount-helper-text', 'get_text'),\
                '提示信息未显示错误'

    @allure.title('test_web_withdraw_crypto_008')
    @allure.description('withdrawal amount-Max')
    def test_withdraw_crypto_008(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'),\
                '页面切换失败'
        with allure.step("BTC：max"):
            with allure.step("获取可用金额数据"):
                available_balance_btc = operate_element_web(chrome_driver, 'assetPage',
                                                             'assets-withdraw-crypto-amount-helper-text', 'get_text')
                available_balance_btc = available_balance_btc.replace(
                    'Available Balance:', '').replace(' ', '').replace('BTC', '').replace(',', '')
                # 自动填入可提现的最大金额，金额和下方的available balance相同
            with allure.step("点击max按钮"):
                operate_element_web(chrome_driver, 'assetPage', 'withdraw_max_crypto')
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'get_value')\
                       == available_balance_btc, '未自动填入最大可提现金额'
        with allure.step("ETH：max"):
            with allure.step("切换至ETH"):
                # 点击下拉框
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
                # 选择ETH
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-ETH-1')
            with allure.step("获取可用金额数据"):
                available_balance_eth = operate_element_web(chrome_driver, 'assetPage',
                                                            'assets-withdraw-crypto-amount-helper-text', 'get_text')
                available_balance_eth = available_balance_eth.replace(
                    'Available Balance:', '').replace(' ', '').replace('ETH', '').replace(',', '')
                # 自动填入可提现的最大金额，金额和下方的available balance相同
            with allure.step("点击max按钮"):
                operate_element_web(chrome_driver, 'assetPage', 'withdraw_max_crypto')
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'get_value')\
                       == available_balance_eth, '未自动填入最大可提现金额'
        with allure.step("USDT：max"):
            with allure.step("切换至USDT"):
                # 点击下拉框
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
                # 选择ETH
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-USDT-2')
            with allure.step("获取可用金额数据"):
                available_balance_usdt = operate_element_web(chrome_driver, 'assetPage',
                                                             'assets-withdraw-crypto-amount-helper-text', 'get_text')
                print(available_balance_usdt)
                available_balance_usdt = available_balance_usdt.replace(
                    'Available Balance:', '').replace(' ', '').replace('USDT', '').replace(',', '')
                # 自动填入可提现的最大金额，金额和下方的available balance相同
            with allure.step("点击max按钮"):
                operate_element_web(chrome_driver, 'assetPage', 'withdraw_max_crypto')
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'get_value')\
                       == available_balance_usdt, '未自动填入最大可提现金额'

    @allure.title('test_web_withdraw_crypto_009')
    @allure.description('receive金额显示')
    def test_withdraw_crypto_009(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            time.sleep(2)
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'),\
                '页面切换失败'
        with allure.step("BTC:receive金额显示"):
            with allure.step("receive默认金额显示，用0调取显示fee"):
                withdrawal_fee = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-fee',
                                                     'get_text').replace(' ', '').replace('BTC', '')
                you_will_receive = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive',
                                                       'get_text').replace(' ', '').replace('BTC', '')
                assert float(withdrawal_fee) + 0 == float(you_will_receive), 'you_will_receive默认显示金额错误'
            with allure.step("检查金额是否正确且为千分位"):
                # 输入金额
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '1')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '1')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '5')
                you_will_receive2 = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive',
                                                        'get_text').replace(' ', '').replace('BTC', '')
                time.sleep(2)
                assert you_will_receive2[1] == ',', '金额未千分位显示'
                you_will_receive_string = you_will_receive2.replace(',', '')
                assert float(withdrawal_fee) + 1015 == float(you_will_receive_string), 'you_will_receive显示金额错误'
            with allure.step("输入框输入金额1005，显示receive后，清空输入框，检查receive金额是否更新"):
                # 清空输入框
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive', 'get_text')\
                       == '-0.0006 BTC', 'receive金额未更新'
        with allure.step("ETH:receive金额显示"):
            with allure.step("切换至ETH"):
                # 点击下拉框
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
                # 选择ETH
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-ETH-1')
            with allure.step("receive默认金额显示，用0调取显示fee"):
                withdrawal_fee = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-fee',
                                                     'get_text').replace(' ', '').replace('ETH', '')
                you_will_receive = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive',
                                                       'get_text').replace(' ', '').replace('ETH', '')
                assert float(withdrawal_fee) + 0 == float(you_will_receive), 'you_will_receive默认显示金额错误'
            with allure.step("检查金额是否正确且为千分位"):
                # 输入金额
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '1')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '1')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '5')
                you_will_receive2 = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive',
                                                        'get_text').replace(' ', '').replace('ETH', '')
                assert you_will_receive2[1] == ',', '金额未千分位显示'
                you_will_receive_string = you_will_receive2.replace(',', '')
                assert float(withdrawal_fee) + 1015 == float(you_will_receive_string), 'you_will_receive显示金额错误'
            with allure.step("输入框输入金额1005，显示receive后，清空输入框，检查receive金额是否更新"):
                # 清空输入框
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive', 'get_text') \
                       == '-0.004 ETH', 'receive金额未更新'
        with allure.step("USDT:receive金额显示"):
            with allure.step("切换至USDT"):
                # 点击下拉框
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-change-drop-btn-up')
                # 选择USDT
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector-option-USDT-2')
            with allure.step("receive默认金额显示，用0调取显示fee"):
                withdrawal_fee = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-fee',
                                                     'get_text').replace(' ', '').replace('USDT', '')
                you_will_receive = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive',
                                                       'get_text').replace(' ', '').replace('USDT', '')
                assert float(withdrawal_fee) + 0 == float(you_will_receive), 'you_will_receive默认显示金额错误'
            with allure.step("检查金额是否正确且为千分位"):
                # 输入金额
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '1')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '1')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '5')
                you_will_receive2 = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive',
                                                        'get_text').replace(' ', '').replace('USDT', '')
                time.sleep(3)
                assert you_will_receive2[1] == ',', '金额未千分位显示'
                you_will_receive_string = you_will_receive2.replace(',', '')
                assert float(withdrawal_fee) + 1015 == float(you_will_receive_string), 'you_will_receive显示金额错误'
            with allure.step("输入框输入金额1005，显示receive后，清空输入框，检查receive金额是否更新"):
                # 清空输入框
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'delete')
                assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-receive', 'get_text') \
                       == '-12.00 USDT', 'receive金额未更新'
                
    @allure.title('test_web_withdraw_crypto_010')
    @allure.description('Next：Submit WithDrawal')
    def test_withdraw_crypto_010(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'),\
                '页面切换失败'
        # with allure.step("信息填写不完整：不输入信息直接点击next，现信息填写不完整，按钮为置灰状态，和cash不同"): operate_element_web(chrome_driver,
        # 'assetPage', 'click_withdraw_confirm_crypto') assert chrome_driver.find_element_by_link_text('Please fill
        # in withdrawal Address, Amount').is_displayed(),\ '未显示提示信息'
        with allure.step("信息填写完整"):
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input',
                                'bc1qa03ha5pgkm0dyl63gkzwr035qxphjf60dw4wnn')
            # 输入提现金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0.001')
            # 点击Next：Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'click_withdraw_confirm_crypto')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailbtn', 'check'),\
                '未弹出认证框'

    @allure.title('test_web_withdraw_crypto_011')
    @allure.description('Next：Submit WithDrawal')
    def test_withdraw_crypto_011(self, chrome_driver):
        webFunction.login_web(chrome_driver, account=get_json()['email']['payout_email'])
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("切换至withdraw crypto页面"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_select_WE120')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-selector', 'check'),\
                '页面切换失败'
        with allure.step("填写提现信息"):
            # 输入withdrawal address
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-address', 'input',
                                'bc1qa03ha5pgkm0dyl63gkzwr035qxphjf60dw4wnn')
            # 输入提现金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-amount', 'input', '0.001')
            # 点击Next：Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'click_withdraw_confirm_crypto')
        # with allure.step("输入错误邮箱验证码"):
        #     # 输入错误邮箱验证码
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailbtn')
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailcode', 'input', '666663')
        #     # 输入google验证码
        #     with allure.step("通过接口获取google验证码"):
        #         secretKey = get_json()['secretKey']
        #         totp = pyotp.TOTP(secretKey)
        #         mfaVerificationCode = totp.now()
        #         operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-googlecode', 'input',
        #                             mfaVerificationCode)
        #         # 点击【confirm withdrawal】
        #         operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-submit')
        #         assert operate_element_web(chrome_driver, 'assetPage', 'MuiAlert-message', 'get_text') == \
        #                'The verification code was wrong.', 'google验证码错误提示信息未显示'
        # with allure.step("输入正确邮箱验证码，错误google验证码"):
        #     # 输入正确邮箱验证码
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailcode', 'delete')
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailcode', 'input', '666666')
        #     # 输入错误谷歌验证码
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-googlecode', 'input', '666666')
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-submit')
        #     assert operate_element_web(chrome_driver, 'assetPage', 'MuiAlert-message', 'get_text') == \
        #            'The Google Authenticator code was wrong.', 'google验证码错误提示信息未显示'
        with allure.step("输入正确邮箱验证码，正确google验证码"):
            with allure.step("申请邮箱验证码"):
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailbtn')
            with allure.step("通过email获取邮箱验证码"):
                code = ApiFunction.get_email_code(type='MFA_EMAIL')
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-mailcode', 'input', code)
            # 输入google验证码
            with allure.step("通过接口获取google验证码"):
                mfaVerificationCode = get_mfa_code()
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-googlecode', 'input',
                                    mfaVerificationCode)
            with allure.step("点击 confirm withdrawal"):
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-crypto-submit')
