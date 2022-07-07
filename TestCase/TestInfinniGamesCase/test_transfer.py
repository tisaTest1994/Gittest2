from Function.api_function import *
from Function.operate_sql import *


# Transfer相关cases
class TestTransferApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

    @allure.title('test_transfer_001')
    @allure.description('基于账户获取划转列表（不传入任何参数，使用默认参数）')
    def test_transfer_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/transfers'.format(account_id), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('GET', url='{}/accounts/{}/transfers'.format(self.url, account_id), headers=headers)
            logger.info('r.json返回值是{}'.format(r.json()))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfers'] is not None, "基于账户获取划转列表（传入部分参数）错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_002')
    @allure.description('基于账户获取划转列表（传入部分参数）')
    def test_transfer_002(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/transfers?page_size=30&has_conversion=false&symbol=USDT&direction=DEBIT'.format(account_id), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('GET', url='{}/accounts/{}/transfers?page_size=30&has_conversion=false&symbol=USDT&direction=DEBIT'.format(self.url, account_id), headers=headers)
            logger.info('r.json返回值是{}'.format(r.json()))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfers'] is not None, "基于账户获取划转列表（传入部分参数）错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_003')
    @allure.description('基于外部账户获取划转列表（不传入任何参数，使用默认参数）')
    def test_transfer_003(self):
        with allure.step("测试用户的外部账户id"):
            user_ext_ref = get_json()['infinni_games']['uid_A']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/userextref/{}/transfers'.format(user_ext_ref), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('GET', url='{}/userextref/{}/transfers'.format(self.url, user_ext_ref), headers=headers)
            logger.info('r.json()返回值是{}'.format(r.json()))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfers'] is not None, "基于账户获取划转列表（传入部分参数）错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_004')
    @allure.description('基于外部账户获取划转列表（传入部分参数）')
    def test_transfer_004(self):
        with allure.step("测试用户的account_id"):
            user_ext_ref = get_json()['infinni_games']['uid_A']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/userextref/{}/transfers?page_size=30&has_conversion=false&symbol=USDT&direction=DEBIT'.format(user_ext_ref), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('GET', url='{}/userextref/{}/transfers?page_size=30&has_conversion=false&symbol=USDT&direction=DEBIT'.format(self.url, user_ext_ref), headers=headers)
            logger.info('r.json()返回值是{}'.format(r.json()))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfers'] is not None, "基于账户获取划转列表（传入部分参数）错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_005')
    @allure.description('基于账户获取划转详情')
    def test_transfer_005(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
            transfer_id = '4b960cc1-ebf8-4bbc-a8fb-f8549e2d60d8'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('GET', url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id), headers=headers)
            logger.info('r.json()返回值是{}'.format(r.json()))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['user_ext_ref'] == 'weqw@163.com', '基于账户获取划转详情错误，返回值是{}'.format(r.text)

    @allure.title('test_transfer_006')
    @allure.description('基于划转ID获取划转详情')
    def test_transfer_006(self):
        transfer_id = "4b960cc1-ebf8-4bbc-a8fb-f8549e2d60d8"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/transfers/{}'.format(transfer_id), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('GET', url='{}/transfers/{}'.format(self.url, transfer_id), headers=headers)
            logger.info('r.json()返回值是{}'.format(r.json()))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['user_ext_ref'] == 'weqw@163.com', '基于划转ID获取划转详情错误，返回值是{}'.format(r.text)

    @allure.title('test_transfer_007')
    @allure.description('infinni games申请，把资金从cabital划转到infinni games')
    def test_transfer_007(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
        with allure.step("获得data"):
            external_id = generate_string(25)
            data = {
                'amount': '120',
                'symbol': 'USDT',
                'otp': str(mfaVerificationCode),
                'direction': 'DEBIT',
                'external_id': external_id
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id),
                                                key='infinni games', nonce=nonce, body=json.dumps(data))
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step('获得transfer前币种可用balance数量'):
            transfer_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=data['symbol'])
        with allure.step("transfer"):
            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                data=json.dumps(data), headers=headers)
            logger.info('r.json返回值是{}'.format(r.json()))
        with allure.step('获得transfer后币种balance数量'):
            transfer_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=data['symbol'])
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfer_id'] is not None, '划转失败，返回值是{}'.format(r.text)
        with allure.step("校验transfer前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_old) - Decimal(data['amount']) == Decimal(
                transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)

    @allure.title('test_transfer_008')
    @allure.description('infinni games申请，把资金从infinni games划转到cabital')
    def test_transfer_008(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
        with allure.step("获得data"):
            external_id = generate_string(25)
            data = {
                'amount': '100',
                'symbol': 'USDT',
                'otp': str(mfaVerificationCode),
                'direction': 'CREDIT',
                'external_id': external_id
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id),
                                                key='infinni games', nonce=nonce, body=json.dumps(data))
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step('获得transfer前币种可用balance数量'):
            transfer_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=data['symbol'])
        with allure.step("transfer"):
            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                data=json.dumps(data), headers=headers)
            logger.info('r.json返回值是{}'.format(r.json()))
        with allure.step('获得transfer后币种balance数量'):
            transfer_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=data['symbol'])
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfer_id'] is not None, '划转失败，返回值是{}'.format(r.text)
        with allure.step("校验transfer前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_old) + Decimal(data['amount']) == Decimal(
                transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)

    @allure.title('test_transfer_009')
    @allure.description('infinni games申请，先做C+T，把资金从cabital划转到infinni games')
    def test_transfer_009(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        for i in ApiFunction.get_connect_cfx_list(self.url, headers, key='infinni games'):
            with allure.step('换汇'):
                transaction = ApiFunction.cfx_random(i, i.split('-')[0])
                cfx_transaction_id = transaction['returnJson']['transaction']['transaction_id']
                with allure.step("获得data"):
                    external_id = generate_string(25)
                    if i.split('-')[0] in get_json()['crypto_list']:
                        symbol = i.split('-')[0]
                    else:
                        symbol = i.split('-')[1]
                    data = {
                        'amount': transaction['data']['buy_amount'],
                        'symbol': symbol,
                        'otp': get_mfa_code(get_json()['email']['secretKey_richard']),
                        'conversion_id': cfx_transaction_id,
                        'direction': 'DEBIT',
                        'external_id': external_id
                    }
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                        url='/api/v1/accounts/{}/transfers'.format(account_id),
                                                        key='infinni games', nonce=nonce, body=json.dumps(data))
                    headers['ACCESS-SIGN'] = sign
                    headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    headers['ACCESS-NONCE'] = nonce
                with allure.step("transfer"):
                    r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                        data=json.dumps(data), headers=headers)
                    logger.info('r.json返回值是{}'.format(r.json()))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['transfer_id'] is not None, '划转失败，返回值是{}'.format(r.text)

    @allure.title('test_transfer_010')
    @allure.description('二笔transfer后balance检查')
    def test_transfer_010(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("获得data"):
            external_id = generate_string(25)
            amount = '120'
            data = {
                'amount': amount,
                'symbol': 'USDT',
                'otp': get_mfa_code(get_json()['email']['secretKey_richard']),
                'direction': 'DEBIT',
                'external_id': external_id
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/accounts/{}/transfers'.format(account_id), key='infinni games', nonce=nonce, body=json.dumps(data))
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step('获得transfer前币种可用balance数量'):
            transfer_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=data['symbol'])
            logger.info('transfer_amount_wallet_balance_old的值是{}'.format(transfer_amount_wallet_balance_old))
        with allure.step("transfer"):
            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                data=json.dumps(data), headers=headers)
        with allure.step('获得transfer后币种balance数量'):
            transfer_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=data['symbol'])
            logger.info('transfer_amount_wallet_balance_latest的值是{}'.format(transfer_amount_wallet_balance_latest))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验transfer前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_old) - Decimal(data['amount']) == Decimal(transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)
            sleep(30)
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
        with allure.step("获得data"):
            external_id = generate_string(25)
            amount1 = '100'
            data = {
                'amount': amount1,
                'symbol': 'USDT',
                'otp': mfaVerificationCode,
                'direction': 'CREDIT',
                'external_id': external_id
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/accounts/{}/transfers'.format(account_id), key='infinni games', nonce=nonce, body=json.dumps(data))
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step('获得transfer前币种可用balance数量'):
            transfer_amount_wallet_balance_old2 = ApiFunction.get_crypto_number(type=data['symbol'])
            logger.info('transfer_amount_wallet_balance_old2的值是{}'.format(transfer_amount_wallet_balance_old2))
        with allure.step("校验第2笔transfer前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_latest) == Decimal(transfer_amount_wallet_balance_old2), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(transfer_amount_wallet_balance_latest, transfer_amount_wallet_balance_old2)
        with allure.step("transfer"):
            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                data=json.dumps(data), headers=headers)
        with allure.step('获得transfer后币种balance数量'):
            transfer_amount_wallet_balance_latest2 = ApiFunction.get_crypto_number(type=data['symbol'])
            logger.info('transfer_amount_wallet_balance_latest2的值是{}'.format(transfer_amount_wallet_balance_latest2))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验第2笔transfer前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_latest2) == Decimal(
                transfer_amount_wallet_balance_old2) + Decimal(amount1), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                transfer_amount_wallet_balance_old2, transfer_amount_wallet_balance_latest2)
        with allure.step("校验2笔transfer前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_old) - Decimal(amount) == Decimal(
                transfer_amount_wallet_balance_latest2) - Decimal(amount1), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest2)

    @allure.title('test_transfer_011')
    @allure.description('对账 - 划转交易详情使用external_id')
    def test_transfer_011(self):
        external_id = 'fVug0yqnyCJcPRbpgYnilfUPF'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/recon/transfers/{}'.format(external_id), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("划转交易详情使用无效external_id"):
            r = session.request('GET', url='{}recon/transfers/{}'.format(self.url, external_id),headers=headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['external_id'] == external_id, "对账 - 划转交易详情使用external_id错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_012')
    @allure.description('infinni games申请，先做C+T，单做一笔交易C成功T失败')
    def test_transfer_012(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
            with allure.step('换汇'):
                pair ='USDT-EUR'
                transaction = ApiFunction.cfx_random(pair, pair.split('-')[0])
                cfx_transaction_id = transaction['returnJson']['transaction']['transaction_id']
                with allure.step("获得data"):
                    external_id = generate_string(25)
                    data = {
                        'amount': '10',
                        'symbol': 'USDT',
                        'otp': '123456',
                        'conversion_id': cfx_transaction_id,
                        'direction': 'DEBIT',
                        'external_id': external_id
                    }
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                        url='/api/v1/accounts/{}/transfers'.format(account_id),
                                                        key='infinni games', nonce=nonce, body=json.dumps(data))
                    headers['ACCESS-SIGN'] = sign
                    headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    headers['ACCESS-NONCE'] = nonce
                with allure.step("transfer"):
                    r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                        data=json.dumps(data), headers=headers)
                    logger.info('r.json()的返回值是{}'.format(r.json()))
                    logger.info('conversion_id的值是{}'.format(data['conversion_id']))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['message'] == 'mfa failed', '划转失败，返回值是{}'.format(r.text)
                with allure.step("等待30秒"):
                    sleep(30)