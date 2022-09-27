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
    @allure.description('获取用户关联信息（通过user_ext_ref获取对应cabital详细信息）')
    def test_account_001(self, partner):
        with allure.step("获取cabital账号link partner账号"):
            user_ext_ref = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['user_ref_id']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(20) + str(time.time()).split('.')[0]
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/partner/links/{}'.format(user_ext_ref), connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                'Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
            r = session.request('GET', url='{}/partner/links/{}'.format(self.url, user_ext_ref), headers=connect_headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['email_address'] == 'richard.wan@cabital.com', "获取用户关联信息（通过user_ext_ref获取对应cabital详细信息）错误，目前返回值是{}".format(r.text)

    @allure.title('test_account_002')
    @allure.description('获取用户关联状况（通过account_vid获取cabital邮箱）')
    def test_account_002(self, partner):
        with allure.step("获取cabital账号link partner账号"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(20) + str(time.time()).split('.')[0]
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_vid), connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
            r = session.request('GET', url='{}/accounts/{}/detail'.format(connect_url, account_vid), headers=connect_headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['email_address'] == 'richard.wan@cabital.com', "获取用户关联信息（通过account_vid获取cabital邮箱）错误，目前返回值是{}".format(r.text)

