from Function.api_function import *
from Function.operate_sql import *


# Balance相关cases
class TestBalanceApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'
        with allure.step("ACCESS-KEY"):
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

    @allure.title('test_config_001')
    @allure.description('connect获取合作方的config')
    def test_config_001(self):
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', key='infinni games',nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/config'.format(self.url), headers=headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['currencies'] is not None, 'config相关配置错误, 返回值是{}'.format(r.text)


