from Function.api_function import *
from Function.operate_sql import *


# Account相关cases
class TestAccountApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_account_001')
    @allure.description('链接新用户')
    def test_account_001(self):
        with allure.step("注册账户"):
            data = {
                'user_ext_ref': get_json()['infinni_games']['uid_A']
            }
            print(data)
            r = session.request('POST', url='{}/connect/account/{}/link'.format(env_url, get_json()['infinni_games']['partner_id']), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            print(r.json())
            assert r.json()['connect_status'] == 3, "用户连接失败，返回值是{}".format(r.text)
            account_vid = r.json()['account_vid']
        with allure.step("断开链接unlink"):
            data = {
                'account_vid': account_vid
            }
            r = session.request('POST',
                                url='{}/connect/account/{}/unlink'.format(env_url,
                                                                          get_json()['infinni_games']['partner_id']),
                                data=json.dumps(data), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_account_002')
    @allure.description('链接新用户')
    def test_account_002(self):
        data = {
            'account_vid': 'f21246e7-e849-4230-9f23-2682bc8a886d'
        }
        r = session.request('POST',
                            url='{}/connect/account/{}/unlink'.format(env_url, get_json()['infinni_games']['partner_id']),
                            data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))