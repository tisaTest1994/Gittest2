from Function.web_function import *
from Function.web_common_function import *


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
                operate_element_web(chrome_driver, 'ConvertPage', 'assets_balanceaction_convert')
                if i == 0:
                    with allure.step("检查弹出提示框"):
                        assert operate_element_web(chrome_driver, '', 'Verify Your Identity', 'check'), "当前账号的kyc状态是:{}, 未弹出Verify Your Identity提示框".format(account_list[test_account])
                    with allure.step("点击Verify Now"):
                        operate_element_web(chrome_driver, 'ConvertPage', 'popup_kyc_action_verify')
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
                        operate_element_web(chrome_driver, 'ConvertPage', 'CloseSharpIcon')
                elif i == 4:
                    with allure.step("检查是否弹出convert弹窗"):
                        assert operate_element_web(chrome_driver, 'ConvertPage', 'convert_sell_input', 'check'),\
                            "当前账号的kyc状态是:{}, 未弹出convert弹窗".format(account_list[test_account])
                    with allure.step("关闭convert弹窗"):
                        operate_element_web(chrome_driver, 'ConvertPage', 'CloseSharpIcon')
                        assert operate_element_web(chrome_driver, 'ConvertPage', 'convert_sell_input', 'check_exist') is False, "未关闭convet弹窗"
            with allure.step("退出当前账号"):
                webFunction.logout_web(chrome_driver)


    # @allure.title('test_web_convert_002')
    # @allure.description('convert 默认币种检查')
    # def test_convert_001(self, chrome_driver):
    #     webFunction.login_web(chrome_driver)
    #     with allure.step("点击convert按钮，弹出convert弹窗"):
    #         operate_element_web(chrome_driver, 'convertPage', 'assets_balanceaction_convert')
    #         assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_input', 'check'), '已弹出convert弹窗'
