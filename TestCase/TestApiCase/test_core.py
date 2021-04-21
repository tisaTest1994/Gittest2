from Function.api_function import *
from run import *
from Function.log import *
import allure


# core相关cases
class TestCoreApi:

    @allure.testcase('test_core_001 查询钱包所有币种详细金额以及报价，以美元价格返回')
    def test_core_001(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'USD'
        with allure.step("查询钱包所有币种详细金额以及报价，以美元价格返回"):
            r = requests.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'wallets' in r.text, "查询钱包所有币种详细金额以及报价，以美元价格返回错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_002 查询钱包所有币种金额')
    def test_core_002(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包所有币种金额"):
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'id' in r.text, "查询钱包所有币种金额错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_003 查询钱包某个币种的详细信息')
    def test_core_003(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包某个币种的详细信息"):
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
            id = r.json()[0]["id"]
        with allure.step("查询钱包某个币种"):
            r = requests.request('GET', url='{}/core/account/wallets/{}'.format(env_url, id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['id'] is not None, "查询钱包某个币种的详细信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_004 查询货币兑换比例')
    def test_core_004(self):
        List = ['BTC-ETH', 'BTC-USDT', 'BTC-GBP', 'BTC-EUR', 'ETH-USDT', 'ETH-GBP', 'ETH-EUR', 'USDT-GBP', 'USDT-EUR']
        with allure.step("查询货币兑换比例"):
            for i in List:
                with allure.step("查询{}兑换比例".format(i)):
                    r = requests.request('GET', url='{}/core/quotes/{}'.format(env_url, i), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['quote'] != {}, " 查询货币兑换比例错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_005 查询钱包中的所有币种投资于SAVING中的金额')
    def test_core_005(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包中的所有币种投资于SAVING中的金额"):
            params = {
                'type': 'SAVING'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'SAVING' in r.text, "查询钱包中的所有币种投资于SAVING中的金额错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_006 查询钱包中的所有币种投资于BALANCE中的金额')
    def test_core_006(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包中的所有币种投资于BALANCE中的金额"):
            params = {
                'type': 'BALANCE'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BALANCE' in r.text, "查询钱包中的所有币种投资于BALANCE中的金额错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_007 查询钱包BTC金额')
    def test_core_007(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包BTC金额"):
            params = {
                'code': 'BTC'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BTC' in r.text, "查询钱包BTC金额错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_008 查询钱包ETH金额')
    def test_core_008(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包ETH金额"):
            params = {
                'code': 'ETH'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ETH' in r.text, "查询钱包ETH金额错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_009 查询钱包USDT金额')
    def test_core_009(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包USDT金额"):
            params = {
                'code': 'USDT'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'USDT' in r.text, "查询钱包USDT金额错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_010 查询钱包所有币种详细金额以及报价，以欧元价格返回')
    def test_core_010(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
            headers['X-Currency'] = 'EUR'
        with allure.step("查询钱包所有币种详细金额以及报价，以欧元价格返回"):
            r = requests.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'wallets' in r.text, "查询钱包所有币种详细金额以及报价，以欧元价格返回错误，返回值是{}".format(r.text)