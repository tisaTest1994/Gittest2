from Function.api_function import *
from Function.operate_sql import *


# Connect相关cases
class TestConnectTransactionApi:

    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.testcase('test_connect_transaction_001 获取报价')
    def test_connect_transaction_001(self):
        with allure.step("获取报价"):
            for i in get_json()['cfx_book'].values():
                with allure.step("获取正向报价"):
                    r = session.request('GET', url='{}/api/v1/quotes/{}'.format(self.url, i), headers=connect_headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)
                with allure.step("获取反向报价"):
                    new_pair = '{}{}{}'.format(i.split('-')[1], '-', i.split('-')[0])
                    r = session.request('GET', url='{}/api/v1/quotes/{}'.format(self.url, new_pair), headers=connect_headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['quote'] is not None, "获取报价错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_002 获取合作方的配置')
    def test_connect_transaction_002(self):
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/api/v1/config'.format(self.url), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '{"currencies":[{"symbol":"ETH","type":2,"deposit_methods":["ERC20"],"withdraw_methods":["ERC20"],"config":{"credit":{"allow":true,"min":"0.02","max":"0"},"debit":{"allow":true,"min":"0","max":"0"},"conversion":{"allow":true,"min":"0.002","max":"100"}}},{"symbol":"BTC","type":2,"deposit_methods":["ERC20"],"withdraw_methods":["ERC20"],"config":{"credit":{"allow":true,"min":"0.001","max":"0"},"debit":{"allow":true,"min":"0","max":"0"},"conversion":{"allow":true,"min":"0.0002","max":"5"}}},{"symbol":"USDT","type":2,"deposit_methods":["ERC20"],"withdraw_methods":["ERC20"],"config":{"credit":{"allow":true,"min":"40","max":"0"},"debit":{"allow":true,"min":"0","max":"0"},"conversion":{"allow":true,"min":"10","max":"200000"}}},{"symbol":"EUR","type":1,"deposit_methods":["SEPA"],"withdraw_methods":["SEPA"],"config":{"credit":{"allow":true,"min":"25","max":"50000"},"debit":{"allow":true,"min":"0","max":"0"},"conversion":{"allow":true,"min":"10","max":"200000"}}},{"symbol":"GBP","type":1,"deposit_methods":["FPS"],"withdraw_methods":["FPS"],"config":{"credit":{"allow":true,"min":"20","max":"40000"},"debit":{"allow":true,"min":"0","max":"0"},"conversion":{"allow":true,"min":"10","max":"200000"}}}],"pairs":[{"pair":"BTC-EUR"},{"pair":"ETH-EUR"},{"pair":"EUR-USDT"},{"pair":"BTC-GBP"},{"pair":"ETH-GBP"},{"pair":"GBP-USDT"},{"pair":"BTC-ETH"},{"pair":"BTC-USDT"},{"pair":"ETH-USDT"}]}' == r.text, "获取合作方的配置错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_003 账户划转列表（不传默认参数）')
    def test_connect_transaction_003(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cbb4568f-ee69-4701-83d4-a6975a852c58'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/transfers'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['pagination_response'] is not None, "账户划转列表错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_004 账户划转列表(传入部分参数）')
    def test_connect_transaction_004(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cbb4568f-ee69-4701-83d4-a6975a852c58'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers?page_size=30&has_conversion=false&symbol=ETH&direction=DEBIT'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/transfers?page_size=30&has_conversion=false&symbol=ETH&direction=DEBIT'.format(self.url, account_id),  headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['pagination_response'] is not None, "账户划转列表（传入部分参数）错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_005 账户划转详情')
    def test_connect_transaction_005(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cbb4568f-ee69-4701-83d4-a6975a852c58'
            transfer_id = "f5946953-d422-4c54-846f-789fafd1c2b2"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfer_id'] == transfer_id, "账户划转详情错误，返回值是{}".format(r.text)

    # @allure.testcase('test_connect_transaction_006 把钱从我们这里转移到bybit账户')
    # def test_connect_transaction_006(self):
    #     with allure.step("测试用户的account_id"):
    #         account_id = 'cbb4568f-ee69-4701-83d4-a6975a852c58'
    #         transfer_id = "f5946953-d422-4c54-846f-789fafd1c2b2"
    #     with allure.step("验签"):
    #         unix_time = int(time.time())
    #         nonce = generate_string(30)
    #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id), nonce=nonce)
    #         connect_headers['ACCESS-SIGN'] = sign
    #         connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
    #         connect_headers['ACCESS-NONCE'] = nonce
    #     with allure.step("账户划转列表"):
    #         r = session.request('GET', url='{}/api/v1/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id), headers=connect_headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
    #     with allure.step("校验返回值"):
    #         assert r.json()['transfer_id'] == transfer_id, "账户划转详情错误，返回值是{}".format(r.text)