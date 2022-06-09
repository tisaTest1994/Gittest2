from Function.api_function import *
from Function.operate_sql import *


# Convert相关cases
class TestConvertApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'
        with allure.step("ACCESS-KEY"):
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

    @allure.title('test_currency_quotes_001')
    @allure.description('获取报价最新的报价')
    def test_currency_quotes_001(self):
        with allure.step("获取最新的报价"):
            for i in get_json()['cfx_book'].values():
                with allure.step("获取正向报价"):
                    r = session.request('GET', url='{}/quotes/{}'.format(self.url, i), headers=connect_headers)
                    logger.info('币种对为{}'.format(i))
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)
                with allure.step("获取反向报价"):
                    new_pair = '{}{}{}'.format(i.split('-')[1], '-', i.split('-')[0])
                    r = session.request('GET', url='{}/quotes/{}'.format(self.url, new_pair),
                                        headers=connect_headers)
                    logger.info('币种对为{}'.format(new_pair))
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)


