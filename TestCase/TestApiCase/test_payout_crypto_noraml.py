from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout crypto normal相关 testcases")
class TestPayoutCryptoNormalApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_crypto_normal_001')
    @allure.description('获取提现费率和提现限制，并检查you will receive金额是否正确')
    def test_payout_crypto_normal_001(self):
        crypto_list = get_json()['crypto_list']
        for i in crypto_list:
            with allure.step("获取提现费率和提现限制"):
                data = {
                    "amount": "40.99",
                    "code": i,
                }
                r = session.request('POST', url='{}/pay/withdraw/verification'.format(env_url), data=json.dumps(data),
                                    headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                logger.info('接口返回值是{}'.format(str(r.text)))
                if i not in crypto_list:
                    raise Exception(("查看法币列表是否新增", crypto_list), ('接口返回', r.json()))
                elif i == 'BTC':
                    assert r.json()['fee'] == '0.0006', '{}提现费率错误，返回值为{}}'.format(i, r.text)
                    assert r.json()['min_amount'] == 0.001, '{}提现最小金额错误，返回值为{}}'.format(i, r.text)
                    assert r.json()['receive_amount'] == str(Decimal(data['amount']) - Decimal(r.json()['fee']))
                elif i == 'ETH':
                    assert r.json()['fee'] == '0.004', '{}提现费率错误，返回值为{}}'.format(i, r.text)
                    assert r.json()['min_amount'] == 0.02, '{}提现最小金额错误，返回值为{}}'.format(i, r.text)
                    assert r.json()['receive_amount'] == str(Decimal(data['amount']) - Decimal(r.json()['fee']))
                elif i == 'USDT':
                    assert r.json()['fee'] == '12', '{}提现费率错误，返回值为{}}'.format(i, r.text)
                    assert r.json()['min_amount'] == 40, '{}提现最小金额错误，返回值为{}}'.format(i, r.text)
                    assert r.json()['receive_amount'] == str(Decimal(data['amount']) - Decimal(r.json()['fee']))

    @allure.title('test_payout_crypto_normal_002')
    @allure.description('获得所有数字货币提现币种')
    def test_payout_crypto_normal_002(self):
        with allure.step("提现币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, 'crypto'), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'crypto' in r.text, "获得数字货币提现币种错误，返回值是{}".format(r.text)

    @allure.title('test_payout_crypto_normal_003')
    @allure.description('确认&创建BTC虚拟货币提现交易')
    def test_payout_crypto_normal_003(self):
        with allure.step("BTC虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '0.02',
                "code": 'BTC',
                "address": 'bc1qa03ha5pgkm0dyl63gkzwr035qxphjf60dw4wnn',
                "method": "ERC20"
            }
        with allure.step("确认BTC虚拟货币提现交易"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json() == {}, "确认BTC虚拟货币提现交易错误，返回值是{}".format(r.text)
        with allure.step("创建ETH虚拟货币提现交易"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            mfaVerificationCode = get_mfa_code()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            r2 = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                                 headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r2.status_code)))
                logger.info('返回值是{}'.format(str(r2.text)))
            with allure.step("校验状态码"):
                assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            return r2.json()['transaction_id']

    @allure.title('test_payout_crypto_normal_004')
    @allure.description('确认&创建ETH虚拟货币提现交易')
    def test_payout_crypto_normal_004(self):
        with allure.step("ETH虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '0.02',
                "code": 'ETH',
                "address": '0x17b9798852E4d4c24a38fb56Ba4080BC39E5279d',
                "method": "ERC20"
            }
        with allure.step("确认ETH虚拟货币提现交易"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json() == {}, "确认ETH虚拟货币提现交易错误，返回值是{}".format(r.text)
        with allure.step("创建ETH虚拟货币提现交易"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            mfaVerificationCode = get_mfa_code()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            r2 = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                                 headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r2.status_code)))
                logger.info('返回值是{}'.format(str(r2.text)))
            with allure.step("校验状态码"):
                assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            return r2.json()['transaction_id']

    @allure.title('test_payout_crypto_normal_005')
    @allure.description('确认&创建USDT虚拟货币提现交易')
    def test_payout_crypto_normal_005(self):
        with allure.step("USDT虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '40',
                "code": 'USDT',
                "address": '0xA7185FBEE96B605709D9659894066dF21cc87f05',
                "method": "ERC20"
            }
        with allure.step("确认USDT虚拟货币提现交易"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json() == {}, "确认USDT虚拟货币提现交易错误，返回值是{}".format(r.text)
        with allure.step("创建USDT虚拟货币提现交易"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            mfaVerificationCode = get_mfa_code()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            r2 = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                                 headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r2.status_code)))
                logger.info('返回值是{}'.format(str(r2.text)))
            with allure.step("校验状态码"):
                assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            return r2.json()['transaction_id']

    @allure.title('test_payout_crypto_normal_006')
    @allure.description('BTC确认Crypto提现交易超过每日限额')
    def test_payout_crypto_normal_006(self):
        with allure.step("BTC确认Crypto提现交易"):
            data = {
                "amount": "2",
                "code": "BTC",
                "address": "tb1q38mwu50xludgz4r52n2v0q6jwlysjgz4zkk3kl",
            }
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103031', "BTC确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)

    @allure.title('test_payout_crypto_normal_007')
    @allure.description('ETH确认Crypto提现交易超过每日限额')
    def test_payout_crypto_normal_007(self):
        with allure.step("ETH确认Crypto提现交易"):
            data = {
                "amount": "40.018",
                "code": "ETH",
                "address": "0xA7185FBEE96B605709D9659894066dF21cc87f05",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103031', "ETH确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)

    @allure.title('test_payout_crypto_normal_008')
    @allure.description('USDT确认Crypto提现交易超过每日限额')
    def test_payout_crypto_normal_008(self):
        with allure.step("USDT确认Crypto提现交易"):
            data = {
                "amount": "20000",
                "code": "USDT",
                "address": "0xA7185FBEE96B605709D9659894066dF21cc87f05",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103031', "USDT确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)
