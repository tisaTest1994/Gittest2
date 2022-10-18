from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api pay in crypto相关 testcases")
class TestPayInCryptoApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_pay_in_crypto_001')
    @allure.description('查询数字货币转入地址')
    def test_pay_in_crypto_001(self):
        with allure.step("查询转入记录"):
            currency = get_json()['crypto_list']
            data = {
                'code': '',
                'chain': ''
            }
            for i in currency:
                data['code'] = i
                if i == 'USD':
                    data['code'] = 'USDC'
                    data['chain'] = 'ETH'
                    r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data,
                                        headers=headers)
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()[0]['code'] == 'USDC', "查询数字货币转入地址错误，返回值是{}".format(r.text)
                else:
                    r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()[0]['code'] == i, "查询数字货币转入地址错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_crypto_002')
    @allure.description('使用错误币种查询数字货币转入地址')
    def test_pay_in_crypto_002(self):
        with allure.step("国际化"):
            for i in get_json()['language_list']:
                headers['locale'] = i
                with allure.step("使用错误币种查询数字货币转入地址"):
                    params = {
                        'code': 'US345'
                    }
                    r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=params,
                                        headers=headers)
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['code'] == '103021', "使用错误币种查询数字货币转入地址错误，返回值是{}".format(r.text)
                        assert r.json()['message'] == 'Invalid code', "使用错误币种查询数字货币转入地址错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_crypto_003')
    @allure.description('使用指定链ETH查询数字货币转入地址')
    def test_pay_in_crypto_003(self):
        with allure.step("查询转入记录"):
            data = {
                'code': 'ETH',
                'chain': 'ETH'
            }
            r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()[0]['code'] == data['code'], "使用指定链ETH查询数字货币转入地址错误，返回值是{}".format(r.text)

    # @allure.title('test_pay_in_crypto_004')
    # @allure.description('使用指定链TRX查询数字货币转入地址')
    # def test_pay_in_crypto_004(self):
    #     with allure.step("查询转入记录"):
    #         data = {
    #             'code': 'ETH',
    #             'chain': 'TRX'
    #         }
    #         r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
    #         with allure.step("状态码和返回值"):
    #             logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
    #             logger.info('状态码是{}'.format(str(r.status_code)))
    #             logger.info('返回值是{}'.format(str(r.text)))
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert r.json()[0]['code'] == data['code'], "使用指定链查询数字货币转入地址错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_crypto_005')
    @allure.description('使用错误链查询数字货币转入地址')
    def test_pay_in_crypto_005(self):
        with allure.step("查询转入记录"):
            data = {
                'code': 'ETH',
                'chain': 'ER124141'
            }
            r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103057', "查询不到转入地址记录（使用错误链查询）错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_crypto_006')
    @allure.description('获得数字货币充值币种')
    def test_pay_in_crypto_006(self):
        with allure.step("充值币种"):
            r = session.request('GET', url='{}/pay/deposit/ccy/{}'.format(env_url, 'crypto'), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                for i in get_json()['crypto_list']:
                    assert i in str(r.json()['crypto']), "获得法币充值币种错误，返回值是{}".format(r.text)

    @allure.title('test_pay_in_crypto_007')
    @allure.description('使用指定链ETH查询数字货币USDC转入地址')
    def test_pay_in_crypto_007(self):
        with allure.step("查询转入记录"):
            data = {
                'code': 'USDC',
                'chain': 'ETH'
            }
            r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()[0]['code'] == data['code'], "使用指定链ETH查询数字货币USDC转入地址错误，返回值是{}".format(r.text)