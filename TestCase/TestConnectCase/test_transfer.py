import allure

from Function.api_function import *
from Function.operate_sql import *


# Connect相关cases
class TestConnectTransactionApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.description('账户操作相关')
    @allure.title('test_connect_config 获取合作方的配置')
    def test_connect_config(self):
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
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('connect_config接口返回值是{}'.format(str(r.text)))
            logger.info("获取合作方的配置结果检查 ==>> 期望结果:currencies is not None,实际结果:【{}】".format(r.json()['currencies']))
            if r.json()['currencies'] is not None:
                assert r.json()['currencies'] is not None
            else:
                raise Exception("currencies is None")

    @allure.description('账户操作相关--获取报价')
    @allure.title('test_currency_quotes_001 获取报价--正向币种对报价')
    def test_currency_quotes_001(self):
        with allure.step("获取报价"):
            for i in get_json()['cfx_book'].values():
                with allure.step("获取正向报价"):
                    r = session.request('GET', url='{}/quotes/{}'.format(self.url, i), headers=connect_headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    logger.info('quotes接口返回值是{}'.format(str(r.text)))
                    logger.info(
                        "获取正向币种报价结果检查==>> 期望结果:quote is not None,实际结果:正向币种对报价是【{}{}】".format(r.json()['quote_id'],
                                                                                             r.json()['quote']))
                    assert r.json()['quote'] is not None
                    assert r.json()['quote_id'] is not None

    @allure.description('账户操作相关--获取报价')
    @allure.title('test_currency_quotes_002 获取报价--反向报价')
    def test_currency_quotes_002(self):
        with allure.step("获取报价"):
            for i in get_json()['cfx_book'].values():
                with allure.step("获取反向报价"):
                    new_pair = '{}{}{}'.format(i.split('-')[1], '-', i.split('-')[0])
                    r = session.request('GET', url='{}/quotes/{}'.format(self.url, new_pair),
                                        headers=connect_headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    logger.info('quotes接口返回值是{}'.format(str(r.text)))
                    logger.info(
                        "获取反向币种报价结果检查==>> 期望结果:quote is not None,实际结果:反向币种对报价是【{}{}】".format(r.json()['quote_id'],
                                                                                             r.json()['quote']))
                    assert r.json()['quote'] is not None
                    assert r.json()['quote_id'] is not None

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_001 获取账户可用余额列表--有资金）')
    def test_wallet_balances_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:balances is not None,实际结果:【{}】".format(r.json()['balances']))
            assert r.json()['balances'] is not None

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_002 获取账户可用余额列表--金额为0检查）')
    def test_wallet_balances_002(self):
        with allure.step("测试用户的account_id"):
            account_id = 'd0f4335e-cf80-44f1-b79c-cca2cab95cac'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:可用余额为0检查,实际结果:【可用余额是{}】".format(r.json()['balances'][0]['balances']))
            assert r.json()['balances'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_003 未在Cabital提交KYC账户--查询可用余额列表）')
    def test_wallet_balances_003(self):
        with allure.step("测试用户的account_id"):
            account_id = 'eb9659ea-0d95-4f0f-83a3-1152c5a90ee9'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:kyc未通过，无法查询余额,实际结果:【错误码是{} 报错信息{}】".format(r.json()['code'],
                                                                                           format(r.json()['message'])))
            assert r.json()['code'] == 'PA012'
            assert r.json()['message'] == 'this account kyc is not passed'

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_004 kyc状态PENDING--查询可用余额列表）')
    def test_wallet_balances_004(self):
        with allure.step("测试用户的account_id"):
            account_id = '358ff717-ea3c-40d4-86da-d73b4a2dce37'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:kyc未通过，,实际结果:【错误码是{} 报错信息{}】".format(r.json()['code'],
                                                                                     format(r.json()['message'])))
            assert r.json()['code'] == 'PA012'
            assert r.json()['message'] == 'this account kyc is not passed'

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_005 kyc状态temporary_rejected--查询可用余额列表）')
    def test_wallet_balances_005(self):
        with allure.step("测试用户的account_id"):
            account_id = '146aa112-2fd7-4cb5-a8ff-bb2fc45f55ed'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:kyc未通过，,实际结果:【错误码是{} 报错信息{}】".format(r.json()['code'],
                                                                                     format(r.json()['message'])))
            assert r.json()['code'] == 'PA012'
            assert r.json()['message'] == 'this account kyc is not passed'

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_006 kyc状态FINAL_REJECTED-查询可用余额列表）')
    def test_wallet_balances_006(self):
        with allure.step("测试用户的account_id"):
            account_id = '1799875b-5749-4056-9cc9-6fba16f0f1e0'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:kyc未通过，,实际结果:【错误码是{} 报错信息{}】".format(r.json()['code'],
                                                                                     format(r.json()['message'])))
            assert r.json()['code'] == 'PA012'
            assert r.json()['message'] == 'this account kyc is not passed'

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_006 kyc状态CREATED-查询可用余额列表）')  # kyc状态CREATED-查询可用余额列表
    def test_wallet_balances_007(self):
        with allure.step("测试用户的account_id"):
            account_id = 'ffa1b49e-46f6-47b3-8ea6-2c41bac6b6ed'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:kyc未通过，,实际结果:【{}】".format(r.json()))
            assert r.json()['balances'] is not None

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_007 kyc状态MATCHING-查询可用余额列表）')  # kyc状态MATCHING-查询可用余额列表
    def test_wallet_balances_008(self):
        with allure.step("测试用户的account_id"):
            account_id = 'bacf2b3e-6599-44f4-adf6-c4c13ff40946'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:kyc未通过，,实际结果:【{}】".format(r.json()))
            assert r.json()['balances'] is not None

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_008 kyc状态MISMATCHED-查询可用余额列表）')  # kyc状态CREATED-查询可用余额列表
    def test_wallet_balances_009(self):
        with allure.step("测试用户的account_id"):
            account_id = 'b7ff2c76-5dae-4ea3-bb42-4b355357072a'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:查询余额,实际结果:【{}】".format(r.json()))
            assert r.json()['balances'] is not None

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_009 kyc状态UNLINKED-查询可用余额列表）')  # kyc状态CREATED-查询可用余额列表
    def test_wallet_balances_010(self):
        with allure.step("测试用户的account_id"):
            account_id = '3fde7f5f-f7a7-4230-8963-89c2303039e0'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            logger.info("获取账户可用余额列表金额检查=>> 期望结果:kyc未通过,实际结果:【{}】".format(r.json()['code'], r.json()['message']))
            assert r.json()['code'] == 'PA012'
            assert r.json()['message'] == 'this account kyc is not passed'

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_010 检查cabital账户可用余额列表与bybit账户可用余额验证一致）')
    def test_wallet_balances_011(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/balances'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("检查cabital账户可用余额列表与bybit账户可用余额验证一致"):
            logger.info('balance接口返回值是{}'.format(str(r.text)))
            balance_list = ApiFunction.balance_list()
            for i in balance_list:
                mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE',
                                                               wallet_type='BALANCE')
                for y in r.json()['balances']:
                    if y['code'] == i:
                        bybit_balance = y['balances']
                        with allure.step("检查cabital账户可用余额列表与bybit账户可用余额验证一致"):
                            logger.info(
                                "cabital与bybit金额一致性校验检查=>> 期望结果:cabital账号是{}{},"
                                "实际结果:【bybit是{}{}】".format(i, mobile_balance, i, bybit_balance))
                        assert float(mobile_balance) == float(bybit_balance)

    @allure.description('账户操作相关--获取账户可用余额列表')
    @allure.title('test_wallet_balances_012 获取账户可用余额单币(有资金）')
    def test_wallet_balances_011(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得balance list"):
            balance_list = ApiFunction.balance_list()
        with allure.step("循环获取单币种"):
            for i in balance_list:
                print(i)
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
                    r = session.request('GET', url='{}/accounts/{}/balances/{}'.format(self.url, account_id, i),
                                        headers=connect_headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['balance'] is not None, "账户可用余额列表错误，返回值是{}".format(r.text)
                with allure.step("通过mobile接口获取金额"):
                    mobile_balance = ApiFunction.get_crypto_number(type=i, balance_type='BALANCE_TYPE_AVAILABLE',
                                                                   wallet_type='BALANCE')
                with allure.step("获取的金额和通过mobile接口获取的金额对比"):
                    logger.info('balance接口返回值是{}'.format(str(r.text)))
                    logger.info("balances=>> 期望结果:{}{},"
                                "实际结果:【币种{} 可用余额：{}】".format(i, mobile_balance, i, r.json()['balance']['balances']))
                assert float(mobile_balance) == float(r.json()['balance'][
                                                          'balances'])

    @allure.description('账户操作相关--获取账户单币入账信息')
    @allure.title('test_deposit_method_001 获取账户单币入账信息, 入币方式缺失，使用默认')
    def test_deposit_method_null(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获取账户单币入账信息"):
            cash_list = get_json()['cash_list']
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                            account_id, i, ''), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("入币方式为空，使用默认"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i, ''),
                                        headers=connect_headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    logger.info('接口返回值是{}'.format(str(r.text)))
                    if i == 'GBP':
                        logger.info(" 期望结果:GBP Faster Payments，实际结果:默认【{} {}】".format(i, r.json()['method']))
                        assert r.json()['method'] == 'Faster Payments'
                    elif i == 'EUR':
                        logger.info("期望结果:EUR SEPA ，实际结果:默认【{} {}】".format(i, r.json()['method']))
                        assert r.json()['method'] == 'SEPA'
                    elif i == 'CHF':
                        logger.info("期望结果:CHF SIC，实际结果:默认【{} {}】".format(i, r.json()['method']))
                        assert r.json()['method'] == 'SIC'

    @allure.description('账户操作相关--获取账户单币入账信息')
    @allure.title('test_deposit_method_002 获取账户单币入账信息, 入币方式SEPA')
    def test_deposit_method_SEPA(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息"):
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                            account_id, i, 'SEPA'), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式SEPA"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id,
                                                                                           i, 'SEPA'),
                                        headers=connect_headers)
                with allure.step('校验返回值'):
                    logger.info('接口返回值是{}'.format(str(r.text)))
                    if i == 'GBP':
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            logger.info(" 期望结果: GBP入币方式SEPA错误,错误码PA033，实际结果:【{} {} {}】".format(i, r.json()['code'],
                                                                                               r.json()['message']))
                            assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式SEPA错误，返回值是{}".format(r.text)
                    elif i == 'EUR':
                        with allure.step("校验状态码"):
                            logger.info(" 期望结果: EUR SEPA，实际结果:【{}】".format(r.json()))
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                            assert r.json()['meta'] is not None

    @allure.description('账户操作相关--获取账户单币入账信息')
    @allure.title('test_deposit_method_003 获取账户单币入账信息, 入币方式Faster Payments')
    def test_deposit_method_FPS(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息, 入币方式Faster Payments"):
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                            account_id, i, 'FPS'), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式Faster Payments"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i,
                                                                                           'FPS'),
                                        headers=connect_headers)
                with allure.step("状态码和返回值"):
                    logger.info('返回值是{}'.format(str(r.text)))
                    if i == 'EUR':
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            logger.info(
                                " 期望结果: EUR入币方式Faster Payments错误,错误码PA033，实际结果:【{} {} {}】".format(i, r.json()['code'],
                                                                                                  r.json()['message']))
                            assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式Faster Payments错误，返回值是{}".format(
                                r.text)
                    elif i == 'GBP':
                        with allure.step("校验状态码"):
                            logger.info(" 期望结果: GBP Faster Payments，实际结果:【{}】".format(r.json()))
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.description('账户操作相关--获取账户单币入账信息')
    @allure.title('test_deposit_method_004 获取账户单币入账信息, 入币方式SIC')
    def test_deposit_method_SIC(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息"):
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                            account_id, i, 'SIC'), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式SIC"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i,
                                                                                           'SIC'),
                                        headers=connect_headers)
                if i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值GBP"):
                        logger.info(" 期望结果: GBP入币方式SIC错误,错误码PA033，"
                                    "实际结果:【{} {} {}】".format(i, r.json()['code'], r.json()['message']))
                        assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                elif i == 'EUR':
                    with allure.step("校验返回值EUR"):
                        logger.info(" 期望结果: EUR入币方式SIC错误,错误码PA033，"
                                    "实际结果:【{} {} {}】".format(i, r.json()['code'], r.json()['message']))
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                elif i == 'CHF':
                    with allure.step("校验状态码"):
                        logger.info(" 期望结果: CHF SIC，实际结果:【{}】".format(r.json()))
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.description('账户操作相关--获取账户单币入账信息')
    @allure.title('test_deposit_method_005 获取账户单币入账信息入币方式与mobile接口返回一致')
    def test_deposit_method_compare(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得法币list"):
            cash_list = get_json()['cash_list']
        with allure.step("获取账户单币入账信息"):
            for i in cash_list:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                        url='/api/v1/accounts/{}/balances/{}/deposit/{}'.format(
                                                            account_id, i, 'SIC'), nonce=nonce)
                    connect_headers['ACCESS-SIGN'] = sign
                    connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    connect_headers['ACCESS-NONCE'] = nonce
                with allure.step("获取账户单币入账信息, 入币方式SIC"):
                    r = session.request('GET',
                                        url='{}/accounts/{}/balances/{}/deposit/{}'.format(self.url, account_id, i,
                                                                                           'SIC'),
                                        headers=connect_headers)
                if i == 'GBP':
                    with allure.step("校验状态码"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值GBP"):
                        assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                elif i == 'EUR':
                    with allure.step("校验返回值EUR"):
                        assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        assert r.json()['code'] == 'PA033', "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                elif i == 'CHF':
                    logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['meta'] is not None, "获取账户单币入账信息, 入币方式SIC错误，返回值是{}".format(r.text)
                        bank_accounts = r.json()['meta']
                    with allure.step("mobile接口一致性查询"):
                        with allure.step("CHF法币充值账户"):
                            r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'CHF', 'SIC'),
                                                headers=headers)
                            with allure.step("校验状态码"):
                                logger.info('返回值是{}'.format(str(r.text)))
                                logger.info(" 期望结果: {}"
                                            "实际结果:【{}】".format(bank_accounts, r.json()['bank_accounts'][0]))
                                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                                assert r.json()['bank_accounts'] is not None, "EUR法币充值账户错误，返回值是{}".format(r.text)
                                with allure.step("校验返回值"):
                                    bank_accounts_mobile = r.json()['bank_accounts'][0]
                                # assert bank_accounts_mobile==bank_accounts
                                assert bank_accounts_mobile.items() & bank_accounts.items()

    @allure.description('账户操作相关--查询划转历史记录')
    @allure.title('test_transaction_list_001 已kyc账户查询划转历史记录(为空检查)')
    def test_transaction_list_001(self):
        with allure.step("测试用户的account_id"):
            account_id = 'd0f4335e-cf80-44f1-b79c-cca2cab95cac'
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
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('返回值是{}'.format(str(r.text)))
            logger.info(" 期望结果: 账户划转列表为空,实际结果:【{}】".format(r.json()['transfers']))
            assert r.json()['transfers'] is None

    @allure.description('账户操作相关--查询划转历史记录')
    @allure.title('test_transaction_list_002 已kyc账户查询划转历史记录(多数据检查)')
    def test_transaction_list_002(self):
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
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('返回值是{}'.format(str(r.text)))
            logger.info(" 期望结果: 账户划转列表多数据检查,实际结果:【{}】".format(r.json()['transfers']))
            assert r.json()['transfers'] is not None

    @allure.description('账户操作相关--查询划转历史记录')
    @allure.title('test_transaction_list_003 未kyc账户查询划转历史记录')
    def test_transaction_list_003(self):
        with allure.step("测试用户的account_id"):
            account_id = 'ffa1b49e-46f6-47b3-8ea6-2c41bac6b6ed'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("未kyc账户查询划转历史记录"):
            r = session.request('GET', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('返回值是{}'.format(str(r.text)))
            logger.info(
                " 期望结果: 未kyc账户查询划转历史记录错误码PA009 ,实际结果:【{} message：{}】".format(r.json()['code'], r.json()['message']))
            assert r.json()['code'] == 'PA009'
            assert r.json()['message'] == 'this account kyc is not matched'

    @allure.description('账户操作相关--查询划转详情')
    @allure.title('test_transaction_detail_001 查询划转详情成功')
    def test_transaction_detail_001(self):
        with allure.step("测试用户的account_id"):
            account_id = '96f29441-feb4-495a-a531-96c833e8261a'
            transfer_id = "0c90d0d3-1195-4ceb-9114-e947e167b479"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id,
                                                                                              transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("正确的transfer_id"):
            r = session.request('GET',
                                url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('返回值是{}'.format(str(r.text)))
            logger.info(" 期望结果: 查询划转详情transfer_id=0c90d0d3-1195-4ceb-9114-e947e167b479 ,实际结果:【{}】".format(
                r.json()['transfer_id']))
            assert r.json()['transfer_id'] is not None

    @allure.description('账户操作相关--查询划转详情')
    @allure.title('test_transaction_detail_002 划转详情transfer_id为空查询')
    def test_transaction_detail_002(self):
        with allure.step("测试用户的account_id"):
            account_id = 'd0f4335e-cf80-44f1-b79c-cca2cab95cac'
            transfer_id = ""
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("划转详情查询"):
            r = session.request('GET',
                                url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('返回值是{}'.format(str(r.text)))
            logger.info(" 期望结果: transfer_id is null,实际结果:【{}】".format(r.json()['transfers']))
            assert r.json()['transfers'] is None

    @allure.description('账户操作相关--查询划转详情')
    @allure.title('test_transaction_detail_003 划转详情使用错误transfer_id查询')
    def test_transaction_detail_003(self):
        with allure.step("测试用户的account_id"):
            account_id = 'd0f4335e-cf80-44f1-b79c-cca2cab95cac'  # account_id与transfer_id
            transfer_id = "09uhhhgf778"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("划转详情查询"):
            r = session.request('GET', url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            logger.info('返回值是{}'.format(r.text))
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json() == {}

    @allure.description('账户操作相关--查询划转详情')
    @allure.title('test_transaction_detail_004 划转详情transfer_id不属于account_id数据匹配查询')
    def test_transaction_detail_004(self):
        with allure.step("测试用户的account_id"):
            account_id = 'd0f4335e-cf80-44f1-b79c-cca2cab95cac'  # account_id与transfer_id
            transfer_id = "0c90d0d3-1195-4ceb-9114-e947e167b479"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id, transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("划转详情查询"):
            r = session.request('GET', url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            logger.info('返回值是{}'.format(r.text))
            logger.info(" 期望结果: transfer_id不存在,实际结果:【{}】".format(r.json()))
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json() == {}

    @allure.description('账户操作相关--查询划转详情')
    @pytest.mark.skip('需划转接口传数据')
    @allure.title('test_transaction_detail_005 查询划转详情字段检查')
    def test_transaction_detail_005(self):
        with allure.step("测试用户的account_id"):
            account_id = '96f29441-feb4-495a-a531-96c833e8261a'
            transfer_id = "0c90d0d3-1195-4ceb-9114-e947e167b479"
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(account_id,
                                                                                              transfer_id),
                                                nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("划转详情查询"):
            r = session.request('GET',
                                url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('返回值是{}'.format(str(r.text)))
            logger.info(" 期望结果: ,实际结果:【{}】".format(r.json()['transfer_id']))
            assert r.json()['transfer_id'] is not None

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_001 划转金额amount字段检查（小于单笔最小限额）')
    def test_connect_transaction_001(self):
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
                logger.info('返回值是{}'.format(str(r.json())))
                print('这是r的数据', r.json())
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r1 = session.request('POST',
                                                 url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                 data=json.dumps(data), headers=connect_headers)
                            print('这是r1的数据', r1.json())
                        with allure.step("校验状态码"):
                            assert r1.status_code == 400, "http状态码不对，目前状态码是{}".format(r1.status_code)
                        with allure.step("校验返回值"):
                            print('这是r1的数据', r1.json())
                            logger.info('返回值是{}'.format(str(r1.text)))
                            print('这是r1的数据', r1.json())
                            logger.info(
                                " 期望结果: config接口返回配置信息, 实际结果:【单笔最小限额{}code{}message{}】".format(i, r1.json()['code'],
                                                                                               r1.json()['message']))
                            assert r1.json()['code'] == 'PA003'
                        sleep(30)
    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_002 划转金额amount字段检查（金额错误）')
    def test_connect_transaction_002(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': 'sasa',
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            # logging.info('期望j金额不合法'.format(i['symbol'])
                            assert r.json()['code'] == 'PA028', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                        r.text)
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_003 划转金额amount字段检查（金额为0）')
    def test_connect_transaction_003(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': 0,
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA999', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                        r.text)
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_004 划转金额amount字段检查（金额为空）')
    def test_connect_transaction_004(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': '',
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA028', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                        r.text)
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_005 划转金额amount字段检查（金额超限）')
    def test_connect_transaction_005(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': 99,
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA999', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                      r.text)
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_006 symbol字段检查（为空）')
    def test_connect_transaction_006(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': '',
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA019', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                        r.text)
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_007 symbol字段检查（不支持的symbol）')
    def test_connect_transaction_007(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': 'ape',
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA019', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                        r.text)
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_008 从cabital转移到bybit账户使用错误otp')
    def test_connect_transaction_008(self):
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
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'PA008', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(r.text)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_009 从cabital转移到bybit账户otp字段为空')
    def test_connect_transaction_009(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("获得data"):
            data = {
                'amount': '0.012',
                'symbol': 'BTC',
                'otp': '',
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
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'PA008', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(r.text)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_010 direction为空检查')
    def test_connect_transaction_010(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': '',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA999', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                        r.text)
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_011 direction为错误类型检查')
    def test_connect_transaction_011(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'withdraw',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA999', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                        r.text)
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_012 direction为CREDIT类型检查')
    def test_connect_transaction_012(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'CREDIT',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

                        with allure.step("校验返回值"):
                            logger.info(" 期望结果: direction为CREDIT类型返回成功 实际结果:【status{}】".format(r.json()['status']))
                            assert r.json()['status'] == 'SUCCESS'
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_013 direction为DEBIT类型检查')
    def test_connect_transaction_013(self):
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
                print(r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r = session.request('POST',
                                                url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

                        with allure.step("校验返回值"):
                            logger.info(" 期望结果: direction为CREDIT类型返回成功 实际结果:【status {}】".format(r.json()['status']))
                            assert r.json()['status'] == 'SUCCESS'
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_014 conversion_id字段为空检查，非必填字段')
    def test_connect_transaction_014(self):
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
                logger.info('返回值是{}'.format(str(r.json())))
                print('这是r的数据', r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'conversion_id': '',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r1 = session.request('POST',
                                                 url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                 data=json.dumps(data), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r1.status_code == 200, "http状态码不对，目前状态码是{}".format(r1.status_code)
                        with allure.step("校验返回值"):
                            logger.info('返回值是{}'.format(str(r1.text)))
                            assert r1.json()['status'] == 'SUCCESS'
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_015 conversion_id字段不存在，报错PA031')
    def test_connect_transaction_015(self):
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
                logger.info('返回值是{}'.format(str(r.json())))
                print('这是r的数据', r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'conversion_id': '—tt@@2121',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r1 = session.request('POST',
                                                 url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                 data=json.dumps(data), headers=connect_headers)
                            print('这是r1的数据', r1.json())
                        with allure.step("校验状态码"):
                            assert r1.status_code == 400, "http状态码不对，目前状态码是{}".format(r1.status_code)
                        with allure.step("校验返回值"):
                            print('这是r1的数据', r1.json())
                            logger.info('返回值是{}'.format(str(r1.text)))
                            print('这是r1的数据', r1.json())
                            logger.info(
                                " 期望结果: , 实际结果:【message{}】".format(i, r1.json()))
                            assert r1.json()['code'] == 'PA031'
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_016  错误的conversion_id ')
    def test_connect_transaction_016(self):
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
                logger.info('返回值是{}'.format(str(r.json())))
                print('这是r的数据', r.json())
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
                                'conversion_id': 'd81adf6d-0322-41d7-8c32-669203e35f11',
                                'external_id': generate_string(15)
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r1 = session.request('POST',
                                                 url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                 data=json.dumps(data), headers=connect_headers)
                        with allure.step("校验状态码"):
                            assert r1.status_code == 400, "http状态码不对，目前状态码是{}".format(r1.status_code)
                        with allure.step("校验返回值"):
                            logger.info(
                                " 期望结果: conversion_id错误检查返回PA031错误, 实际结果:【返回值{}】".format(str(r1.text)))
                            assert r1.json()['code'] == 'PA031'
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_017  external_id错误 ')
    def test_connect_transaction_017(self):
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
                logger.info('返回值是{}'.format(str(r.json())))
                print('这是r的数据', r.json())
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        with allure.step("获得otp"):
                            secretKey = get_json()['email']['secretKey']
                            totp = pyotp.TOTP(secretKey)
                            mfaVerificationCode = totp.now()
                        with allure.step("获得data"):
                            data = {
                                'amount': str(float(i['config']['debit']['min'])),
                                'symbol': i['symbol'],
                                'otp': str(mfaVerificationCode),
                                'direction': 'DEBIT',
                                'external_id': 'jjikkjjh008'
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
                        with allure.step("把数字货币从cabital转移到bybit账户"):
                            r1 = session.request('POST',
                                                 url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                 data=json.dumps(data), headers=connect_headers)
                        with allure.step("校验状态码"):
                            print('状态码'.format(r1.status_code))
                            # assert r1.status_code == 200, "http状态码不对，目前状态码是{}".format(r1.status_code)
                        with allure.step("校验返回值"):
                            assert r1.json()['code'] == 'PA029'
                        sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_018 把数字货币从cabital转移到bybit账户')
    def test_connect_transaction_018(self):
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
                            assert r.json()['status'] == 'SUCCESS', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                            r.text)
                        with allure.step("获得转移后cabital内币种balance金额"):
                            sleep(30)
                            balance_latest = ApiFunction.get_crypto_number(type=i['symbol'])
                        assert Decimal(balance_old) - Decimal(data['amount']) == Decimal(
                            balance_latest), "把{}从cabital转移到bybit账户错误，转移前balance是{},转移后balance是{}".format(i['symbol'],
                                                                                                          balance_old,
                                                                                                          balance_latest)
    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_019 从cabital转移到bybit账户并且关联C+T交易')
    def test_connect_transaction_019(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("换汇"):
            for i in ApiFunction.get_cfx_list():
                for y in get_json()['cash_list']:
                    if y in i:
                        with allure.step('换汇'):
                            transaction = ApiFunction.cfx_random(i, i.split('-')[0])
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
                                'conversion_id': transaction['returnJson']['transaction']['transaction_id']
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
                        with allure.step("把数字货币从cabital转移到bybit账户并且关联C+T交易"):
                            r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                                data=json.dumps(data), headers=connect_headers, timeout=10)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['status'] == 'SUCCESS', "把BTC从cabital转移到bybit账户并且关联C+T交易错误，返回值是{}".format(
                                r.text)
                            sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_020从cabital转移到bybit账户并且关联C+T交易，Direct Debit的金额大于cfx交易的金额')
    def test_connect_transaction_020(self):
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
                    r = session.request('POST', url='{}/accounts/{}/conversions'.format(self.url, account_id),
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
                    'amount': str(Decimal(cfx_amount['buy_amount']) + Decimal('0.001')),
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
                r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                    data=json.dumps(data), headers=connect_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA032', "Direct Debit的金额大于cfx交易的金额错误，返回值是{}".format(r.text)
                sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_021 从cabital转移到bybit账户并且关联C+T交易，Direct Debit的金额 必须小于等于 cfx交易的金额')
    def test_connect_transaction_021(self):
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
                    r = session.request('POST', url='{}/accounts/{}/conversions'.format(self.url, account_id),
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
                    'amount': str(Decimal(cfx_amount['buy_amount']) - Decimal('0.001')),
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
                r = session.request('POST', url='{}/accounts/{}/transfers'.format(self.url, account_id),
                                    data=json.dumps(data), headers=connect_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()[
                           'status'] == 'SUCCESS', "从cabital转移到bybit账户并且关联C+T交易，Direct Debit的金额 必须小于等于 cfx交易的金额错误，返回值是{}".format(
                    r.text)
                sleep(30)

    @allure.description('账户操作相关--划转')
    @allure.title('test_connect_transaction_022 把数字货币从bybit转移到cabital账户')
    def test_connect_transaction_022(self):
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
                    if i['config']['credit']['allow']:
                        with allure.step("获得转移前cabital内币种balance金额"):
                            balance_old = ApiFunction.get_crypto_number(type=i['symbol'])
                        with allure.step("获得data"):
                            data = {
                                'amount': str(Decimal(i['config']['credit']['max']) + Decimal('2.456')),
                                'symbol': i['symbol'],
                                'direction': 'CREDIT',
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
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['status'] == 'SUCCESS', "把{}从cabital转移到bybit账户错误，返回值是{}".format(i['symbol'],
                                                                                                            r.text)
                        with allure.step("获得转移后cabital内币种balance金额"):
                            sleep(30)
                            balance_latest = ApiFunction.get_crypto_number(type=i['symbol'])
                        assert Decimal(balance_old) + Decimal(data['amount']) == Decimal(
                            balance_latest), "把{}从bybit转移到cabital账户错误，转移前balance是{},转移后balance是{}".format(i['symbol'],
                                                                                                          balance_old,
                                                                                                          balance_latest)

    @allure.title('test_connect_recon_001 对账 - 划转交易详情查询成功')
    @allure.description('connect 对账接口/api/v1/recon/transfers/{}')
    def test_connect_recon_001(self):
        external_id = '16'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/recon/transfers/{}'.format(external_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转详情使用错误transfer_id"):
            r = session.request('GET', url='{}recon/transfers/{}'.format(self.url, external_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transfer_id'] == 'f5946953-d422-4c54-846f-789fafd1c2b2', "对账 - 划转交易详情错误，返回值是{}".format(
                r.text)

    @allure.title('test_connect_recon_002  划转交易详情使用无效external_id')
    @allure.description('connect 对账接口/api/v1/recon/transfers/{}')
    def test_connect_recon_002(self):
        external_id = generate_string(15)
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/recon/transfers/{}'.format(external_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户划转详情使用错误transfer_id"):
            r = session.request('GET', url='{}recon/transfers/{}'.format(self.url, external_id),
                                headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'PA030', "对账 - 划转交易详情使用无效external_id错误，返回值是{}".format(r.text)
