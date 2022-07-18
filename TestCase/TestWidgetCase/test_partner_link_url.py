from Function.api_function import *
from Function.operate_sql import *


# Account相关cases
class TestWidgetApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'

    linked = [('link', 'https://widget.latibac.com/wallet'),
              ('kyc', 'https://widget.latibac.com/onboarding/identity'),
              ('2fa', 'https://widget.latibac.com/account/gauth'),
              ('wallet', 'https://widget.latibac.com/wallet'),
              ('deposit', 'https://widget.latibac.com/deposit'),
              ('withdraw', 'https://widget.latibac.com/withdraw'),
              ('convert', 'https://widget.latibac.com/convert'),
              ('transfer', 'https://widget.latibac.com/transfer'),
              ('transactions', 'https://widget.latibac.com/wallet//transaction'),
              ]
    linked_case_title = ['feature:link参数跳转检查',
                         'feature:kyc参数跳转检查',
                         'feature:2fa参数跳转检查',
                         'feature:wallet参数跳转检查',
                         'feature:deposit参数跳转检查',
                         'feature:withdraw参数跳转检查',
                         'feature:convert参数跳转检查',
                         'feature:transfer参数跳转检查',
                         'feature:transactions参数跳转检查',
                         ]

    @allure.title('test_link_001')
    @allure.description('partner linked用户link时根据参数跳转对应地址')
    @pytest.mark.parametrize('feature, expect_url', linked, ids=linked_case_title)
    def test_account_001(self, feature, expect_url):
        with allure.step("获得用户信息"):
            params = {
                'user_ext_ref': '988518746672869376',
                'partner_key': '07c9297b-65f1-4e16-a0bd-ff6889e386de',
                'feature': feature,
                'device_type': 'app'
            }
            with allure.step("验签"):
                sign = ApiFunction.infinni_games_access_sign(
                    url='{}/partner/link?user_ext_ref={}&partner_key={}&feature={}&device_type={}'.format(self.url,
                                                                                                          params[
                                                                                                              'user_ext_ref'],
                                                                                                          params[
                                                                                                              'partner_key'],
                                                                                                          params[
                                                                                                              'feature'],
                                                                                                          params[
                                                                                                              'device_type']))
            params['signature'] = sign
            r = session.request('GET', url='{}/partner/link'.format(self.url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.url)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验url返回值"):
                assert expect_url in r.url, "获取跳转地址,期望url是{}，返回值是{}".format(expect_url, r.url)

    @allure.title('test_link_002')
    @allure.description('partner unlink用户link时全跳转到link地址,infinni账号：alice000010000@yeah.net')
    def test_account_002(self):
        expect_url = 'https://widget.latibac.com/connect/link'
        feature = ['link', 'kyc', '2fa', 'wallet', 'deposit', 'withdraw', 'convert', 'transfer', 'transactions']
        for i in feature:
            params = {
                'user_ext_ref': '992025295185788928',
                'partner_key': '07c9297b-65f1-4e16-a0bd-ff6889e386de',
                'feature': i,
                'device_type': 'app'
            }
            with allure.step("验签"):
                sign = ApiFunction.infinni_games_access_sign(
                    url='{}/partner/link?user_ext_ref={}&partner_key={}&feature={}&device_type={}'.format(self.url,
                                                                                                          params[
                                                                                                              'user_ext_ref'],
                                                                                                          params[
                                                                                                              'partner_key'],
                                                                                                          params[
                                                                                                              'feature'],
                                                                                                          params[
                                                                                                              'device_type']))
            params['signature'] = sign
            r = session.request('GET', url='{}/partner/link'.format(self.url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('feature的参数是{},url返回值是{}'.format(i, str(r.url)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验url返回值"):
                assert expect_url in r.url, "获取跳转地址,期望url是{}，返回值是{}".format(i, expect_url, r.url)
