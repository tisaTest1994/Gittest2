from Function.web_function import *
from Function.web_common_function import *
from Function.api_function import *


@allure.feature("web ui convert 相关 testcases")
class TestWebConvert:
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency

    def teardown_method(self):
        pass

    @allure.title('test_web_convert_001')
    @allure.description('convert kyc检测')
    def test_convert_001(self, chrome_driver):
        account_list = {'winniekyc11@test.com': "还未在 Cabital 提交 KYC", 'winniekyc12@test.com': 'Cabital处理用户材料中',
                        'winniekyc13@test.com': '用户被 Cabital 要求提供正确材料', 'winniekyc14@test.com': '用户被 Cabital 最终拒绝开户',
                        'winniekyc15@test.com': 'KYC pass'}
        len_account = len(account_list)
        for i in range(0, len_account):
            test_account = list(account_list)[i]
            with allure.step("登录不同KYC状态的账号"):
                webFunction.login_web(chrome_driver, account=test_account, password='A!234sdfg')
            with allure.step("点击convert按钮"):
                operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
                if i == 0:
                    with allure.step("检查弹出提示框"):
                        assert operate_element_web(chrome_driver, '', 'Verify Your Identity', 'check'), "当前账号的kyc状态是:{}, 未弹出Verify Your Identity提示框".format(account_list[test_account])
                    with allure.step("点击Verify Now"):
                        operate_element_web(chrome_driver, 'convertPage', 'popup_kyc_action_verify')
                        assert operate_element_web(chrome_driver, '', 'Identity Verification', 'check'), "未跳转至kyc认证页面"
                elif i == 1:
                    with allure.step("检查弹出提示框"):
                        assert operate_element_web(chrome_driver, '', 'Verification Under Review', 'check'), "当前账号的kyc状态是:{}, 未弹出Verification Under Review提示框".format(account_list[test_account])
                    with allure.step("点击Got it"):
                        operate_element_web(chrome_driver, '', 'Got it')
                        assert operate_element_web(chrome_driver, '', 'Verification Under Review', 'check_exist') is False, "提示信息未关闭"
                elif i == 2:
                    with allure.step("检查弹出提示框"):
                        assert operate_element_web(chrome_driver, '', 'Action Required', 'check'), "当前账号的kyc状态是:{}, 未弹出Action Required提示框".format(account_list[test_account])
                    with allure.step("点击Resubmit"):
                        operate_element_web(chrome_driver, '', 'Resubmit')
                        assert operate_element_web(chrome_driver, '', 'Identity Verification', 'check'), "未跳转至Identity Verification页面"
                elif i == 3:
                    with allure.step("检查弹出提示框"):
                        assert operate_element_web(chrome_driver, '', 'Verification Failed', 'check'), "当前账号的kyc状态是:{}, 未弹出Action Required提示框".format(account_list[test_account])
                    with allure.step("Contact Us不点击验证，关闭窗口"):
                        operate_element_web(chrome_driver, 'convertPage', 'CloseSharpIcon')
                elif i == 4:
                    with allure.step("检查是否弹出convert弹窗"):
                        assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', 'check'),\
                            "当前账号的kyc状态是:{}, 未弹出convert弹窗".format(account_list[test_account])
                    with allure.step("关闭convert弹窗"):
                        operate_element_web(chrome_driver, 'convertPage', 'CloseSharpIcon')
                        assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', 'check_exist') is False, "未关闭convet弹窗"
            with allure.step("退出当前账号"):
                webFunction.logout_web(chrome_driver)

    @allure.title('test_web_convert_002')
    @allure.description('convert 默认币种检查')
    def test_convert_002(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击convert按钮，弹出convert弹窗"):
            operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
            assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', 'check'), '已弹出convert弹窗'
            fiat_sell_default = 'EUR'
            fiat_buy_default = 'USDT'
        with allure.step("检查默认币种"):
            assert operate_element_web(chrome_driver, '', fiat_sell_default, 'check'), "sell默认币种错误"
            assert operate_element_web(chrome_driver, '', fiat_buy_default, 'check'), "buy默认币种错误"

    @allure.title('test_web_convert_003')
    @allure.description('convert主流程测试')
    def test_convert_003(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("convert主流程测试"):
            for i in ApiFunction.get_cfx_list():
                with allure.step("正向币种对，major_ccy 是buy值"):
                    buy_currency = i.split('-')[0]
                    sell_currency = i.split('-')[1]
                    with allure.step("点击convert按钮，弹出convert弹窗"):
                        operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
                        assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input',
                                                   'check'), '已弹出convert弹窗'
                    with allure.step("切换buy币种和sell币种"):
                        webFunction.web_convert_select_currency(chrome_driver, buy_currency, sell_currency)
                    with allure.step("获得换汇前buy币种balance金额"):
                        buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step('获得换汇前sell币种balance金额'):
                        sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("随机生成要输入的金额"):
                        transaction = webFunction.web_cfx_random(i, i.split('-')[0])
                        operate_element_web(chrome_driver, 'convertPage', 'convert_buy_input', "input", transaction['data']['buy_amount'])
                        
                    with allure.step("点击convert按钮"):
                        operate_element_web(chrome_driver, 'convertPage', 'convert_btn_submit')
                        sleep(1)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("验证convert成功后buy的金额是否正确"):
                        assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                            transaction['data']['buy_amount']) == Decimal(
                            buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                            i.split('-')[0], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                            buy_amount_wallet_balance_latest)
                    with allure.step("验证convert成功后sell的金额是否正确"):
                        assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                            transaction['data']['sell_amount']) == Decimal(
                            sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                            i.split('-')[1], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                            sell_amount_wallet_balance_latest)
                with allure.step("正向币种对，major_ccy 是sell值"):
                    buy_currency = i.split('-')[0]
                    sell_currency = i.split('-')[1]
                    with allure.step("点击convert按钮，弹出convert弹窗"):
                        operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
                        assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input',
                                                  'check'), '已弹出convert弹窗'
                    with allure.step("切换buy币种和sell币种"):
                        webFunction.web_convert_select_currency(chrome_driver, buy_currency, sell_currency)
                    with allure.step("获得换汇前buy币种balance金额"):
                        buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step('获得换汇前sell币种balance金额'):
                        sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                        sleep(1)
                    with allure.step("随机生成要输入的金额"):
                        transaction = webFunction.web_cfx_random(i, i.split('-')[1])
                        operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', "input", transaction['data']['sell_amount'])
                    with allure.step("点击convert按钮"):
                        operate_element_web(chrome_driver, 'convertPage', 'convert_btn_submit')
                        sleep(1)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("验证convert成功后buy的金额是否正确"):
                        assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                            transaction['data']['buy_amount']) == Decimal(
                            buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                            i.split('-')[0], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                            buy_amount_wallet_balance_latest)
                    with allure.step("验证convert成功后sell的金额是否正确"):
                        assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                            transaction['data']['sell_amount']) == Decimal(
                            sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                            i.split('-')[1], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                            sell_amount_wallet_balance_latest)
                with allure.step("反向币种对，major_ccy 是buy值"):
                    buy_currency = i.split('-')[1]
                    sell_currency = i.split('-')[0]
                    with allure.step("点击convert按钮，弹出convert弹窗"):
                        operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
                        assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input',
                                                   'check'), '已弹出convert弹窗'
                    with allure.step("切换buy币种和sell币种"):
                        webFunction.web_convert_select_currency(chrome_driver, buy_currency, sell_currency)
                    with allure.step("获得换汇前buy币种balance金额"):
                        buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step('获得换汇前sell币种balance金额'):
                        sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("随机生成要输入的金额"):
                        transaction = webFunction.web_cfx_random('{}-{}'.format(i.split('-')[1], i.split('-')[0]),
                                                         i.split('-')[1])
                        operate_element_web(chrome_driver, 'convertPage', 'convert_buy_input', "input", transaction['data']['buy_amount'])
                    with allure.step("点击convert按钮"):
                        operate_element_web(chrome_driver, 'convertPage', 'convert_btn_submit')
                        sleep(3)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("验证convert成功后buy的金额是否正确"):
                        assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                            transaction['data']['buy_amount']) == Decimal(
                            buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                            i.split('-')[1], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                            buy_amount_wallet_balance_latest)
                    with allure.step("验证convert成功后sell的金额是否正确"):
                        assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                            transaction['data']['sell_amount']) == Decimal(
                            sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                            i.split('-')[0], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                            sell_amount_wallet_balance_latest)
                with allure.step("反向币种对，major_ccy 是sell值"):
                    buy_currency = i.split('-')[1]
                    sell_currency = i.split('-')[0]
                    with allure.step("点击convert按钮，弹出convert弹窗"):
                        operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
                        assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input',
                                                   'check'), '已弹出convert弹窗'
                    with allure.step("切换buy币种和sell币种"):
                        webFunction.web_convert_select_currency(chrome_driver, buy_currency, sell_currency)
                    with allure.step("获得换汇前buy币种balance金额"):
                        buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step('获得换汇前sell币种balance金额'):
                        sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("随机生成要输入的金额"):
                        transaction = webFunction.web_cfx_random('{}-{}'.format(i.split('-')[1], i.split('-')[0]),
                                                         i.split('-')[0])
                        operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', "input", transaction['data']['sell_amount'])
                    with allure.step("点击convert按钮"):
                        operate_element_web(chrome_driver, 'convertPage', 'convert_btn_submit')
                        sleep(3)
                    with allure.step("获得换汇后buy币种balance金额"):
                        buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[1])
                    with allure.step("获得换汇后sell币种balance金额"):
                        sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=i.split('-')[0])
                    with allure.step("验证convert成功后buy的金额是否正确"):
                        assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                            transaction['data']['buy_amount']) == Decimal(
                            buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                            i.split('-')[1], buy_amount_wallet_balance_old, transaction['data']['buy_amount'],
                            buy_amount_wallet_balance_latest)
                    with allure.step("验证convert成功后sell的金额是否正确"):
                        assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                            transaction['data']['sell_amount']) == Decimal(
                            sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                            i.split('-')[0], sell_amount_wallet_balance_old, transaction['data']['sell_amount'],
                            sell_amount_wallet_balance_latest)

    @allure.title('test_web_convert_004')
    @allure.description('available金额检查')
    def test_convert_004(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击convert按钮，弹出convert弹窗"):
            operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
            assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', 'check'), '已弹出convert弹窗'
        with allure.step("检查默认sell币种的available balance金额显示"):
            with allure.step("从接口获取sell的available balance"):
                fiat_sell_default = 'EUR'
                sell_amount_wallet_balance = ApiFunction.get_crypto_number(type=fiat_sell_default)
                with allure.step("数据处理(千分位, 末尾补0去0)"):
                    sell_amount_wallet_balance2 = add_currency_symbol(sell_amount_wallet_balance, fiat_sell_default)
            with allure.step("判断页面金额显示是否和接口返回数据一致"):
                available_balance = chrome_driver.find_element_by_xpath("//*[@id='convert_sell_input']/../../../div").text
                available_balance_amount = available_balance.split(":")[1].strip()
                assert available_balance_amount == sell_amount_wallet_balance2, "available balance金额显示错误"

    @allure.title('test_web_convert_005')
    @allure.description('convert_sell_max功能验证，自动填入sell的available balance')
    def test_convert_005(self, chrome_driver):
        webFunction.login_web(chrome_driver)
        with allure.step("点击convert按钮，弹出convert弹窗"):
            operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
            assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', 'check'), '已弹出convert弹窗'
        with allure.step("从接口获取sell的available balance"):
            fiat_sell_default = 'EUR'
            sell_amount_wallet_balance = ApiFunction.get_crypto_number(type=fiat_sell_default)
        with allure.step("点击max按钮"):
            operate_element_web(chrome_driver, 'convertPage', 'dialog_convert_max')
            assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', 'get_value') == sell_amount_wallet_balance, 'max按钮未自动填入最大可用金额'


    # @allure.title('test_web_convert_006')
    # @allure.description('sell和buy金额限制校验（单笔最大最小值只判断Major code，Available Balance只判断Sell）')
    # def test_convert_006(self, chrome_driver):
    #     webFunction.login_web(chrome_driver)
    #     with allure.step("点击convert按钮，弹出convert弹窗"):
    #         operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
    #         assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', 'check'), '已弹出convert弹窗'