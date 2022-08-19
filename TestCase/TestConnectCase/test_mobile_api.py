from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api connect 相关 testcases")
class TestConnectApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_connect_001')
    @allure.description('获取合作方配置')
    def test_connect_001(self):
        with allure.step("获取合作方配置"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(self.url, get_json()['connect'][
                get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['configs'] is not None, "获取合作方配置错误，返回值是{}".format(r.text)

    @allure.title('test_connect_002')
    @allure.description('transfer 预校验')
    def test_connect_002(self):
        with allure.step("获取合作方配置"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(self.url, get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), headers=headers)
            for i in r.json()['configs']:
                amount = str(float(i['withdraw']['amount_limit']['min']) + float(0.002))
                data = {
                    "amount": amount,
                    "symbol": i['code'],
                    "direction": "DEBIT"
                }
                with allure.step("transfer 预校验"):
                    r = session.request('POST', url='{}/connect/{}/transfer/confirm'.format(self.url, get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "transfer 预校验错误，返回值是{}".format(r.text)

    @allure.title('test_connect_003')
    @allure.description('transfer 预校验小于最小值')
    def test_connect_003(self):
        with allure.step("获取合作方配置"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(self.url, get_json()['connect'][
                get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), headers=headers)
            for i in r.json()['configs']:
                amount = str(float(i['withdraw']['amount_limit']['min']) - float(0.0001))
                data = {
                    "amount": amount,
                    "symbol": i['code'],
                    "direction": "DEBIT"
                }
                with allure.step("transfer 预校验小于最小值"):
                    r = session.request('POST', url='{}/connect/{}/transfer/confirm'.format(self.url, get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == 'PA003', "transfer 预校验小于最小值错误，返回值是{}".format(r.text)

    @allure.title('test_connect_004 transfer 交易')
    @allure.description('transfer 交易')
    def test_connect_004(self):
        with allure.step("获取合作方配置"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(self.url, get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), headers=headers)
            for i in r.json()['configs']:
                with allure.step("获得transfer前金额"):
                    wallet_balance_old = ApiFunction.get_crypto_number(type=i['code'])
                amount = str(float(i['withdraw']['amount_limit']['min']) + float(0.001))
                data = {
                    "amount": amount,
                    "symbol": i['code'],
                    "direction": "DEBIT"
                }
                with allure.step("获取2fa code"):
                    mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
                    headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                with allure.step("transfer 交易"):
                    r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url, get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), data=json.dumps(data), headers=headers)
                    print(r.url)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['txn_id'] is not None, "transfer 交易错误，返回值是{}".format(r.text)
                    assert r.json()['status'] == 1, "transfer 交易错误，返回值是{}".format(r.text)
                sleep(15)
                with allure.step("获得transfer后金额"):
                    wallet_balance_latest = ApiFunction.get_crypto_number(type=i['code'])
                assert Decimal(wallet_balance_old) - Decimal(data['amount']) == Decimal(wallet_balance_latest), 'transfer币种是{},transfer前金额是{},transfer金额是{}，transfer后金额是{}'.format(i['symbol'], wallet_balance_old, data['amount'], wallet_balance_latest)

    @allure.title('test_connect_005')
    @allure.description('transfer 交易小于最小值')
    def test_connect_005(self):
        with allure.step("指定account"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
        with allure.step("获取合作方配置"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(self.url, get_json()['connect'][
                get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), headers=headers)
            for i in r.json()['crypto']:
                amount = str(float(i['withdraw']['amount_limit']['min']) - float(0.0001))
                data = {
                    "amount": amount,
                    "symbol": i['symbol'],
                    "direction": "DEBIT"
                }
                with allure.step("获取email code"):
                    code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                    headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                with allure.step("获取2fa code"):
                    secretKey = get_json()['secretKey']
                    totp = pyotp.TOTP(secretKey)
                    mfaVerificationCode = totp.now()
                    headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                with allure.step("transfer 交易"):
                    r = session.request('POST', url='{}/connect/{}/transfer'.format(self.url, get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == 'PA003', "transfer 交易错误，返回值是{}".format(r.text)
                sleep(45)



