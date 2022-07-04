from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout crypto abnormal相关 testcases")
class TestPayoutCryptoAbnormalApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_crypto_abnormal_001')
    @allure.description('确认&创建BTC虚拟货币提现交易-(提现金额小于最小金额)')
    def test_payout_crypto_abnormal_001(self):
        with allure.step("BTC虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '0.0009',
                "code": 'BTC',
                "address": 'bc1qa03ha5pgkm0dyl63gkzwr035qxphjf60dw4wnn',
                "method": "ERC20"
            }
        with allure.step("确认BTC虚拟货币提现交易-(提现金额小于最小金额)"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103001', "确认BTC虚拟货币提现交易-(提现金额小于最小金额)，返回值是{}".format(r.text)
        with allure.step("创建BTC虚拟货币提现交易"):
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
                assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r2.json()['code'] == '103001', \
                    "创建BTC虚拟货币提现交易-(提现金额小于最小数量)返回值错误，接口返回值是{}".format(r2.text)
            
    @allure.title('test_payout_crypto_abnormal_002')
    @allure.description('确认&创建BTC虚拟货币提现交易-错误地址（带有特殊字符的地址）')
    def test_payout_crypto_abnormal_002(self):
        with allure.step("BTC虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '0.001',
                "code": 'BTC',
                "address": 'bc1qa03ha5pgkm0dyl63gkzwr035qxphjf!#nn',
                "method": "ERC20"
            }
        with allure.step("确认BTC虚拟货币提现交易-错误地址（带有特殊字符的地址）"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103035', "确认BTC虚拟货币提现交易-错误地址（带有特殊字符的地址），返回值是{}".format(r.text)
        with allure.step("创建BTC虚拟货币提现交易"):
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
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json()['code'] == '103035', "BTC使用带有特殊字符的地址提现结果非预期，返回值为{}".format(r.text)

    @allure.title('test_payout_crypto_bnormal_003')
    @allure.description('确认&创建ETH虚拟货币提现交易-(提现金额小于最小金额')
    def test_payout_crypto_abnormal_003(self):
        with allure.step("ETH虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '0.019',
                "code": 'ETH',
                "address": '0x1145c02268E90a7EA4FD438c67EB499DcA9B1F87',
                "method": "ERC20"
            }
        with allure.step("确认ETH虚拟货币提现交易-(提现金额小于最小金额)"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103001', "确认ETH虚拟货币提现交易-(提现金额小于最小金额)，返回值是{}".format(r.text)
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
                assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r2.json()['code'] == '103001', \
                    "创建ETH虚拟货币提现交易-(提现金额小于最小金额)返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_crypto_abnormal_004')
    @allure.description('确认&创建ETH虚拟货币提现交易-错误地址（带有特殊字符的地址）')
    def test_payout_crypto_abnormal_004(self):
        with allure.step("ETH虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '0.02',
                "code": 'ETH',
                "address": 'bc1qa03ha5pgkm0dyl63gkzwr035qxphjf!#nn',
                "method": "ERC20"
            }
        with allure.step("确认ETH虚拟货币提现交易-错误地址（带有特殊字符的地址）"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103035', "确认ETH虚拟货币提现交易-错误地址（带有特殊字符的地址），返回值是{}".format(r.text)
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
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json()['code'] == '103035',  "ETH使用带有特殊字符的地址提现结果非预期，返回值为{}".format(r.text)

    @allure.title('test_payout_crypto_bnormal_005')
    @allure.description('确认&创建USDT虚拟货币提现交易-(提现金额小于最小金额)')
    def test_payout_crypto_abnormal_005(self):
        with allure.step("USDT虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '39.9',
                "code": 'USDT',
                "address": '0xA7185FBEE96B605709D9659894066dF21cc87f05',
                "method": "ERC20"
            }
        with allure.step("确认USDT虚拟货币提现交易-(提现金额小于最小金额)"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103001', "确认USDT虚拟货币提现交易-(提现金额小于最小金额)，返回值是{}".format(r.text)
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
                assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r2.json()['code'] == '103001', \
                    "创建USDT虚拟货币提现交易-(提现金额小于最小金额)返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_crypto_abnormal_006')
    @allure.description('确认&创建USDT虚拟货币提现交易-错误地址（带有特殊字符的地址）')
    def test_payout_crypto_abnormal_006(self):
        with allure.step("ETH虚拟货币提现"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "amount": '40',
                "code": 'USDT',
                "address": '0x1145c02268E90a7EA4FD438c67EB499DcA9B!#nn',
                "method": "ERC20"
            }
        with allure.step("确认BTC虚拟货币提现交易-错误地址（带有特殊字符的地址）"):
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url),
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103035', "确认USDT虚拟货币提现交易-错误地址（带有特殊字符的地址），返回值是{}".format(r.text)
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
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json()['code'] == '103035',  "USDT使用带有特殊字符的地址提现结果非预期，返回值为{}".format(r.text)
