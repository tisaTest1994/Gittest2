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

    linked = [('link', 'https://widget.latibac.com/connect/link?'),
              ('kyc', 'https://widget.latibac.com/onboarding?feature=kyc'),
              ('2fa', 'https://widget.latibac.com/account/gauth?feature=2fa'),
              ('wallet', 'https://widget.latibac.com/wallet?feature=wallet'),
              ('deposit', 'https://widget.latibac.com/deposit?feature=deposit'),
              ('withdraw', 'https://widget.latibac.com/withdraw?feature=withdraw'),
              ('convert', 'https://widget.latibac.com/convert?feature=convert'),
              ('transfer', 'https://widget.latibac.com/wallet?feature=transfer'),
              ('transaction', 'https://widget.latibac.com/transaction?feature=transaction'),
              ('transactionlist', 'https://widget.latibac.com/wallet?feature=wallet'),
              ('onboarding', 'https://widget.latibac.com/onboarding?'),
              ]
    linked_case_title = ['feature:link参数跳转检查',
                         'feature:kyc参数跳转检查',
                         'feature:2fa参数跳转检查',
                         'feature:wallet参数跳转检查',
                         'feature:deposit参数跳转检查',
                         'feature:withdraw参数跳转检查',
                         'feature:convert参数跳转检查',
                         'feature:transfer参数跳转检查',
                         'feature:transaction参数跳转检查',
                         'feature:transactionlist参数跳转检查',
                         'feature:onboarding参数跳转检查',
                         ]
    unlinked = [('link', 'https://widget.latibac.com/connect/link?'),
              ('kyc', 'https://widget.latibac.com/onboarding?feature=kyc'),
              ('2fa', 'https://widget.latibac.com/account/gauth?feature=2fa'),
              ('wallet', 'https://widget.latibac.com/wallet?feature=wallet'),
              ('deposit', 'https://widget.latibac.com/deposit?feature=deposit'),
              ('withdraw', 'https://widget.latibac.com/withdraw?feature=withdraw'),
              ('convert', 'https://widget.latibac.com/convert?feature=convert'),
              ('transfer', 'https://widget.latibac.com/wallet?feature=transfer'),
              ('transaction', 'https://widget.latibac.com/transaction?feature=transaction'),
               ('transactionlist', 'https://widget.latibac.com/connect/link?feature=link'),
              ('onboarding', 'https://widget.latibac.com/onboarding?'),
              ]

    @allure.title('test_link_001')
    @allure.description('partner linked用户link时根据参数跳转对应地址')
    @pytest.mark.parametrize('feature, expect_url', linked, ids=linked_case_title)
    def test_account_001(self, feature, expect_url, partner):
        with allure.step("获得用户信息"):
            params = {
                'user_ext_ref': get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                        'user_ref_id'],
                'partner_key': get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID'],
                'feature': feature,
                'redirect_url': '',
                'device_type': 'app',
                'pair':'',
                'major_ccy': '',
                'major_amount': ''
            }
            r1 = session.request('GET', url='{}/partner/link'.format(connect_url), params=params, headers=headers)
            with allure.step("验签"):
                sign = ApiFunction.get_link_sign(url=r1.url, partner=partner)
                connect_headers['ACCESS-SECRET'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                    'Secret_Key']
                params['signature'] = sign
            r = session.request('GET', url='{}/partner/link'.format(connect_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.url)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验url返回值"):
                assert expect_url in r.url, "feature是{},获取跳转地址,期望url是{}，返回值是{}".format(feature,expect_url, r.url)

    @allure.description('partner未linked用户传入不同的feature跳转地址校验，以infinni为例')
    @pytest.mark.parametrize('feature, expect_url', unlinked, ids=linked_case_title)
    def test_account_002(self, feature, expect_url, partner):
        partner ='infinni'
        with allure.step("获得用户信息"):
            params = {
                'user_ext_ref': '992025295185788928',
                'partner_key': '07c9297b-65f1-4e16-a0bd-ff6889e386de',
                'feature': feature,
                'redirect_url': '',
                'device_type': 'app',
                'pair': '',
                'major_ccy': '',
                'major_amount': ''
            }
            r1 = session.request('GET', url='{}/partner/link'.format(connect_url), params=params, headers=headers)
            with allure.step("验签"):
                sign = ApiFunction.get_link_sign(url=r1.url, partner=partner)
                connect_headers['ACCESS-SECRET'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                    'Secret_Key']
                params['signature'] = sign
            r = session.request('GET', url='{}/partner/link'.format(connect_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.url)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验url返回值"):
                assert expect_url in r.url, "获取跳转地址,期望url是{}，返回值是{}".format(expect_url, r.url)
