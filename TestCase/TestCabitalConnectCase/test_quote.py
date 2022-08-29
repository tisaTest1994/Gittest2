from Function.api_function import *
from Function.operate_sql import *


# 获取最新的报价
class TestQuoteApi:

    @allure.title('test_quotes_001')
    @allure.description('获取报价最新的报价')
    def test_quotes_001(self, partner):
        with allure.step("签名"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/config', connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/config'.format(connect_url), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("获取最新的报价"):
            new_list = []
            for i in r.json()['pairs']:
                new_list.append(i['pair'])
            for i in new_list:
                with allure.step("获取正向报价"):
                    with allure.step("签名"):
                        unix_time = int(time.time())
                        nonce = generate_string(30)
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/quotes/{}'.format(i),
                                                          connect_type=partner, nonce=nonce)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    r = session.request('GET', url='{}/quotes/{}'.format(connect_url, i), headers=connect_headers)
                    logger.info('币种对为{}'.format(i))
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)
