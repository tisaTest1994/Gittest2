from Function.api_function import *
from Function.operate_sql import *


# convert相关cases
class TestConnectApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.testcase('test_connect_001 获取合作方配置')
    def test_connect_001(self):
        with allure.step("获取合作方配置"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(self.url, get_json()['connect'][
                get_json()['env']]['Headers']['ACCESS-KEY']), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['crypto'] is not None, "获取合作方配置错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_002 transfe 预校验')
    def test_connect_002(self):
        with allure.step("获取合作方配置"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(self.url, get_json()['connect'][
                get_json()['env']]['Headers']['ACCESS-KEY']), headers=headers)
            for i in r.json()['crypto']:
                amount = str(float(i['withdraw']['amount_limit']['min']) + float(0.002))
                data = {
                    "amount": amount,
                    "symbol": i['symbol'],
                    "direction": "DEBIT"
                }
