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

    @allure.title('test_web_withdraw_cash_001')
    @allure.description('select withdrawal currency')
    def test_withdraw_cash_001(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            time.sleep(2)
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'),\
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("检查默认币种，并切换币种"):
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'get_value') == 'EUR', "默认币种错误"
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', '-assets-withdraw-fiat-selector-change-drop-btn-up')
            # 选择GBP
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector-option-GBP-1')
            assert chrome_driver.find_element_by_xpath('//div/img[@src="../images/coin/GBP.png"]'), '币种未切换至GBP'
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', '-assets-withdraw-fiat-selector-change-drop-btn-up')
            # 选择EUR
            operate_element_web(chrome_driver, 'assetPage', '-option-EUR-0')
            assert chrome_driver.find_element_by_xpath('//div/img[@src="../images/coin/EUR.png"]'), '币种未切换至EUR'

    @allure.title('test_web_withdraw_cash_002')
    @allure.description('change')
    def test_withdraw_cash_002(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("点击change按钮，并判断是否弹出更改信息框"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_namechange')
            time.sleep(2)
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-setname', 'check'), '未弹出更改信息框'

    @allure.title('test_web_withdraw_cash_003')
    @allure.description('FAQ about Account Name')
    def test_withdraw_cash_003(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("点击change按钮"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_namechange')
        with allure.step("点击FAQ about Account Name文字"):
            chrome_driver.find_element_by_xpath('//*[text()="{}"]'.format('FAQ about Account Name')).click()
            time.sleep(2)
            handles = chrome_driver.window_handles
            chrome_driver.switch_to_window(handles[1])
            # 获取当前的url
            now_url = chrome_driver.current_url
            print(now_url)
            # 对url做判断
            assert now_url == "https://faq.cabital.com/s/article/What-if-my-bank-account-name-is-different-from-my-" \
                              "Cabital-username?topicId=0TO5g000000ClReGAK", '页面跳转错误'

    @allure.title('test_web_withdraw_cash_004')
    @allure.description('comfirm和cancel按钮')
    def test_withdraw_cash_004(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("点击cancel按钮"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_namechange')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-modal-close')
            assert operate_element_web(chrome_driver, 'assetPage', 'withdraw_namechange', 'check'), '窗口未关闭'
        with allure.step("点击confirm按钮"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_namechange')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-setname')
            assert operate_element_web(chrome_driver, 'assetPage', 'withdraw_namechange', 'check'), '窗口未关闭'

    @allure.title('test_web_withdraw_cash_005')
    @allure.description('IBAN规则校验')
    def test_withdraw_cash_005(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("输入错误格式iban：不在范围内的bank_country_code"):
            # 输入错误格式iban
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'input',
                                'AA12345678901234567890')
            time.sleep(1)
            # 输入正确格式bic
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'input', 'ZXCVBG12')
            time.sleep(1)
            # 输入正确金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '5')
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "code": "EUR",
                    "amount": "22.5",
                    "payment_method": "SEPA",
                    "account_name": "kimi w",
                    "iban": "AA12345678901234567890",
                    "bic": "ZXCVBG12"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data1), headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("输入错误格式iban：正确范围内的bank_country_code+错误长度阿拉伯数字"):
            # 清空iban输入框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'delete')
            # 输入错误格式iban
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'input',
                                'BG1234567890123456789')
            time.sleep(5)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data2 = {
                    "code": "EUR",
                    "amount": "22.5",
                    "payment_method": "SEPA",
                    "account_name": "kimi w",
                    "iban": "BG1234567890123456789",
                    "bic": "ZXCVBG12"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data2), headers=headers)
                time.sleep(2)
                message = r.json()['message']
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("输入正确格式iban：正确范围内的bank_country_code+正确长度阿拉伯数字"):
            # 清空iban输入框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'delete')
            # 输入错误格式iban
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'input',
                                'BG12345678901234567890')
            time.sleep(5)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailbtn', 'check'),\
                '未弹出withdrawal认证框'

    @allure.title('test_web_withdraw_cash_006')
    @allure.description('BIC规则校验')
    def test_withdraw_cash_006(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("输入错误格式bic，错误长度"):
            # 输入正确格式iban
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'input',
                                'BG12345678901234567890')
            time.sleep(1)
            # 输入错误格式bic，错误长度
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'input', 'ZXCVBG123')
            time.sleep(1)
            # 输入正确金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '5')
            time.sleep(2)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "code": "EUR",
                    "amount": "22.5",
                    "payment_method": "SEPA",
                    "account_name": "kimi w",
                    "iban": "BG12345678901234567890",
                    "bic": "ZXCVBG123"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data1),
                                    headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("输入错误格式bic，前6位非字母"):
            # 清空bic
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'delete')
            # 输入错误格式bic，前6位非字母
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'input', 'ZXC123')
            time.sleep(1)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "code": "EUR",
                    "amount": "22.5",
                    "payment_method": "SEPA",
                    "account_name": "kimi w",
                    "iban": "BG12345678901234567890",
                    "bic": "ZXC123"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data1),
                                    headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("输入正确格式bic，正确长度（8位或11位）且前六位为字母"):
            # 清空bic
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'delete')
            # 输入正确格式bic，正确长度（8位或11位）且前六位为字母
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'input', 'ZXCVBG12')
            time.sleep(1)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailbtn', 'check'),\
                '未弹出withdrawal认证框'

    @allure.title('test_web_withdraw_cash_007')
    @allure.description('account number规则校验')
    def test_withdraw_cash_007(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("切换至GBP"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector-change-drop-btn-up')
            # 选择GBP
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector-option-GBP-1')
        with allure.step("输入错误格式account number,错误长度纯数字"):
            # 输入account number
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userNum', 'input',
                                '123456')
            time.sleep(1)
            # 输入正确格式sort code
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userCode', 'input', '123456')
            time.sleep(1)
            # 输入正确金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '0')
            time.sleep(2)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "code": "GBP",
                    "amount": "17.5",
                    "payment_method": "Faster Payments",
                    "account_name": "kimi w",
                    "account_number": "123456",
                    "sort_code": "123456"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data1),
                                    headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("输入错误格式account number,正确长度非纯数字"):
            # 清空account number
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userNum', 'delete')
            # 输入account number
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userNum', 'input',
                                '12345abc')
            time.sleep(1)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "code": "GBP",
                    "amount": "17.5",
                    "payment_method": "Faster Payments",
                    "account_name": "kimi w",
                    "account_number": "12345abc",
                    "sort_code": "123456"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data1),
                                    headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("输入正确格式account number（8位纯数字）"):
            # 清空account number
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userNum', 'delete')
            # 输入account number
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userNum', 'input',
                                '12345678')
            time.sleep(1)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailbtn', 'check'),\
                '未弹出withdrawal认证框'

    @allure.title('test_web_withdraw_cash_008')
    @allure.description('Sort code规则校验')
    def test_withdraw_cash_008(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("切换至GBP"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector-change-drop-btn-up')
            # 选择GBP
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector-option-GBP-1')
        with allure.step("输入错误格式从sort code,6位非纯数字"):
            # 输入account number
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userNum', 'input',
                                '12345678')
            time.sleep(1)
            # 输入sort code
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userCode', 'input', 'abc666')
            time.sleep(1)
            # 输入正确金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '0')
            time.sleep(2)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "code": "GBP",
                    "amount": "17.5",
                    "payment_method": "Faster Payments",
                    "account_name": "kimi w",
                    "account_number": "12345678",
                    "sort_code": "abc666"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data1),
                                    headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("输入错误格式从sort code,非6位纯数字"):
            # 清空sort code
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userCode', 'delete')
            # 输入sort code
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userCode', 'input', '12345')
            time.sleep(1)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "code": "GBP",
                    "amount": "17.5",
                    "payment_method": "Faster Payments",
                    "account_name": "kimi w",
                    "account_number": "12345678",
                    "sort_code": "12345"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data1),
                                    headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'
        with allure.step("输入正确格式sort code,6位纯数字"):
            # 清空sort code
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userCode', 'delete')
            # 输入sort code
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userCode', 'input', '123456')
            time.sleep(1)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailbtn', 'check'), \
                '未弹出withdrawal认证框'

    @allure.title('test_web_withdraw_cash_009')
    @allure.description('IBAN和BIC匹配校验')
    def test_withdraw_cash_009(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        # 接口会进行校验，如IBAN_CODE和BIC_CODE不匹配（BIC是第5位和第6位是国家代码，IBAN是前两位）
        with allure.step("IBAN_CODE和BIC_CODE不匹配"):
            # 输入iban
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'input',
                                'BG12345678901234567890')
            time.sleep(1)
            # 输入bic
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'input', 'ZXCVGB123')
            time.sleep(1)
            # 输入正确金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '5')
            time.sleep(2)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            with allure.step("调用接口获得数据"):
                data1 = {
                    "code": "EUR",
                    "amount": "22.5",
                    "payment_method": "SEPA",
                    "account_name": "kimi w",
                    "iban": "BG12345678901234567890",
                    "bic": "ZXCVGB123"
                }
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data1),
                                    headers=headers)
                time.sleep(2)
                message = r.json()['message']
                print(message)
                assert operate_element_web(chrome_driver, '', message, type='check'), '未显示接口返回提示信息'

    @allure.title('test_web_withdraw_cash_010')
    @allure.description('withdrawal amount金额限制校验（EUR）')
    def test_withdraw_cash_0010(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("输入的值小于最小提现金额"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount-helper-text',
                                       'get_text') == 'Minimum: 25', '最小限额提示信息未显示'
        with allure.step("输入的值大于最大可提现金额（available balance）"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2000000')
            assert 'Insufficient Amount' in operate_element_web(chrome_driver, 'assetPage',
                                                                'assets-withdraw-fiat-amount-helper-text', 'get_text'),\
                '最大限额提示信息未显示'
        with allure.step("输入的值大于最大可提现金额（available balance）"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '50001')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount-helper-text',
                                       'get_text') == 'Maximum: 50,000.00', '最大限额提示信息未显示'
        with allure.step("输入符合要求的提现金额"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '30')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount-helper-text',
                                       'check_exist') is False, '提示信息未显示错误'

    @allure.title('test_web_withdraw_cash_011')
    @allure.description('withdrawal amount金额限制校验（GBP）')
    def test_withdraw_cash_0011(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("切换币种：GBP"):
            # 点击下拉框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector-change-drop-btn-up')
            # 选择GBP
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector-option-GBP-1')
        with allure.step("输入的值小于最小提现金额"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount-helper-text',
                                       'get_text') == 'Minimum: 20', '最小限额提示信息未显示'
        with allure.step("输入的值大于最大可提现金额（available balance）"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2000000')
            assert 'Insufficient Amount' in operate_element_web(chrome_driver, 'assetPage',
                                                                'assets-withdraw-fiat-amount-helper-text', 'get_text'),\
                '最大限额提示信息未显示'
        with allure.step("输入的值大于最大可提现金额（available balance）"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '40001')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount-helper-text',
                                       'get_text') == 'Maximum: 40,000.00', '最大限额提示信息未显示'
        with allure.step("输入符合要求的提现金额"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '25')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount-helper-text',
                                       'check_exist') is False, '提示信息未显示错误'

    @allure.title('test_web_withdraw_cash_012')
    @allure.description('withdrawal amount-Max')
    def test_withdraw_cash_012(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("获取可用金额数据"):
            available_balance_text = operate_element_web(chrome_driver, 'assetPage',
                                                         'assets-withdraw-fiat-amount-helper-text', 'get_text')
            available_balance = available_balance_text.replace(
                'Available Balance: ', '').replace(' ', '').replace('EUR', '').replace(',', '')
            # 自动填入可提现的最大金额，金额和下方的available balance相同
        with allure.step("点击max按钮"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_max_fiat')
            assert chrome_driver.find_element_by_id('assets-withdraw-fiat-amount').get_attribute('value')\
                   == available_balance, '未自动填入最大可提现金额'

    @allure.title('test_web_withdraw_cash_013')
    @allure.description('receive金额显示')
    def test_withdraw_cash_013(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("receive默认金额显示，用0调取显示fee"):
            withdrawal_fee = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-fee',
                                                 'get_text').replace(' ', '').replace('EUR', '')
            you_will_receive = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-receive',
                                                   'get_text').replace(' ', '').replace('EUR', '')
            assert float(withdrawal_fee) + 0 == float(you_will_receive), 'you_will_receive默认显示金额错误'
        with allure.step("检查金额是否正确且为千分位"):
            # 输入金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '1')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '0')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '0')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '5')
            you_will_receive2 = operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-receive',
                                                    'get_text').replace(' ', '').replace('EUR', '')
            time.sleep(2)
            assert you_will_receive2[1] == ',', '金额未千分位显示'
            you_will_receive_string = you_will_receive2.replace(',', '')
            assert float(withdrawal_fee) + 1005 == float(you_will_receive_string), 'you_will_receive显示金额错误'
        with allure.step("输入框输入金额1005，显示receive后，清空输入框，检查receive金额是否更新"):
            # 清空输入框
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'delete')
            time.sleep(2)
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-receive', 'get_text')\
                   == '-2.5 EUR', 'receive金额未更新'

    @allure.title('test_web_withdraw_cash_014')
    @allure.description('Next：Submit WithDrawal')
    def test_withdraw_cash_014(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
            time.sleep(2)
        with allure.step("信息填写不完整：不输入信息直接点击next"):
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            time.sleep(2)
            assert chrome_driver.find_element_by_xpath('//*[text()="{}"]'.format('Please fill in IBAN, BIC, Amount')).is_displayed(),\
                '未显示提示信息'
        with allure.step("信息填写完整"):
            # 输入iban
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'input',
                                'BG12345678901234567890')
            time.sleep(1)
            # 输入bic
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'input', 'ZXCVBG12')
            time.sleep(1)
            # 输入正确金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '2')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '5')
            time.sleep(2)
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailcode', 'check'),\
                '未弹出认证框'

    @allure.title('test_web_withdraw_cash_015')
    @allure.description('confirm withdrawal流程')
    def test_withdraw_cash_015(self, chrome_driver):
        webFunction.login_web(chrome_driver, account=get_json()['email']['payout_email'])
        with allure.step("点击withdraw按钮，并判断是否跳转至withdraw页面,默认为Withdraw Cash"):
            operate_element_web(chrome_driver, 'assetPage', 'assets_balanceaction_withdraw')
            assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-selector', 'check'), \
                '页面未跳转至Withdraw-withdraw Cash页面'
        with allure.step("填写提现信息"):
            # 输入iban
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userIBAN', 'input',
                                'BG12345678901234567890')
            # 输入bic
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-userBIC', 'input', 'ZXCVBG12')
            # 输入正确金额
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-fiat-amount', 'input', '25')
            # 点击Next: Submit Withdrawal
            operate_element_web(chrome_driver, 'assetPage', 'withdraw_confirm_cash')
        with allure.step("申请邮箱验证码"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailbtn')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailcode', 'input', '666663')

            # 输入google验证码
            with allure.step("通过接口获取google验证码"):
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-googlecode', 'input',
                                    mfaVerificationCode)
                # 点击【confirm withdrawal】
                operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-submit')
                assert operate_element_web(chrome_driver, 'assetPage', 'MuiAlert-message', 'get_text') ==\
                       'The verification code was wrong.', 'google验证码错误提示信息未显示'
        with allure.step("输入正确邮箱验证码，错误google验证码"):
            # 输入正确邮箱验证码
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailcode', 'delete')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailcode', 'input', '666666')
            # 输入错误谷歌验证码
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-googlecode', 'input', '666666')
        with allure.step("通过email获取邮箱验证码"):
            code = ApiFunction.get_email_code(type='MFA_EMAIL')
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailcode', 'input', code)
        # 输入google验证码
        with allure.step("通过接口获取google验证码"):
            mfaVerificationCode = get_mfa_code()
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-googlecode', 'input', mfaVerificationCode)
        with allure.step("点击 confirm withdrawal"):
            operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-submit')
            sleep(1000)



        # with allure.step("输入正确邮箱验证码，错误google验证码"):
        #     # 输入正确邮箱验证码
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailcode', 'delete')
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-mailcode', 'input', '666666')
        #     # 输入错误谷歌验证码
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-googlecode', 'input', '666666')
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-submit')
        #     assert operate_element_web(chrome_driver, 'assetPage', 'MuiAlert-message', 'get_text') ==\
        #            'The Google Authenticator code was wrong.', 'google验证码错误提示信息未显示'
        # with allure.step("输入正确邮箱验证码，正确google验证码"):
        #     # 输入清除错误谷歌验证码
        #     operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-googlecode', 'delete')
        #     with allure.step("通过接口获取google验证码"):
        #         secretKey = get_json()['secretKey']
        #         totp = pyotp.TOTP(secretKey)
        #         mfaVerificationCode = totp.now()
        #         operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-googlecode', 'input',
        #                             mfaVerificationCode)
        #         # 点击【confirm withdrawal】
        #         operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-submit')
        #         assert operate_element_web(chrome_driver, 'assetPage', 'assets-withdraw-cash-submit', 'check'), '窗口未关闭'
