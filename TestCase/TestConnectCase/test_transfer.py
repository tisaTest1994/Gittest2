from Function.api_function import *
from Function.operate_sql import *


# 账户划转相关cases
class TestTransferApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_transfer_001')
    @allure.description('账户划转列表（不传默认参数）')
    def test_transfer_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfers'] is not None, "账户划转列表错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_002')
    @allure.description('账户划转列表(传入部分参数）')
    def test_transfer_002(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers?page_size=30&has_conversion=false&symbol=ETH&direction=DEBIT'.format(
                                                    account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET',
                                url='{}/accounts/{}/transfers?page_size=30&has_conversion=false&symbol=ETH&direction=DEBIT'.format(
                                    self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfers'] is not None, "账户划转列表（传入部分参数）错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_003')
    @allure.description('没有通过kyc的账户划转列表（不传默认参数）失败')
    def test_transfer_003(self):
        with allure.step("测试用户的account_id"):
            account_id = "eb9659ea-0d95-4f0f-83a3-1152c5a90ee9"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("没有通过kyc的账户划转列表（不传默认参数）失败"):
            r = session.request('GET', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfers'] is None, "没有通过kyc的账户划转列表（不传默认参数）失败错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_004')
    @allure.description('把数字货币从cabital转移到bybit账户（小于单比最小限额）')
    def test_transfer_004(self):
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
                        with allure.step("获得otp"):
                            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min']) - float(0.0001)),
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
                            }
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
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA003', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                        r.text)

    @allure.title('test_transfer_005')
    @allure.description('从cabital转移到bybit账户使用错误otp')
    def test_transfer_005(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得data"):
            data = {
                'amount': '0.012',
                'symbol': 'BTC',
                'otp': '123456',
                'direction': 'DEBIT',
                'external_id': generate_string(15),
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce,
                                                body=json.dumps(data))
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("把BTC从cabital转移到bybit账户并且关联C+T交易"):
            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                data=json.dumps(data), headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'PA008', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_006')
    @allure.description('bybit发起请求，把资金从cabital转移到bybit账户')
    def test_transfer_006(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce,
                                                body=json.dumps(data))
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                data=json.dumps(data), headers=connect_headers)
            logger.info('r.json()返回值是{}'.format(r.json()))
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
            r = session.request('GET', url='{}/recon/transfers/{}'.format(self.url, external_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['external_id'] == external_id, "查询转账记录错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_007')
    @allure.description('从cabital转移到bybit账户并且关联C+T交易')
    def test_transfer_007(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("换汇"):
            for i in ApiFunction.get_connect_cfx_list(self.url, connect_headers):
                with allure.step('换汇'):
                    transaction = ApiFunction.cfx_random(i, i.split('-')[0])
                    cfx_transaction_id = transaction['returnJson']['transaction']['transaction_id']
                with allure.step("获得otp"):
                    mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
                with allure.step("获得data"):
                    if i.split('-')[0] in get_json()['crypto_list']:
                        symbol = i.split('-')[0]
                    else:
                        symbol = i.split('-')[1]
                    data = {
                        'amount': transaction['data']['buy_amount'],
                        'symbol': symbol,
                        'otp': str(mfaVerificationCode),
                        'direction': 'DEBIT',
                        'external_id': generate_string(15),
                        'conversion_id': cfx_transaction_id
                    }
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                        url='/api/v1/accounts/{}/transfers'.format(
                                                            account_id),
                                                        nonce=nonce,
                                                        body=json.dumps(data))
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("把BTC从cabital转移到bybit账户并且关联C+T交易"):
                    r = session.request('POST',
                                        url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                        data=json.dumps(data), headers=connect_headers)
                    logger.info('r.json返回值是{}'.format(r.json()))
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    if r.status_code == 200:
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['status'] == 'SUCCESS', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(r.text)
                    else:
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA043', "关联C+T交易错误，返回值是{}".format(
                            r.text)





