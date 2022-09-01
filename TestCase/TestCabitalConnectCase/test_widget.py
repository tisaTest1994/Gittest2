from Function.api_function import *
from Function.operate_sql import *


# Convert相关cases
class TestWidgetApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_widget_001')
    @allure.description('不传入partner_id, 取得全部conversion limit')
    def test_widget_001(self):
        with allure.step("不传入partner_id, 取得全部conversion limit"):
            params = {
                'partner_id': ''
            }
            r = session.request('GET', url='{}/connect/conversion/limits'.format(env_url), params=params,
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json() == {"limits": {"BRL": {"min": "50", "max": "1000000"}, "BTC": {"min": "0.0002", "max": "5"},
                                           "CHF": {"min": "10", "max": "200000"}, "ETH": {"min": "0.002", "max": "100"},
                                           "EUR": {"min": "10", "max": "200000"}, "GBP": {"min": "10", "max": "200000"},
                                           "USDT": {"min": "10", "max": "200000"},
                                           "VND": {"min": "250000", "max": "5000000000"}}}, '不传入partner_id, 取得全部conversion limit错误，返回值是{}'.format(r.text)

    @allure.title('test_widget_001')
    @allure.description('传入partner_id, 取得全部conversion limit')
    def test_widget_001(self, partner):
        with allure.step("传入partner_id, 取得全部conversion limit"):
            params = {
                'partner_id': get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            }
            r = session.request('GET', url='{}/connect/conversion/limits'.format(env_url), params=params,
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("验证数据是否和config一致"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                for y in r.json()['limits']:
                    if i['symbol'] == y:
                        config_conversion = i['config']['conversion']
                        del config_conversion['allow']
                        assert r.json()['limits'][y] == config_conversion, '传入partner_id, 取得全部conversion limit错误，币种是{}, config 配置内的值是{}, 接口返回值是{}'.format(y, config_conversion, r.json()['limits'][y])
