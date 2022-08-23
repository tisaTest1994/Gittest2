from Function.api_function import *
from Function.operate_sql import *


class TestTransferAbnormalApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("多语言支持"):
            headers['locale'] = 'zh-TW'
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

    @allure.title('test_transfer_001')
    @allure.description('partner发起创建direct debit交易-(校验config debit amount小于最小限额)')
    def test_transfer_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
        with allure.step("获得data"):
            external_id = generate_string(25)
        with allure.step("改symbol，模拟对应的币种limit限额"):
            symbol = 'USDT'
            debit_limit = ApiFunction.get_config_info(project='infinni games', type='debit_limit', symbol=symbol)
            logger.info('debit_limit最小限额值是：{}'.format(debit_limit[0][0]))
            debit_fee_value = ApiFunction.get_config_info(project='infinni games', type='debit_fee', symbol=symbol)
            logger.info('debit_fee_value优惠值是：{}，fee原价是：{}'.format(debit_fee_value[0][0], debit_fee_value[0][1] ))
            amount = int(debit_limit[0][0]) - int(1) - int(debit_fee_value[0][0])
            logger.info('amount传入值是：{}'.format(amount))
            if int(debit_limit[0][0]) != -1:
                data = {
                    'amount': str(amount),
                    'symbol': symbol,
                    'otp': str(mfaVerificationCode),
                    'direction': 'DEBIT',
                    'external_id': external_id
                }
            else:
                data = {
                    'amount': str(amount),
                    'symbol': symbol,
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
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA003', "划转失败，返回值是{}".format(r.text)
            with allure.step("校验transfer前后的可用balance数量"):
                assert Decimal(transfer_amount_wallet_balance_old) == Decimal(
                    transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                    transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)

    @allure.title('test_transfer_002')
    @allure.description('partner发起创建direct debit交易-(校验config debit amount大于最大限额)')
    def test_transfer_002(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
        with allure.step("获得data"):
            external_id = generate_string(25)
        with allure.step("改symbol，模拟对应的币种limit限额"):
            symbol = 'USDT'
            debit_limit = ApiFunction.get_config_info(project='infinni games', type='debit_limit', symbol=symbol)
            logger.info('debit_limit最大限额值是：{}'.format(debit_limit[0][1]))
            debit_fee_value = ApiFunction.get_config_info(project='infinni games', type='debit_fee', symbol=symbol)
            logger.info('debit_fee_value优惠值是：{}，fee原价是：{}'.format(debit_fee_value[0][0], debit_fee_value[0][1]))
            amount = int(debit_limit[0][1]) + int(1) - int(debit_fee_value[0][0])
            logger.info('amount传入的值是：{}'.format(amount))
            if int(debit_limit[0][1]) != -1:
                data = {
                    'amount': str(amount),
                    'symbol': symbol,
                    'otp': str(mfaVerificationCode),
                    'direction': 'DEBIT',
                    'external_id': external_id
                }
            else:
                data = {
                    'amount': str(amount),
                    'symbol': symbol,
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
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA003', "划转失败，返回值是{}".format(r.text)
            with allure.step("校验transfer前后的可用balance数量"):
                assert Decimal(transfer_amount_wallet_balance_old) == Decimal(
                    transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                    transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)

    @allure.title('test_transfer_003')
    @allure.description('infinni games申请发起一笔direct credit交易-(校验config credit amount小于最小限额)')
    def test_transfer_003(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
        with allure.step("获得data"):
            symbol = 'USDT'
            external_id = generate_string(25)
            credit_limit = ApiFunction.get_config_info(project='infinni games', type='credit_limit', symbol=symbol)
            logger.info('credit_limit最小限额值是：{}'.format(credit_limit[0][0]))
            amount = int(credit_limit[0][0]) - int(1)
            logger.info('amount传入的值是：{}'.format(amount))
            if int(credit_limit[0][0]) != -1:
                data = {
                    'amount': str(amount),
                    'symbol': symbol,
                    'otp': str(mfaVerificationCode),
                    'direction': 'CREDIT',
                    'external_id': external_id
                }
            else:
                data = {
                    'amount': str(amount),
                    'symbol': symbol,
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
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA003', "划转失败，返回值是{}".format(r.text)
            with allure.step("校验transfer前后的可用balance数量"):
                assert Decimal(transfer_amount_wallet_balance_old) == Decimal(
                    transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                    transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)

    @allure.title('test_transfer_004')
    @allure.description('infinni games申请发起一笔direct credit交易-(校验config credit amount大于最大限额)')
    def test_transfer_004(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
        with allure.step("获得data"):
            symbol = 'USDT'
            external_id = generate_string(25)
            credit_limit = ApiFunction.get_config_info(project='infinni games', type='credit_limit', symbol=symbol)
            logger.info('credit_limit最大限额值是：{}'.format(credit_limit[0][1]))
            amount = int(credit_limit[0][1]) + int(1)
            logger.info('amount传入的值是：{}'.format(amount))
            if int(credit_limit[0][1]) != -1:
                data = {
                    'amount': str(amount),
                    'symbol': symbol,
                    'otp': str(mfaVerificationCode),
                    'direction': 'CREDIT',
                    'external_id': external_id
                }
            else:
                data = {
                    'amount': str(amount),
                    'symbol': symbol,
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
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA004', "划转失败，返回值是{}".format(r.text)
            with allure.step("校验transfer前后的可用balance数量"):
                assert Decimal(transfer_amount_wallet_balance_old) == Decimal(
                    transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                    transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)

    @allure.title('test_transfer_005')
    @allure.description('infinni games申请direct debit，C小于最小限额也可成功')
    def test_transfer_005(self):
        with allure.step("从config获取Cfx的最小限额"):
            symbol = 'USDT'
            cfx_limit = ApiFunction.get_config_info(project='infinni games', type='cfx_limit', symbol=symbol)
            logger.info('cfx_limit最小限额值是：{}'.format(cfx_limit[0][0]))
            buy_amount = int(cfx_limit[0][0]) - int(1)
            logger.info('buy_amount值是：{}'.format(buy_amount))
        with allure.step("获取换汇币种对"):
            for i in ApiFunction.get_config_info(project='infinni games', type='pairs'):
                if i.split('-')[0] == 'USDT':
                    with allure.step('换汇'):
                        transaction = ApiFunction.cfx_random(i, i.split('-')[0], buy_amount=buy_amount)
                        logger.info('换汇后transaction的返回值是{}'.format(transaction))
                    with allure.step("校验返回值"):
                        assert int(buy_amount) < int(cfx_limit[0][0]), "换汇失败，buy_amount返回值是{},换汇最小限额值是{},".format(buy_amount, cfx_limit[0][0])
                else:
                    print(i)
    # @allure.title('test_transfer_006')
    # @allure.description('异常场景C成功T失败，infinni games发起direct debit，校验C最大限额，因C+T时C小于T失败，获取conversion_id')
    # def test_transfer_006(self):
    #     with allure.step("测试用户的account_id"):
    #         account_id = get_json()['infinni_games']['account_vid']
    #     with allure.step("从config获取Cfx的最大限额"):
    #         symbol = 'USDT'
    #         cfx_limit = ApiFunction.get_config_info(project='infinni games', type='cfx_limit', symbol=symbol)
    #         logger.info('cfx_limit最大限额值是：{}'.format(cfx_limit[0][1]))
    #         debit_limit = ApiFunction.get_config_info(project='infinni games', type='debit_limit', symbol=symbol)
    #         debit_limit_max = int(debit_limit[0][1])
    #         logger.info('config获取到最大debit限额值是：{}'.format(debit_limit_max))
    #         cfx_limit_max = int(cfx_limit[0][1])
    #         logger.info('换汇buy_amount值是：{}'.format(cfx_limit_max))
    #         buy_amount2 = cfx_limit_max + int(1)
    #         logger.info('做T时的buy_amount2值是：{}'.format(buy_amount2))
    #     with allure.step('换汇'):
    #         pair = 'USDT-EUR'
    #         transaction = ApiFunction.cfx_random(pair, pair.split('-')[0], buy_amount=cfx_limit_max)
    #         cfx_transaction_id = transaction['returnJson']['transaction']['transaction_id']
    #     with allure.step("获得data"):
    #         external_id = generate_string(25)
    #         if debit_limit_max == -1 and cfx_limit_max != -1:
    #             data = {
    #                 'amount': str(buy_amount2),
    #                 'symbol': symbol,
    #                 'otp': get_mfa_code(get_json()['email']['secretKey_richard']),
    #                 'conversion_id': cfx_transaction_id,
    #                 'direction': 'DEBIT',
    #                 'external_id': external_id
    #             }
    #             with allure.step("验签"):
    #                 unix_time = int(time.time())
    #                 nonce = generate_string(30)
    #                 sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
    #                                                     url='/api/v1/accounts/{}/transfers'.format(account_id),
    #                                                     key='infinni games', nonce=nonce, body=json.dumps(data))
    #                 headers['ACCESS-SIGN'] = sign
    #                 headers['ACCESS-TIMESTAMP'] = str(unix_time)
    #                 headers['ACCESS-NONCE'] = nonce
    #             with allure.step("transfer"):
    #                 r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
    #                                     data=json.dumps(data), headers=headers)
    #                 logger.info('r.json()的返回值是{}'.format(r.json()))
    #                 logger.info('conversion_id的值是{}'.format(data['conversion_id']))
    #             with allure.step("校验状态码"):
    #                 assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
    #             with allure.step("校验返回值"):
    #                 assert r.json()['code'] == 'PA032', "http状态码不对，目前状态码是{}".format(r.json()['code'])
    #             with allure.step("校验返回值"):
    #                 assert r.json()['message'] == 'transfer amount greater than conversion amount', '划转失败，返回值是{}'.format(r.text)

    @allure.title('test_transfer_007')
    @allure.description('异常场景C成功T失败，infinni games发起direct debit，C最小限额，因C+T时C小于T失败，获取conversion_id')
    def test_transfer_007(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
            user_ref_id ='979698088019091456'
            type = 'convert'
        with allure.step("从config获取Cfx的最小限额"):
            symbol = 'USDT'
            cfx_limit = ApiFunction.get_config_info(project='infinni games', type='cfx_limit', symbol=symbol)
            logger.info('cfx_limit最小限额值是：{}'.format(cfx_limit[0][0]))
            buy_amount = int(cfx_limit[0][0]) - int(1)
            buy_amount2 = int(cfx_limit[0][0]) + int(1)
            logger.info('buy_amount值是：{}'.format(buy_amount))
        with allure.step('换汇'):
            pair = 'USDT-EUR'
            transaction = ApiFunction.cfx_random(pair, pair.split('-')[0], buy_amount=buy_amount)
            cfx_transaction_id = transaction['returnJson']['transaction']['transaction_id']
            print(cfx_transaction_id)
        with allure.step("获得data"):
            external_id = generate_string(25)
            data = {
                'amount': str(buy_amount2),
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
            # logger.info('r.json()的返回值是{}'.format(r.json()))
            logger.info('conversion_id的值是{}'.format(data['conversion_id']))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA032', "http状态码不对，目前状态码是{}".format(r.json()['code'])
            with allure.step("校验返回值"):
                assert r.json()['message'] == 'transfer amount greater than conversion amount', '划转失败，返回值是{}'.format(r.text)
        if r.status_code == 400:
            with allure.step("查询transfer"):
                r = session.request('Get', url='{}/accounts/{}/transaction/{}/{}'.format(self.url, user_ref_id, type, symbol),
                                     headers=headers)
                logger.info('r.json()的返回值是{}'.format(r.json()))
    @allure.title('test_transfer_008')
    @allure.description('infinni games申请，先做C+T，单做一笔交易C成功T因2FA失败，获取conversion_id')
    def test_transfer_008(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['infinni_games']['account_vid']
            with allure.step('换汇'):
                pair = 'USDT-EUR'
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

    @allure.title('test_transfer_009')
    @allure.description('对账异常场景 - 划转交易详情使用无效external_id')
    def test_transfer_009(self):
        external_id = generate_string(25)
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
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'PA030', "对账 - 划转交易详情使用external_id错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_010')
    @allure.description('基于账户获取划转列表（传入错误的account_id/account_vid,返回403）')
    def test_transfer_010(self):
        with allure.step("测试用户的account_id"):
            account_id = '9777dcc37-fb9f-40fc-af2833a362222312'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/transfers'.format(account_id), key='infinni games', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("把数字货币从cabital转移到bybit账户"):
            r = session.request('GET', url='{}/accounts/{}/transfers'.format(self.url, account_id), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_transfer_011')
    @allure.description('交易列表查询（不传默认参数）-INITIALIZED 权限校验')
    def test_transfer_011(self):
        with allure.step("partner用户的user_ext_ref"):
            user_ext_ref = '992030823286849536'
            tx_type_list = ['buy', 'convert', 'transfer']
            for tx_type in tx_type_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/transactions/{}'.format(user_ext_ref,
                                                                                                         tx_type),
                                                        key='infinni games', nonce=nonce)
                    headers['ACCESS-SIGN'] = sign
                    headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    headers['ACCESS-NONCE'] = nonce
                with allure.step("账户划转列表"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/transactions/{}'.format(self.url, user_ext_ref, tx_type),
                                        headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 403, "http状态码不对，目前状态码是{}".format(r.status_code)