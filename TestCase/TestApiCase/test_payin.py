from Function.api_function import *
from Function.operate_sql import *


# pay in相关cases
class TestPayInApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.testcase('test_pay_in_001 查询转入地址记录（不指定链）')
    @pytest.mark.multiprocess
    def test_pay_in_001(self):
        with allure.step("查询转入记录"):
            currency = ['USDT', 'BTC', 'ETH']
            data = {}
            for i in currency:
                data['code'] = i
                r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == [] or 'code' in r.text, "查询查询转入地址记录（不指定链）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_002 查询不到转入地址记录（使用错误币种）')
    @pytest.mark.multiprocess
    def test_pay_in_002(self):
        with allure.step("查询不到转入记录"):
            params = {
                'code': 'US345'
            }
            r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103003', "查询不到转入地址记录（使用错误币种）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_003 查询转入地址记录（指定链）')
    @pytest.mark.multiprocess
    def test_pay_in_003(self):
        with allure.step("查询转入记录"):
            data = {
                'code': 'ETH',
                'method': 'ERC20'
            }
            r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'ERC20' in r.text, "查询转入地址记录（指定链）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_004 查询不到转入地址记录（使用错误链查询）')
    @pytest.mark.multiprocess
    def test_pay_in_004(self):
        with allure.step("查询转入记录"):
            data = {
                'code': 'ETH',
                'method': 'ER124141'
            }
            r = session.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103003', "查询不到转入地址记录（使用错误链查询）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_005 获得法币充值币种')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_pay_in_005(self):
        with allure.step("充值币种"):
            r = session.request('GET', url='{}/pay/deposit/ccy/{}'.format(env_url, 'fiat'), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'fiat' in r.text, "获得法币充值币种错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_006 获得数字货币充值币种')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_pay_in_006(self):
        with allure.step("充值币种"):
            r = session.request('GET', url='{}/pay/deposit/ccy/{}'.format(env_url, 'crypto'), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'crypto' in r.text, "获得数字货币充值币种错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_007 获得全部货币充值币种')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_pay_in_007(self):
        with allure.step("充值币种"):
            r = session.request('GET', url='{}/pay/deposit/ccy/{}'.format(env_url, ''), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'crypto' in r.text, "获得全部货币充值币种错误，返回值是{}".format(r.text)
                assert 'fiat' in r.text, "获得全部货币充值币种错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_008 法币充值账户')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_pay_in_008(self):
        with allure.step("充值币种"):
            params = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/deposit/fiat'.format(env_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'Lithuania' in r.text, "法币充值账户错误，返回值是{}".format(r.text)
