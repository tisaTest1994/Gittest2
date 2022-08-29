from Function.api_function import *
from Function.operate_sql import *


# 获取合作方的配置
class TestConfigApi:
    connect_header = {
        "Content-Type": "application/json"
    }

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_config_001')
    @allure.description('获得config')
    def test_config_001(self, partner):
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config',
                                                nonce=nonce)
            connect_header['ACCESS-SIGN'] = sign
            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_header['ACCESS-NONCE'] = nonce
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/config'.format(connect_url), headers=connect_header)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['currencies'] is not None, 'config相关配置错误, 返回值是{}'.format(r.text)