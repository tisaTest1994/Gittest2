from Function.api_function import *
from Function.operate_sql import *


# Connect相关cases
class TestWalletApi:

    url = get_json()['connect'][get_json()['env']]['url']
    ApiFunction.add_headers()

    @allure.testcase('test_connect_001 账户可用余额列表')
    def test_connect_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/balances'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['balances'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
        with allure.step("判断提供给bybit的和我们自用的值一致"):
            balance_list = ApiFunction.balance_list()
            for i in balance_list:
                mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
                for y in r.json()['balances']:
                    if y['code'] == i:
                        bybit_balance = y['balances']
                        assert mobile_balance == bybit_balance, '币种{}判断提供给bybit的和我们自用的值一致失败，我们自用balance是{},bybit是{}'.format(i, mobile_balance, bybit_balance)

    @allure.testcase('test_connect_002 账户可用余额单币')
    def test_connect_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得balance list"):
            balance_list = ApiFunction.balance_list()
        with allure.step("循环获取单币种"):
            for i in balance_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}'.format(account_id, i),
                                                        nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("账户可用余额列表"):
                    r = session.request('GET', url='{}/api/v1/accounts/{}/balances'.format(self.url, account_id),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['balances'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)

