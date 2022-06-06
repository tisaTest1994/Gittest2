from Function.api_function import *
from Function.operate_sql import *


# 对账-划转交易详情
class TestTransactionApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_transaction_001')
    @allure.description('先进行一笔交易后，查询转账记录')
    def test_connect_transaction_006(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得otp"):
            sleep(30)
            secretKey = get_json()['email']['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
        with allure.step("获得data"):
            external_id = generate_string(25)
            data = {
                    'amount': '0.02',
                    'symbol': 'ETH',
                    'otp': str(mfaVerificationCode),
                    'direction': 'DEBIT',
                    'external_id': external_id
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce, body=json.dumps(data))
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id), data=json.dumps(data), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/recon/transfers/{}'.format(external_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("查询转账记录"):
            r = session.request('GET', url='{}/recon/transfers/{}'.format(self.url, external_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['external_id'] == external_id, "查询转账记录错误，返回值是{}".format(r.text)

    @allure.title('test_transaction_002')
    @allure.description('对账 - 划转交易详情使用无效external_id')
    def test_transaction_002(self):
        external_id = generate_string(15)
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/recon/transfers/{}'.format(external_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("划转交易详情使用无效external_id"):
            r = session.request('GET', url='{}recon/transfers/{}'.format(self.url, external_id),headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'PA030', "对账 - 划转交易详情使用无效external_id错误，返回值是{}".format(r.text)
