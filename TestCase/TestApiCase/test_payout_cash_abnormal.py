from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout cash abnormal相关 testcases")
class TestPayoutCashAbnormalApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_cash_abnormal_001')
    @allure.description('确认&创建Payme VND法币提现交易-（提现金额小于最小金额or大于最大金额）')
    def test_payout_cash_abnormal_001(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step('获取法币最小和最大提现金额'):
            params = {
                'code': 'VND'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params,
                                headers=headers)
            amount_min = r.json()['payment_methods']['Bank Transfer']['min']
            amount_max = r.json()['payment_methods']['Bank Transfer']['max']
            amount_list = [str(int(amount_min)-1), str(int(amount_max)+1)]
        for i in amount_list:
            data = {
                "code": "VND",
                "amount": i,
                "payment_method": "Bank Transfer",
                "account_name": "NGUYEN VAN A",
                "account_number": "9704000000000018",
                "bic": "SBITVNVX"
            }
            with allure.step("确认Payme VND法币提现交易（提现金额小于最小金额or大于最大金额））"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r.json()['code'] == '103001', "确认Payme VND法币提现交易-（提现金额小于最小金额）返回值错误，当前返回值是{}".format(
                            r.text)
                    else:
                        assert r.json()['code'] == '103002', "确认Payme VND法币提现交易-（提现金额大于最大金额）返回值错误，当前返回值是{}".format(
                            r.text)
            with allure.step("创建Payme VND法币提现交易-失败（提现金额小于最小金额or大于最大金额））"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r2.json()['code'] == '103001', "创建Payme VND法币提现交易-（提现金额小于最小金额）返回值错误，当前返回值是{}".format(r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建Payme VND法币提现交易-（提现金额大于最大金额）返回值错误，当前返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_002')
    @allure.description('确认&创建Payme VND法币提现交易-错误account name')
    def test_payout_cash_abnormal_002(self):
        with allure.step("法币提现交易-错误account name"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "wrong name",
                "account_number": "9704000000000018",
                "bic": "SBITVNVX"
            }
            with allure.step("确认Payme VND法币提现交易-错误account name"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103015',\
                        "确认Payme VND法币提现交易-错误account name返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建Payme VND法币提现交易-错误account name"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103015',\
                        "创建Payme VND法币提现交易-错误account name返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_003')
    @allure.description('确认&创建Payme VND法币提现交易-错误Account number')
    def test_payout_cash_abnormal_003(self):
        with allure.step("法币提现交易-错误Account number"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "NGUYEN VAN A",
                "account_number": "123456",
                "bic": "SBITVNVX"
            }
            with allure.step("确认Payme VND法币提现交易-错误Account number"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103024', \
                        "确认Payme VND法币提现交易-错误Account number返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建Payme VND法币提现交易-Account number"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103024', \
                        "创建Payme VND法币提现交易-错误Account number返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_004')
    @allure.description('创建&确认Payme VND法币提现交易-Invalid bic (swift)')
    def test_payout_cash_abnormal_004(self):
        with allure.step("法币提现交易-错误Swift code"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "NGUYEN VAN A",
                "account_number": "9704000000000018",
                "bic": "ABCDCH1234"
            }
            with allure.step("确认Payme VND法币提现交易-错误Swift code"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103028', \
                        "确认Payme VND法币提现交易-错误Swift code返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建Payme VND法币提现交易-Swift code"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL',
                                                         account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103028', \
                        "创建Payme VND法币提现交易-错误Swift code返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_005')
    @allure.description('确认&创建Payme VND法币提现交易-错误Payment method')
    def test_payout_cash_abnormal_005(self):
        with allure.step("法币提现交易-错误Payment method"):
            headers['Accept-Language'] = 'en-US'
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "123",
                "account_name": "NGUYEN VAN A",
                "account_number": "9704000000000018",
                "bic": "SBITVNVX"
            }
            with allure.step("确认Payme VND法币提现交易-错误Payment method"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103020', \
                        "确认Payme VND法币提现交易-错误Payment method返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建Payme VND法币提现交易-Payment method"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL',
                                                         account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103020', \
                        "创建Payme VND法币提现交易-错误Payment method返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_006')
    @allure.description('确认&创建BRL-PIX—CPF法币提现交易-（提现金额小于最小金额or大于最大金额）')
    def test_payout_cash_abnormal_006(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step('获取法币最小和最大提现金额'):
            params = {
                'code': 'BRL'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params,
                                headers=headers)
            amount_pix_min = r.json()['payment_methods']['PIX']['min']
            amount_pix_max = r.json()['payment_methods']['PIX']['max']
            amount_list = [str(int(amount_pix_min)-1), str(int(amount_pix_max)+1)]
        for i in amount_list:
            data = {
                "code": "BRL",
                "amount": i,
                "payment_method": "PIX",
                "pix_key_type": 1,
                "cpf": "718.638.715-27",
                "account_name": "Richard External QA"
            }
            with allure.step("确认BRL-PIX—CPF法币提现交易（提现金额小于最小金额or大于最大金额））"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r.json()['code'] == '103001', "确认BRL-PIX—CPF法币提现交易-（提现金额小于最小金额）返回值错误，当前返回值是{}".format(
                            r.json()['code'])
                    else:
                        assert r.json()['code'] == '103002', "确认BRL-PIX—CPF法币提现交易-（提现金额大于最大金额）返回值错误，当前返回值是{}".format(
                            r.json()['code'])
            with allure.step("创建BRL-PIX—CPF法币提现交易-失败（提现金额小于最小金额or大于最大金额））"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r2.json()['code'] == '103001', "创建BRL-PIX—CPF法币提现交易-（提现金额小于最小金额）返回值错误，当前返回值是{}".format(r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建BRL-PIX—CPF法币提现交易-（提现金额大于最大金额）返回值错误，当前返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_007')
    @allure.description('确认&创建BRL-Ted法币提现交易-（提现金额小于最小金额or大于最大金额）')
    def test_payout_cash_abnormal_007(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step('获取法币最小和最大提现金额'):
            params = {
                'code': 'BRL'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params,
                                headers=headers)
            amount_ted_min = r.json()['payment_methods']['Bank Transfer']['min']
            amount_ted_max = r.json()['payment_methods']['Bank Transfer']['max']
            amount_list = [str(int(amount_ted_min) - 1), str(int(amount_ted_max) + 1)]
        for i in amount_list:
            data = {
                "code": "BRL",
                "amount": i,
                "payment_method": "Bank Transfer",
                "cpf": "718.638.715-27",
                "bank_name": "Banco Santander (Brasil) S.A. (033)",
                "bank_code": "90240",
                "branch_code": "0123",
                "account_type": 2,
                "account_name": "Richard External QA",
                "account_number": "1234567890"
            }
            with allure.step("确认BRL-Ted法币提现交易（提现金额小于最小金额or大于最大金额））"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r.json()['code'] == '103001', "确认BRL-Ted法币提现交易-（提现金额小于最小金额）返回值错误，当前返回值是{}".format(
                            r.json()['code'])
                    else:
                        assert r.json()['code'] == '103002', "确认BRL-Ted法币提现交易-（提现金额大于最大金额）返回值错误，当前返回值是{}".format(
                            r.json()['code'])
            with allure.step("创建BRL-Ted法币提现交易-失败（提现金额小于最小金额or大于最大金额））"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r2.json()['code'] == '103001', "创建BRL-Ted法币提现交易-（提现金额小于最小金额）返回值错误，当前返回值是{}".format(
                            r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建BRL-Ted法币提现交易-（提现金额大于最大金额）返回值错误，当前返回值是{}".format(
                            r2.text)

    @allure.title('test_payout_cash_abnormal_008')
    @allure.description('确认&创建BRL提现提现交易，BRL-PIX—CPF（输入错误CPF）')
    def test_payout_cash_abnormal_008(self):
        with allure.step("法币提现交易-输入错误CPF"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "BRL",
                "amount": "130",
                "payment_method": "PIX",
                "pix_key_type": 1,
                "cpf": "718.638.715-28",
                "account_name": "Richard External QA"
            }
            with allure.step("确认BRL提现提现交易，BRL-PIX—CPF，输入错误CPF"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103041', \
                        "确认BRL提现提现交易，BRL-PIX—CPF，输入错误CPF，接口返回值是{}".format(r.text)
            with allure.step("创建BRL提现提现交易，BRL-PIX—CPF，输入错误CPF"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL',
                                                         account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103041', \
                        "创建BRL提现提现交易，BRL-PIX—CPF，输入错误CPF，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_009')
    @allure.description('确认&创建BRL提现提现交易，BRL-Ted（输入错误CPF）')
    def test_payout_cash_abnormal_009(self):
        with allure.step("法币提现交易-输入错误CPF"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "BRL",
                "amount": "300001",
                "payment_method": "Bank Transfer",
                "cpf": "718.638.715-28",
                "bank_name": "Banco Santander (Brasil) S.A. (033)",
                "bank_code": "90240",
                "branch_code": "0123",
                "account_type": 2,
                "account_name": "Richard External QA",
                "account_number": "1234567890"
            }
            with allure.step("确认BRL提现提现交易，BRL-Ted，输入错误CPF"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103041', \
                        "确认BRL提现提现交易，BRL-Ted，输入错误CPF，接口返回值是{}".format(r.text)
            with allure.step("创建BRL提现提现交易，BRL-Ted，输入错误CPF"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL',
                                                         account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103041', \
                        "创建BRL提现提现交易，BRL-Ted，输入错误CPF，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_010')
    @allure.description('确认&创建BRL-PIX_CPF提现交易-（输入错误account name）')
    def test_payout_cash_abnormal_010(self):
        with allure.step("法币提现交易-错误account name"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "BRL",
                "amount": "300000",
                "payment_method": "PIX",
                "pix_key_type": 1,
                "cpf": "718.638.715-27",
                "account_name": "Richard External AQ"
            }
            with allure.step("确认BRL-PIX_CPF法币提现交易-错误account name"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103015', \
                        "确认BRL-PIX_CPF法币提现交易-错误account name返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建BRL-PIX_CPF法币提现交易-错误account name"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103015', \
                        "创建BRL-PIX_CPF法币提现交易-错误account name返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_011')
    @allure.description('确认&创建BRL-Ted提现交易-（输入错误account name）')
    def test_payout_cash_abnormal_011(self):
        with allure.step("法币提现交易-错误account name"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "BRL",
                "amount": "130",
                "payment_method": "Bank Transfer",
                "cpf": "718.638.715-27",
                "bank_name": "Banco Santander (Brasil) S.A. (033)",
                "bank_code": "90240",
                "branch_code": "0123",
                "account_type": 2,
                "account_name": "Richard External AQ",
                "account_number": "1234567890"
            }
            with allure.step("确认BRL-Ted法币提现交易-错误account name"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103015', \
                        "确认BRL-Ted法币提现交易-错误account name返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建BRL-Ted法币提现交易-错误account name"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103015', \
                        "创建BRL-Ted法币提现交易-错误account name返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_012')
    @allure.description('确认&创建EUR法币提现交易-（提现金额小于最小金额or大于最大金额）')
    def test_payout_cash_abnormal_012(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step('获取法币最小和最大提现金额'):
            params = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params,
                                headers=headers)
            amount_min = r.json()['payment_methods'][r.json()['supported_payment_methods']]['min']
            amount_max = r.json()['payment_methods'][r.json()['supported_payment_methods']]['max']
            amount_list = [str(int(amount_min)-1), str(int(amount_max)+1)]
        for i in amount_list:
            data = {
                "code": "EUR",
                "amount": i,
                "payment_method": "SEPA",
                "account_name": "Richard External QA",
                "iban": "AT234567891827364532",
                "bic": "BKAUATWWXXX"
            }
            with allure.step("确认EUR法币提现交易（提现金额小于最小金额or大于最大金额））"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r.json()['code'] == '103001', "确认EUR法币提现交易-（提现金额小于最小金额）返回值错误，当前返回值是{}".format(
                            r.text)
                    else:
                        assert r.json()['code'] == '103002', "确认EUR法币提现交易-（提现金额大于最大金额）返回值错误，当前返回值是{}".format(
                            r.text)
            with allure.step("创建EUR法币提现交易-失败（提现金额小于最小金额or大于最大金额））"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                secretKey = get_json()['secretKey']
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r2.json()['code'] == '103001', "创建EUR法币提现交易-（提现金额小于最小金额）返回值错误，当前返回值是{}".format(r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建EUR法币提现交易-（提现金额大于最大金额）返回值错误，当前返回值是{}".format(r2.text)
    #
    # @allure.title('test_payout_cash_033')
    # @allure.description('创建法币提现交易：BCB GBP失败')
    # def test_payout_cash_033(self):
    #     with allure.step("从开启法币提现画面接口获取name list"):
    #         headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
    #             account=get_json()['email']['payout_email'])
    #         params = {
    #             'code': 'GBP'
    #         }
    #         r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
    #         account_name = r.json()['name_list']
    #     with allure.step("创建GBP法币提现交易"):
    #         code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
    #         secretKey = get_json()['secretKey']
    #         totp = pyotp.TOTP(secretKey)
    #         mfaVerificationCode = totp.now()
    #         headers['X-Mfa-Otp'] = str(mfaVerificationCode)
    #         headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
    #         data = {
    #             "code": "GBP",
    #             "amount": "5.61",
    #             "payment_method": "Faster Payments",
    #             "account_name": account_name[0],
    #             "account_number": "00003162",
    #             "sort_code": "040541"
    #         }
    #         r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
    #                             headers=headers)
    #         ApiFunction.add_headers()
    #         with allure.step("状态码和返回值"):
    #             logger.info('状态码是{}'.format(str(r.status_code)))
    #             logger.info('返回值是{}'.format(str(r.text)))
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert 'txn_id' in r.text, "开启法币提现画面错误，返回值是{}".format(r.text)
    #
    # @allure.title('test_payout_019')
    # @allure.description('法币提现获得信息，不传code')
    # def test_payout_019(self):
    #     with allure.step("法币提现获得信息，不传code"):
    #         data = {
    #             'code': '',
    #             'payment_method': ''
    #         }
    #         r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         assert r.json()['code'] == '100000', "法币提现获得信息，不传code错误，返回值是{}".format(r.text)
    # #
    # #     @allure.title('test_payout_020')
    # #     @allure.description('法币提现英镑获得信息，白名单排序')
    # #     def test_payout_020(self):
    # #         with allure.step("法币提现英镑获得信息，白名单排序"):
    # #             data = {
    # #                 'code': 'GBP',
    # #                 'payment_method': 'Faster Payments'
    # #             }
    # #             r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
    # #         with allure.step("校验状态码"):
    # #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    # #         assert "Faster Payments" in r.text, "法币提现英镑获得信息，白名单排序错误，返回值是{}".format(r.text)
    # #         a = 1
    # #         with allure.step("确保1在前，0在后"):
    # #             for i in r.json()['account_names']:
    # #                 if a == 1:
    # #                     if i['status'] == 0:
    # #                         a = 0
    # #                 elif a == 0:
    # #                     assert i['status'] == 0, '白名单排序问题，没1在前0在后。'
    # #
    #
    #
    # @allure.title('test_payout_023')
    # @allure.description('BCB EUR法币提现GBP法币用户名字带有中文字符提现失败错误')
    # def test_payout_023(self):
    #     with allure.step("开启GBP法币提现画面"):
    #         headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
    #             account=get_json()['email']['payout_email'])
    #         params = {
    #             'code': 'GBP'
    #         }
    #         r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
    #         account_name = r.json()['name_list']
    #         logger.info('提款名字是{}'.format(account_name))
    #     with allure.step("GBP法币提现"):
    #         code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
    #         secretKey = get_json()['secretKey']
    #         totp = pyotp.TOTP(secretKey)
    #         mfaVerificationCode = totp.now()
    #         headers['X-Mfa-Otp'] = str(mfaVerificationCode)
    #         headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
    #         data = {
    #             "code": "GBP",
    #             "amount": "26.81",
    #             "payment_method": "Faster Payments",
    #             "account_name": account_name[3],
    #             "account_number": "00003162",
    #             "sort_code": "040541"
    #         }
    #         r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
    #                             headers=headers)
    #         ApiFunction.add_headers()
    #         with allure.step("状态码和返回值"):
    #             logger.info('状态码是{}'.format(str(r.status_code)))
    #             logger.info('返回值是{}'.format(str(r.text)))
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert r.json()['code'] == '103015', "GBP法币用户名字带有中文字符提现失败错误，返回值是{}".format(r.text)
    #
    # @allure.title('test_payout_024')
    # @allure.description('Faster Payments GBP法币提现')
    # def test_payout_024(self):
    #     with allure.step("开启GBP法币提现画面"):
    #         headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
    #             account=get_json()['email']['payout_email'])
    #         params = {
    #             'code': 'GBP'
    #         }
    #         r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
    #         account_name = r.json()['name_list']
    #         logger.info('account_name是{}'.format(account_name))
    #     with allure.step("Faster Payments GBP法币提现"):
    #         code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
    #         secretKey = get_json()['secretKey']
    #         totp = pyotp.TOTP(secretKey)
    #         mfaVerificationCode = totp.now()
    #         headers['X-Mfa-Otp'] = str(mfaVerificationCode)
    #         headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
    #         data = {
    #             "code": "GBP",
    #             "amount": "23.81",
    #             "payment_method": "Faster Payments",
    #             "account_name": account_name[0],
    #             "account_number": "00003162",
    #             "sort_code": "040541"
    #         }
    #         r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
    #                             headers=headers)
    #         with allure.step("状态码和返回值"):
    #             logger.info('状态码是{}'.format(str(r.status_code)))
    #             logger.info('返回值是{}'.format(str(r.text)))
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert 'txn_id' in r.text, "BCB GBP法币提现错误，返回值是{}".format(r.text)
    # #
    # #     @allure.title('test_payout_025')
    #     @allure.description('BTC确认Crypto提现交易超过每日限额')
    #     def test_payout_025(self):
    #         with allure.step("BTC确认Crypto提现交易"):
    #             data = {
    #                 "amount": "2",
    #                 "code": "BTC",
    #                 "address": "tb1q38mwu50xludgz4r52n2v0q6jwlysjgz4zkk3kl",
    #             }
    #             r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data),
    #                                 headers=headers)
    #             with allure.step("状态码和返回值"):
    #                 logger.info('状态码是{}'.format(str(r.status_code)))
    #                 logger.info('返回值是{}'.format(str(r.text)))
    #             with allure.step("校验状态码"):
    #                 assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #             with allure.step("校验返回值"):
    #                 assert r.json()['code'] == '103031', "BTC确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)
    #
    #     @allure.title('test_payout_026')
    #     @allure.description('ETH确认Crypto提现交易超过每日限额')
    #     def test_payout_026(self):
    #         with allure.step("ETH确认Crypto提现交易"):
    #             data = {
    #                 "amount": "40.018",
    #                 "code": "ETH",
    #                 "address": "0xA7185FBEE96B605709D9659894066dF21cc87f05",
    #                 "method": "ERC20"
    #             }
    #             r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data),
    #                                 headers=headers)
    #             with allure.step("状态码和返回值"):
    #                 logger.info('状态码是{}'.format(str(r.status_code)))
    #                 logger.info('返回值是{}'.format(str(r.text)))
    #             with allure.step("校验状态码"):
    #                 assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #             with allure.step("校验返回值"):
    #                 assert r.json()['code'] == '103031', "ETH确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)
    #
    #     @allure.title('test_payout_027')
    #     @allure.description('USDT确认Crypto提现交易超过每日限额')
    #     def test_payout_027(self):
    #         with allure.step("USDT确认Crypto提现交易"):
    #             data = {
    #                 "amount": "20000",
    #                 "code": "USDT",
    #                 "address": "0xA7185FBEE96B605709D9659894066dF21cc87f05",
    #                 "method": "ERC20"
    #             }
    #             r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data),
    #                                 headers=headers)
    #             with allure.step("状态码和返回值"):
    #                 logger.info('状态码是{}'.format(str(r.status_code)))
    #                 logger.info('返回值是{}'.format(str(r.text)))
    #             with allure.step("校验状态码"):
    #                 assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #             with allure.step("校验返回值"):
    #                 assert r.json()['code'] == '103031', "USDT确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)
    #
    #     @allure.title('test_payout_028')
    #     @allure.description('MFA认证提现ETH成功')
    #     def test_payout_028(self):
    #         ApiFunction.get_payout_transaction_id(amount='0.02', address='0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C',
    #                                               code_type='ETH')
    #
    #     @allure.title('test_payout_029')
    #     @allure.description('MFA认证提现BTC成功')
    #     def test_payout_029(self):
    #         ApiFunction.get_payout_transaction_id(amount='0.01', address='tb1q3fhjd9f0th907cuym9dtyzpy3zu9tn6205jhwm',
    #                                               code_type='BTC')
    #
    #     @allure.title('test_payout_030')
    #     @allure.description('MFA认证提现USDT成功')
    #     def test_payout_030(self):
    #         ApiFunction.get_payout_transaction_id(amount='50.01', address='0x0f841561A9e5c95926b234FC5fA12cDcf9BEB378',
    #                                               code_type='USDT')
    #
    #     @allure.title('test_payout_031')
    #     @allure.description('确认法币提现交易，bic使用小写')
    #     def test_payout_031(self):
    #         with allure.step("确认法币提现交易"):
    #             data = {
    #                 "code": "EUR",
    #                 "amount": "27.51",
    #                 "payment_method": "SEPA",
    #                 "account_name": "yilei",
    #                 "iban": "AT234567891827364532",
    #                 "bic": "bkauatwwxxx"
    #             }
    #             r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
    #                                 headers=headers)
    #             with allure.step("状态码和返回值"):
    #                 logger.info('状态码是{}'.format(str(r.status_code)))
    #                 logger.info('返回值是{}'.format(str(r.text)))
    #             with allure.step("校验状态码"):
    #                 assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #             with allure.step("校验返回值"):
    #                 assert r.json() == {}, "开启法币提现画面错误，返回值是{}".format(r.text)
    #
    #     @allure.title('test_payout_032')
    #     @allure.description('BCB EUR法币提现使用不支持的国家')
    #     def test_payout_032(self):
    #         with allure.step("开启法币提现画面"):
    #             headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
    #                 account=get_json()['email']['payout_email'])
    #             params = {
    #                 'code': 'EUR'
    #             }
    #             r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
    #             account_name = r.json()['name_list']
    #         with allure.step("法币提现"):
    #             code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
    #             secretKey = get_json()['secretKey']
    #             totp = pyotp.TOTP(secretKey)
    #             mfaVerificationCode = totp.now()
    #             headers['X-Mfa-Otp'] = str(mfaVerificationCode)
    #             headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
    #             data = {
    #                 "code": "EUR",
    #                 "amount": "27.61",
    #                 "payment_method": "SEPA",
    #                 "account_name": account_name[0],
    #                 "iban": "BE09967206444557",
    #                 "bic": "ITHOMTM2"
    #             }
    #             r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
    #                                 headers=headers)
    #             with allure.step("状态码和返回值"):
    #                 logger.info('状态码是{}'.format(str(r.status_code)))
    #                 logger.info('返回值是{}'.format(str(r.text)))
    #             with allure.step("校验状态码"):
    #                 assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #             with allure.step("校验返回值"):
    #                 assert r.json()['code'] == '103036', "EUR法币提现使用不支持的国家错误，返回值是{}".format(r.text)
    #
    #     @allure.title('test_payout_033')
    #     @allure.description('BTC使用带有特殊字符的地址提现会报错')
    #     def test_payout_033(self):
    #         headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
    #             account=get_json()['email']['payout_email'])
    #         code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
    #         secretKey = get_json()['secretKey']
    #         totp = pyotp.TOTP(secretKey)
    #         mfaVerificationCode = totp.now()
    #         headers['X-Mfa-Otp'] = str(mfaVerificationCode)
    #         headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
    #         data = {
    #             "amount": '0.012',
    #             "code": 'BTC',
    #             "address": 'tb1q3fhjd9f0th907cuym9dtyzpy3zu9tn6205jh@m',
    #             "method": "ERC20"
    #         }
    #         r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
    #                             headers=headers)
    #         with allure.step("状态码和返回值"):
    #             logger.info('状态码是{}'.format(str(r.status_code)))
    #             logger.info('返回值是{}'.format(str(r.text)))
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         assert r.json()['code'] == '103035', "BTC使用带有特殊字符的地址提现会报错"
    #
    #     @allure.title('test_payout_034')
    #     @allure.description('确认CHF提现交易，bic使用小写')
    #     def test_payout_034(self):
    #         with allure.step("确认法币提现交易"):
    #             data = {
    #                 "code": "CHF",
    #                 "amount": "35.51",
    #                 "payment_method": "SIC",
    #                 "account_name": "yilei",
    #                 "iban": "AT234567891827364532",
    #                 "bic": "bkauatwwxxx"
    #             }
    #             r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
    #                                 headers=headers)
    #             with allure.step("校验状态码"):
    #                 assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #             with allure.step("校验返回值"):
    #                 assert r.json() == {}, "开启法币提现画面错误，返回值是{}".format(r.text)
    #
    #     @allure.title('test_payout_035')
    #     @allure.description('SIC CHF法币提现使用不支持的国家')
    #     def test_payout_035(self):
    #         with allure.step("开启法币提现画面"):
    #             headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
    #                 account=get_json()['email']['payout_email'])
    #             params = {
    #                 'code': 'CHF'
    #             }
    #             r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
    #             account_name = r.json()['name_list']
    #         with allure.step("法币提现"):
    #             code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
    #             secretKey = get_json()['secretKey']
    #             totp = pyotp.TOTP(secretKey)
    #             mfaVerificationCode = totp.now()
    #             headers['X-Mfa-Otp'] = str(mfaVerificationCode)
    #             headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
    #             data = {
    #                 "code": "CHF",
    #                 "amount": "35.61",
    #                 "payment_method": "SIC",
    #                 "account_name": account_name[0],
    #                 "iban": "BE09967206444557",
    #                 "bic": "ITHOMTM2"
    #             }
    #             r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
    #                                 headers=headers)
    #             with allure.step("状态码和返回值"):
    #                 logger.info('状态码是{}'.format(str(r.status_code)))
    #                 logger.info('返回值是{}'.format(str(r.text)))
    #             with allure.step("校验状态码"):
    #                 assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #             with allure.step("校验返回值"):
    #                 assert r.json()['code'] == '103036', "EUR法币提现使用不支持的国家错误，返回值是{}".format(r.text)
    #
