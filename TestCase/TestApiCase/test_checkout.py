from Function.api_function import *
from Function.operate_sql import *
from Function.operate_excel import *


@allure.feature("Check out 相关 testcases")
class TestCheckoutApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_check_out_001')
    @allure.description('打开数字货币购买画面接口')
    def test_check_out_001(self):
        with allure.step("BRL法币充值账户信息"):
            r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("获取接口返回的所有币种并放入list中"):
                payment_currencies = r.json()['payment_currencies']
                print(payment_currencies)
            with allure.step("读取product limit中35个币种buy的limit"):
                for i in OperateExcel.get_product_limit():
                    if i['transaction_type'] == 'Buy':
                        for j in range(0, len(payment_currencies)):
                            if i['code'] in payment_currencies[j]:
                                assert i['min'] == j['min']

    @allure.title('test_check_out_051')
    @allure.description('查询用户使用过的所有卡')
    def test_check_out_051(self):
        with allure.step("查询用户使用过的所有卡"):
            params = {
                'binding': 'false'
            }
            r = session.request('GET', url='{}/acquiring/cards'.format(env_url), headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_check_out_052')
    @allure.description('删除用户是用过的卡')
    def test_check_out_052(self):
        with allure.step("删除用户是用过的卡"):
            params = {
                'token_id': 'false'
            }
            r = session.request('DELETE', url='{}/acquiring/cards/{}'.format(env_url, params['token_id']), headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)






