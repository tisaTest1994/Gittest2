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

    # @allure.title('test_account_001')
    # @allure.description('partner unlink(改account_vid)')
    # def test_account_001(self):
    #     headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='test1027@163.com',password ='Zcdsw123')
    #     partner_id = get_json()["infinni_games"]["partner_id"]
    #     account_id = "ab09d031-9c3e-4e86-8b0e-b7f4b4372cb5"
    #     with allure.step("获得data"):
    #         data = {
    #             "channel": "PARTNER"
    #         }
    #     with allure.step("验签"):
    #         unix_time = int(time.time())
    #         nonce = generate_string(30)
    #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
    #                                             url='/api/v1/accounts/{}/unlink'.format(account_id),
    #                                             key='infinni games', nonce=nonce, body=json.dumps(data))
    #         headers['ACCESS-SIGN'] = sign
    #         headers['ACCESS-TIMESTAMP'] = str(unix_time)
    #         headers['ACCESS-NONCE'] = nonce
    #         headers['ACCESS-KEY'] = partner_id
    #         r = session.request('POST', url='{}/accounts/{}/unlink'.format(self.url, account_id), data=json.dumps(data), headers=headers)
    #         logger.info('r.json的返回值是{}'.format(r.json())
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)


    @allure.title('test_account_002')
    @allure.description('获取用户绑定关系新（通过infinni games账号获取cabital信息）')
    def test_account_002(self):
        with allure.step("获取cabital账号link infinni games账号"):
            params = {
                'partner_ids': get_json()['infinni_games']['partner_id'],
                'user_ext_ref': '',
                'link_mode': ''
            }
            r = session.request('GET', url='{}/connect/account/links'.format(self.url), params=params, headers=headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['list'][0]['partner_id'] == params['partner_ids'], "获取cabital账号link infinni games账号错误，返回值是{}".format(r.text)
                assert r.json()['list'][0]['account_links'][2]['user_ext_ref'] == get_json()['infinni_games']['uid_A'], "获取cabital账号link infinni games账号错误，返回值是{}".format(r.text)

    @allure.title('test_account_003')
    @allure.description('获取用户绑定关系旧接口（通过infinni games账号获取cabital信息）')
    def test_account_003(self):
        with allure.step("获取cabital账号link infinni games账号"):
            params = {
                'partner_id': get_json()['infinni_games']['partner_id']
            }
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), params=params, headers=headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['account_bindings'][0]['partner_name'] == 'Yeeha Games', "获取cabital账号link infinni games账号错误，返回值是{}".format(r.text)

    @allure.title('test_account_004')
    @allure.description('获取partner userinfo')
    def test_account_004(self):
        with allure.step("获取infinni games账号信息"):
            params = {
                'partner_id': get_json()['infinni_games']['partner_id'],
                'user_ext_ref': get_json()['infinni_games']['uid_A']
            }
            r = session.request('GET', url='{}/connect/partner/user/info'.format(self.url), params=params, headers=headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['email'] == 'zcdsw@sina.com', "获取infinni games账号信息错误,返回值是{}".format(r.text)

    # @allure.title('test_account_005')
    # @allure.description('cabital unlink解绑成功（改account_vid）')
    # def test_account_005(self):
    #     headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='test1027@163.com')
    #     partner_id = get_json()["infinni_games"]["partner_id"]
    #     with allure.step("获得data"):
    #         data = {
    #             'account_vid': 'c713ddf2-895e-4ef5-b123-98e035ad0967'
    #         }
    #         r = session.request('POST', url='{}/connect/account/{}/unlink'.format(env_url, partner_id), data=json.dumps(data), headers=headers)
    #         print(r.json())
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert r.json()['link_status'] == 3, "http 状态码不对，目前状态码是{}".format(r.json()['link_status'])
    #
    # @allure.title('test_account_006')
    # @allure.description('cabital 单一用户link成功（改account&uid）')
    # def test_account_006(self):
    #     headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='test1027@163.com')
    #     partner_id = get_json()["infinni_games"]["partner_id"]
    #     with allure.step("获得data"):
    #         data = {
    #             'user_ext_ref': '992025900348358656'
    #         }
    #         r = session.request('POST', url='{}/connect/account/{}/link'.format(env_url, partner_id), data=json.dumps(data), headers=headers)
    #         print(r.json())
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert r.json()['link_status'] == 2, "http 状态码不对，目前状态码是{}".format(r.json()['link_status'])