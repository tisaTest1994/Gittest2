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

    @allure.title('test_account_partner_001')
    @allure.description('获取用户关联信息（通过user_ext_ref获取对应cabital详细信息）')
    def test_account_partner_001(self):
        with allure.step("获取cabital账号link infinni games账号"):
            user_ext_ref = get_json()['infinni_games']['uid_A']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/partner/links/{}'.format(user_ext_ref),
                                                key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']
            r = session.request('GET', url='{}/partner/links/{}'.format(self.url, user_ext_ref), headers=headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_account_partner_002')
    @allure.description('获取用户关联状况（通过account_vid获取cabital邮箱）')
    def test_account_partner_002(self):
        with allure.step("获取cabital账号link infinni games账号"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/detail'.format(account_id),
                                                key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)