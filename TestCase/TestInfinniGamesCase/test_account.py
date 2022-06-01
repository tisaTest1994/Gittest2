import json

from Function.api_function import *
from Function.operate_sql import *


# Account相关cases
class TestAccountApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'

    @allure.title('test_account_001')
    @allure.description('链接新用户')
    def test_account_001(self):
        with allure.step("获得用户信息"):
            params = {
                'user_ext_ref': get_json()['infinni_games']['uid_A'],
                'partner_key': '07c9297b-65f1-4e16-a0bd-ff6889e386de'
            }
            with allure.step("验签"):
                sign = ApiFunction.infinni_games_access_sign(url='{}/partner/link?user_ext_ref={}&partner_key={}'.format(self.url, params['user_ext_ref'], params['partner_key']))
            params['signature'] = sign
            r = session.request('GET', url='{}/partner/link'.format(self.url), params=params, headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("注册账户"):
            data = {
                'user_ext_ref': params['user_ext_ref']
            }
            r = session.request('POST', url='{}/connect/account/{}/link'.format(env_url,
                                                                                get_json()['infinni_games'][
                                                                                    'partner_id']),
                                data=json.dumps(data), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['link_status'] == 2, "link新用户失败，返回值是{}".format(r.text)
                assert r.json()['connect_status'] == 3, "link新用户失败，返回值是{}".format(r.text)
        with allure.step("删除数据库link信息"):
            sql = "delete from account_link where user_ref_id = '{}';".format(params['user_ext_ref'])
            logger.info('sql命令是{}'.format(sql))
            sqlFunction().connect_mysql('partner', sql=sql)






    #     with allure.step("校验状态码"):
    #         assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
    #     with allure.step("校验返回值"):
    #         print(r.json())
    #         assert r.json()['connect_status'] == 3, "用户连接失败，返回值是{}".format(r.text)
    #         account_vid = r.json()['account_vid']
    #     with allure.step("断开链接unlink"):
    #         data = {
    #             'account_vid': account_vid
    #         }
    #         r = session.request('POST',
    #                             url='{}/connect/account/{}/unlink'.format(env_url,
    #                                                                       get_json()['infinni_games']['partner_id']),
    #                             data=json.dumps(data), headers=headers)
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
    #
    # @allure.title('test_account_002')
    # @allure.description('链接新用户')
    # def test_account_002(self):
    #     params = {
    #         'user_ext_ref': ''
    #     }
    #     r = session.request('GET',
    #                         url='{}/partner/link?user_ext_ref={}&partner_key=07c9297b-65f1-4e16-a0bd-ff6889e386de'.format(env_url,
    #                                                                   get_json()['infinni_games']['partner_id']), headers=headers)
    #     print(r.url)
    #     print(r.json())
    #
    #     data = {
    #         'account_vid': 'f21246e7-e849-4230-9f23-2682bc8a886d'
    #     }
    #     r = session.request('POST',
    #                         url='{}/connect/account/{}/unlink'.format(env_url, get_json()['infinni_games']['partner_id']),
    #                         data=json.dumps(data), headers=headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))