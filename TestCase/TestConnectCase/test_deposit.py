from Function.api_function import *
from Function.operate_sql import *


# Deposit相关cases
class TestDepositApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_deposit_001 把数字货币从cabital转移到bybit账户')
    def test_deposit_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("从配置接口获取可以划转的数据"):
            with allure.step("验签"):
                unix_time = int(time.time())
                nonce = generate_string(30)
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config',
                                                    nonce=nonce)
                connect_headers['ACCESS-SIGN'] = sign
                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                connect_headers['ACCESS-NONCE'] = nonce
            with allure.step("获取合作方的配置"):
                r = session.request('GET', url='{}/config'.format(self.url), headers=connect_headers)
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得转移前cabital内币种balance金额"):
                            balance_old = ApiFunction.get_crypto_number(type=i['symbol'])
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': i['config']['debit']['min'],
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
                            }
                            logger.info('参数是{}'.format(data))
                        with allure.step("验签"):
                            unix_time = int(time.time())
                            nonce = generate_string(30)
                            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                                url='/api/v1/accounts/{}/transfers'.format(account_id),
                                                                nonce=nonce,
                                                                body=json.dumps(data))
                            connect_headers['ACCESS-SIGN'] = sign
                            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                            connect_headers['ACCESS-NONCE'] = nonce
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers, timeout=10)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['status'] == 'SUCCESS', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'], r.text)
                        with allure.step("获得转移后cabital内币种balance金额"):
                            sleep(30)
                            balance_latest = ApiFunction.get_crypto_number(type=i['symbol'])
                        assert Decimal(balance_old) - Decimal(data['amount']) == Decimal(
                            balance_latest), "把{}从cabital转移到bybit账户错误，转移前balance是{},转移后balance是{}".format(i['symbol'], balance_old, balance_latest)

    @allure.title('test_deposit_002 从cabital转移到bybit账户并且关联C+T交易')
    def test_deposit_002(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("换汇"):
            for i in ApiFunction.get_cfx_list():
                for y in get_json()['cash_list']:
                    if y in i:
                        with allure.step('换汇'):
                            transaction = ApiFunction.cfx_random(i, i.split('-')[0])
                        with allure.step("验签"):
                            unix_time = int(time.time())
                            nonce = generate_string(30)
                            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                                url='/api/v1/accounts/{}/conversions'.format(
                                                                    account_id),
                                                                nonce=nonce, body=json.dumps(transaction['data']))
                            connect_headers['ACCESS-SIGN'] = sign
                            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                            connect_headers['ACCESS-NONCE'] = nonce
                        with allure.step("账户可用余额列表"):
                            r = session.request('POST', url='{}/accounts/{}/conversions'.format(self.url, account_id),
                                                data=json.dumps(transaction['data']), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['transaction_id'] is not None, "换汇错误，返回值是{}".format(r.text)
                            assert r.json()['status'] == 'Success', "换汇错误，返回值是{}".format(r.text)
                            cfx_transaction_id = r.json()['transaction_id']
                        sleep(5)
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': transaction['data']['buy_amount'],
                                'symbol': i.split('-')[0],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15),
                                'conversion_id': cfx_transaction_id
                            }
                            print(data)
                        with allure.step("验签"):
                            unix_time = int(time.time())
                            nonce = generate_string(30)
                            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                                url='/api/v1/accounts/{}/transfers'.format(account_id),
                                                                nonce=nonce,
                                                                body=json.dumps(data))
                            connect_headers['ACCESS-SIGN'] = sign
                            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                            connect_headers['ACCESS-NONCE'] = nonce
                        with allure.step("把BTC从cabital转移到bybit账户并且关联C+T交易"):
                            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['status'] == 'SUCCESS', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(
                                r.text)
                            sleep(30)
