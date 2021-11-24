from Function.api_function import *
from Function.operate_sql import *


# Connect相关cases
class TestConnectApi:

    url = get_json()['connect'][get_json()['env']]['url']
    headers = get_json()['connect'][get_json()['env']]['Headers']

    @allure.testcase('test_connect_001 获取报价')
    def test_connect_001(self):
        headers = self.headers
        for i in get_json()['cfx_book'].values():
            with allure.step("获取正向报价"):
                unix_time = int(time.time())
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/quotes/{}'.format(i))
                headers['ACCESS-SIGN'] = sign
                headers['ACCESS-TIMESTAMP'] = str(unix_time)
                r = session.request('GET', url='{}/api/v1/quotes/{}'.format(self.url, i), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)
            with allure.step("获取反向报价"):
                unix_time = int(time.time())
                i.split('-')
                new_pair = '{}{}{}'.format(i.split('-')[1], '-', i.split('-')[0])
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/quotes/{}'.format(new_pair))
                headers['ACCESS-SIGN'] = sign
                headers['ACCESS-TIMESTAMP'] = str(unix_time)
                r = session.request('GET', url='{}/api/v1/quotes/{}'.format(self.url, new_pair), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_002 获取合作方的配置')
    def test_connect_002(self):
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
            print(headers)
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/api/v1/config'.format(self.url), headers=headers)
            print(r.text)

