from Function.api_function import *
from Function.operate_sql import *


# Faas相关cases
class TestFaasApi:

    url = get_json()['faas'][get_json()['env']]['url']
    headers = get_json()['faas'][get_json()['env']]['Headers']

    @allure.testcase('test_faas_001 获取报价')
    def test_faas_001(self):
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
                    assert r.json()['ask'] is not None, "获取报价错误，返回值是{}".format(r.text)


