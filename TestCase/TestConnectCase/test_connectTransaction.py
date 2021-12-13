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
                    r = session.request('GET', url='{}/api/v1/quotes/{}'.format(self.url, new_pair),
                                        headers=connect_headers)
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config',
                                                nonce=nonce)
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
            assert r.json()['currencies'] is not None, "获取合作方的配置错误，返回值是{}".format(r.text)

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
                                                url='/api/v1/accounts/{}/transfers?page_size=30&has_conversion=false&symbol=ETH&direction=DEBIT'.format(
                                                    account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET',
                                url='{}/api/v1/accounts/{}/transfers?page_size=30&has_conversion=false&symbol=ETH&direction=DEBIT'.format(
                                    self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['pagination_response'] is not None, "账户划转列表（传入部分参数）错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_005 没有通过kyc的账户划转列表（不传默认参数）失败')
    def test_connect_transaction_005(self):
        with allure.step("测试用户的account_id"):
            account_id = '90da0a64-4871-4d7e-b4a5-c80bf4ec9d5e'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("没有通过kyc的账户划转列表（不传默认参数）失败"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/transfers'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'PA009', "没有通过kyc的账户划转列表（不传默认参数）失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_006 账户划转详情')
    def test_connect_transaction_006(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cbb4568f-ee69-4701-83d4-a6975a852c58'
            transfer_id = "f5946953-d422-4c54-846f-789fafd1c2b2"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转列表"):
            r = session.request('GET',
                                url='{}/api/v1/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfer_id'] == transfer_id, "账户划转详情错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_007 账户划转详情使用错误transfer_id')
    def test_connect_transaction_007(self):
        with allure.step("测试用户的account_id"):
            account_id = 'cbb4568f-ee69-4701-83d4-a6975a852c58'
            transfer_id = "f5346953-d422-4c56-846f-779fafd1c2b2"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转详情使用错误transfer_id"):
            r = session.request('GET',
                                url='{}/api/v1/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "账户划转详情使用错误transfer_id错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_008 把数字货币从cabital转移到bybit账户')
    def test_connect_transaction_008(self):
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
                r = session.request('GET', url='{}/api/v1/config'.format(self.url), headers=connect_headers)
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
                                                url='{}/api/v1/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
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

    @allure.testcase('test_connect_transaction_009 把数字货币从cabital转移到bybit账户（小于单比最小限额）')
    def test_connect_transaction_009(self):
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
                r = session.request('GET', url='{}/api/v1/config'.format(self.url), headers=connect_headers)
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
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
                                                url='{}/api/v1/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA003', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'], r.text)
                        sleep(30)

    @allure.testcase('test_connect_transaction_010 从cabital转移到bybit账户使用错误otp')
    def test_connect_transaction_010(self):
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
            r = session.request('POST', url='{}/api/v1/accounts/{}/transfers'.format(self.url, account_id),
                                data=json.dumps(data), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == '100003', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_transaction_011 从cabital转移到bybit账户并且关联C+T交易')
    def test_connect_transaction_011(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("换汇"):
            cfx_book = get_json()['cfx_book']
            del cfx_book['1']
            del cfx_book['2']
            del cfx_book['3']
            for i in cfx_book.values():
                pair_list = i.split('-')
                cfx_dict = {'buy': pair_list[0], 'sell': pair_list[1], 'major_ccy': pair_list[0]}
                cfx_amount = ApiFunction.cfx_random_number(cfx_dict)
                data = {
                    "quote_id": cfx_amount['quote']['quote_id'],
                    "quote": cfx_amount['quote']['quote'],
                    "pair": '{}-{}'.format(cfx_amount['buy'], cfx_amount['sell']),
                    "buy_amount": str(cfx_amount['buy_amount']),
                    "sell_amount": str(cfx_amount['sell_amount']),
                    "major_ccy": cfx_amount['major_ccy']
                }
                logger.info('发送换汇data是{}'.format(data))
                with allure.step("获得换汇前buy币种balance金额"):
                    buy_amount_wallet_balance_old = ApiFunction.get_crypto_number(
                        type=cfx_amount['buy'])
                with allure.step('获得换汇前sell币种balance金额'):
                    sell_amount_wallet_balance_old = ApiFunction.get_crypto_number(
                        type=cfx_amount['sell'])
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                        url='/api/v1/accounts/{}/conversions'.format(account_id),
                                                        nonce=nonce, body=json.dumps(data))
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("账户可用余额列表"):
                    r = session.request('POST', url='{}/api/v1/accounts/{}/conversions'.format(self.url, account_id),
                                        data=json.dumps(data), headers=connect_headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['transaction_id'] is not None, "换汇错误，返回值是{}".format(r.text)
                    assert r.json()['status'] == 'Success', "换汇错误，返回值是{}".format(r.text)
                    cfx_transaction_id = r.json()['transaction_id']
                sleep(5)
                with allure.step("获得换汇后buy币种balance金额"):
                    buy_amount_wallet_balance_latest = ApiFunction.get_crypto_number(
                        type=cfx_amount['buy'])
                with allure.step("获得换汇后sell币种balance金额"):
                    sell_amount_wallet_balance_latest = ApiFunction.get_crypto_number(
                        type=cfx_amount['sell'])
                logger.info('buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(cfx_amount['buy'],
                                                                              buy_amount_wallet_balance_old,
                                                                              cfx_amount['buy_amount'],
                                                                              buy_amount_wallet_balance_latest))
                logger.info('sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(cfx_amount['sell'],
                                                                                sell_amount_wallet_balance_old,
                                                                                cfx_amount[
                                                                                    'sell_amount'],
                                                                                sell_amount_wallet_balance_latest))
                assert Decimal(buy_amount_wallet_balance_old) + Decimal(
                    cfx_amount['buy_amount']) == Decimal(
                    buy_amount_wallet_balance_latest), '换汇后金额不匹配，buy币种是{}.在换汇前钱包有{},buy金额是{},交易完成后钱包金额是{}'.format(
                    cfx_amount['buy'], buy_amount_wallet_balance_old, cfx_amount['buy_amount'],
                    buy_amount_wallet_balance_latest)
                assert Decimal(sell_amount_wallet_balance_old) - Decimal(
                    cfx_amount['sell_amount']) == Decimal(
                    sell_amount_wallet_balance_latest), '换汇后金额不匹配，sell币种是{}.在换汇前钱包有{},sell金额是{},交易完成后钱包金额是{}'.format(
                    cfx_amount['sell'], sell_amount_wallet_balance_old, cfx_amount['sell_amount'],
                    sell_amount_wallet_balance_latest)
            with allure.step("获得otp"):
                secretKey = get_json()['email']['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
            with allure.step("获得data"):
                data = {
                    'amount': str(cfx_amount['buy_amount']),
                    'symbol': pair_list[0],
                    'otp': str(mfaVerificationCode),
                    'direction': 'DEBIT',
                    'external_id': generate_string(15),
                    'conversion_id': cfx_transaction_id
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
                r = session.request('POST', url='{}/api/v1/accounts/{}/transfers'.format(self.url, account_id),
                                    data=json.dumps(data), headers=connect_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'SUCCESS', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(r.text)
                sleep(30)
