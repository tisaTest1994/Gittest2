from Function.api_function import *
from run import *
from Function.log import *
import allure


# pay in相关cases
class TestPayInApi:

    @allure.testcase('test_pay_in_001 查询转入记录（不指定链）')
    def test_pay_in_001(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询转入记录"):
            currency = ['USDT', 'BTC', 'ETH']
            data = {}
            for i in currency:
                data['code'] = i
                r = requests.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data,
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == [] or 'code' in r.text, "查询转入记录（不指定链）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_002 查询不到转入记录（使用错误币种）')
    def test_pay_in_002(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询不到转入记录"):
            data = {
                'code': 'US345'
            }
            r = requests.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'method is not support message' in r.text, "查询不到转入记录（使用错误币种）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_003 查询转入记录（使用转币链查询）')
    def test_pay_in_003(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询转入记录"):
            data = {
                'code': 'ETH',
                'method': 'ERC20'
            }
            r = requests.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'ERC20' in r.text, "查询转入记录（使用转币链查询）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_004 查询转入记录（使用错误转币链查询）')
    def test_pay_in_004(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询转入记录"):
            data = {
                'code': 'ETH',
                'method': 'ER124141'
            }
            r = requests.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'method is not support message' in r.text, "查询转入记录（使用错误转币链查询）错误，返回值是{}".format(r.text)
