from Function.api_function import *
from Function.operate_sql import *


# 获取最新的报价
class TestQuoteApi:

    @allure.title('test_quotes_001')
    @allure.description('寻价')
    def test_quotes_001(self, partner):
        with allure.step("签名"):
            unix_time = int(time.time())
            nonce = generate_string(20) + str(time.time()).split('.')[0]
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET', url='/api/v1/config',
                                              connect_type=partner, nonce=nonce)
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
                    r = session.request('GET', url='{}/quotes/{}'.format(connect_url, i), headers=connect_headers)
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
                    r = session.request('GET', url='{}/quotes/{}'.format(connect_url, new_pair),
                                        headers=connect_headers)
                    logger.info('币种对为{}'.format(new_pair))
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)

    @allure.title('test_quotes_002')
    @allure.description('换汇批量寻价')
    def test_quotes_002(self, partner):
        with allure.step("获取需要寻价的币种"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                params = {
                    'target': i['symbol'],
                    'transaction_type': 'CONVERSION'
                }
                with allure.step("签名"):
                    unix_time = int(time.time())
                    nonce = generate_string(20) + str(time.time()).split('.')[0]
                    sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET',
                                                      url='/api/v1/connect/prices',
                                                      connect_type=partner, nonce=nonce, body=params)
                    connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                        'Partner_ID']
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("换汇批量寻价"):
                    r = session.request('GET', url='{}/connect/prices'.format(connect_url), params=params,
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['target'] == i['symbol'], "获取报价错误，返回值是{}".format(r.text)

    @allure.title('test_quotes_003')
    @allure.description('cabital buy批量寻价,指定法币')
    def test_quotes_003(self, partner):
        with allure.step("获取需要寻价的币种"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['buy']['fiat']:
                for y in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['buy']['crypto']:
                    params = {
                        'target': y['symbol'],
                        'source': i['symbol'],
                        'transaction_type': 'BUY'
                    }
                    with allure.step("签名"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET',
                                                          url='/api/v1/connect/prices',
                                                          connect_type=partner, nonce=nonce, body=params)
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("换汇批量寻价"):
                        r = session.request('GET', url='{}/connect/prices'.format(connect_url), params=params,
                                            headers=connect_headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['target'] == y['symbol'], "cabital buy批量寻价,指定法币错误，返回值是{}".format(r.text)
                        assert list((r.json()['sources']).keys())[0] == i[
                            'symbol'], "cabital buy批量寻价,指定法币错误，返回值是{}".format(r.text)

    @allure.title('test_quotes_004')
    @allure.description('cabital buy批量寻价,不指定法币，获取全部报价')
    def test_quotes_004(self, partner):
        with allure.step("获取需要寻价的币种"):
            for y in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['buy']['crypto']:
                params = {
                    'target': y['symbol'],
                    'transaction_type': 'BUY'
                }
                with allure.step("签名"):
                    unix_time = int(time.time())
                    nonce = generate_string(20) + str(time.time()).split('.')[0]
                    sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET',
                                                      url='/api/v1/connect/prices',
                                                      connect_type=partner, nonce=nonce, body=params)
                    connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                        'Partner_ID']
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("换汇批量寻价"):
                    r = session.request('GET', url='{}/connect/prices'.format(connect_url), params=params,
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['target'] == y['symbol'], "cabital buy批量寻价,不指定法币，获取全部报价错误，返回值是{}".format(r.text)
                    for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['buy']['fiat']:
                        assert r.json()['sources'][i['symbol']] is not None, "cabital buy批量寻价,不指定法币，获取全部报价错误，返回值是{}".format(r.text)
