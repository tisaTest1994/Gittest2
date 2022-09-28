from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout cash abnormal相关 testcases")
class TestPayoutCashAbnormalApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_cash_abnormal_001')
    @allure.description('确认&创建Payme VND法币提现交易-(提现金额小于最小金额or大于最大金额)')
    @pytest.mark.skip(reason='提现现在未开放vnd，先不管')
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
            with allure.step("确认Payme VND法币提现交易(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                        assert r.json()['code'] == '103001', "确认Payme VND法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(
                            r.text)
                    else:
                        assert r.json()['code'] == '103002', "确认Payme VND法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(
                            r.text)
            with allure.step("创建Payme VND法币提现交易-失败(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                        assert r2.json()['code'] == '103001', "创建Payme VND法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建Payme VND法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_002')
    @allure.description('确认&创建Payme VND法币提现交易-错误account name')
    @pytest.mark.skip(reason='提现现在未开放vnd，先不管')
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
                mfaVerificationCode = get_mfa_code()
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
    @pytest.mark.skip(reason='提现现在未开放vnd，先不管')
    def test_payout_cash_abnormal_003(self):
        with allure.step("法币提现交易-错误Account number"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "NGUYEN VAN A",
                "account_number": "abc",
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
                mfaVerificationCode = get_mfa_code()
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
    @pytest.mark.skip(reason='提现现在未开放vnd，先不管')
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
                mfaVerificationCode = get_mfa_code()
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
    @pytest.mark.skip(reason='提现现在未开放vnd，先不管')
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
                mfaVerificationCode = get_mfa_code()
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
    @allure.description('确认&创建BRL-PIX—CPF法币提现交易-(提现金额小于最小金额or大于最大金额)')
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
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
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
            with allure.step("确认BRL-PIX—CPF法币提现交易(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r.json()['code'] == '103001', "确认BRL-PIX—CPF法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(
                            r.json()['code'])
                    else:
                        assert r.json()['code'] == '103002', "确认BRL-PIX—CPF法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(
                            r.json()['code'])
            with allure.step("创建BRL-PIX—CPF法币提现交易-(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r2.json()['code'] == '103001', "创建BRL-PIX—CPF法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建BRL-PIX—CPF法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_007')
    @allure.description('确认&创建BRL-Ted法币提现交易-(提现金额小于最小金额or大于最大金额)')
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
            with allure.step("确认BRL-Ted法币提现交易(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                        assert r.json()['code'] == '103001', "确认BRL-Ted法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(
                            r.json()['code'])
                    else:
                        assert r.json()['code'] == '103002', "确认BRL-Ted法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(
                            r.json()['code'])
            with allure.step("创建BRL-Ted法币提现交易-失败(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                        assert r2.json()['code'] == '103001', "创建BRL-Ted法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(
                            r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建BRL-Ted法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(
                            r2.text)

    @allure.title('test_payout_cash_abnormal_008')
    @allure.description('确认&创建BRL提现提现交易，BRL-PIX—CPF(输入错误CPF)')
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
                mfaVerificationCode = get_mfa_code()
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
    @allure.description('确认&创建BRL提现提现交易，BRL-Ted(输入错误CPF)')
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
                mfaVerificationCode = get_mfa_code()
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
    @allure.description('确认&创建BRL-PIX_CPF提现交易-(输入错误account name)')
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
                mfaVerificationCode = get_mfa_code()
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
    @allure.description('确认&创建BRL-Ted提现交易-(输入错误account name)')
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
                mfaVerificationCode = get_mfa_code()
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
    @allure.description('确认&创建EUR法币提现交易-(提现金额小于最小金额or大于最大金额)')
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
                "iban": "BG12345678901234567890",
                "bic": "ZXCVBG12"
            }
            with allure.step("确认EUR法币提现交易(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                        assert r.json()['code'] == '103001', "确认EUR法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(
                            r.text)
                    else:
                        assert r.json()['code'] == '103002', "确认EUR法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(
                            r.text)
            with allure.step("创建EUR法币提现交易-失败(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                        assert r2.json()['code'] == '103001', "创建EUR法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建EUR法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_013')
    @allure.description('确认&创建EUR法币提现交易-错误account name')
    def test_payout_cash_abnormal_013(self):
        with allure.step("法币提现交易-错误account name"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "EUR",
                "amount": "25",
                "payment_method": "SEPA",
                "account_name": "Richard External AQ",
                "iban": "BG12345678901234567890",
                "bic": "ZXCVBG12"
            }
            with allure.step("确认EUR法币提现交易-错误account name"):
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
                        "确认EUR法币提现交易-错误account name返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建EUR法币提现交易-错误account name"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    if r2.status_code == 504 and r.json()['message'] == 'context deadline exceeded':
                        pytest.skip(msg='后端接口不稳定导致504')
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103015',\
                        "创建EUR法币提现交易-错误account name返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_014')
    @allure.description('确认&创建EUR法币提现交易-错误payment method')
    def test_payout_cash_abnormal_014(self):
        with allure.step("法币提现交易-错误payment method"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "EUR",
                "amount": "25",
                "payment_method": "Faster Payments",
                "account_name": "Richard External QA",
                "iban": "BG12345678901234567890",
                "bic": "ZXCVBG12"
            }
            with allure.step("确认EUR法币提现交易-错误payment method"):
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
                    assert r.json()['code'] == '103022',\
                        "确认EUR法币提现交易-错误payment method返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建EUR法币提现交易-错误payment method"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    if r2.status_code == 504 and r.json()['message'] == 'context deadline exceeded':
                        pytest.skip(msg='后端接口不稳定导致504')
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103022',\
                        "创建EUR法币提现交易-错误payment method返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_015')
    @allure.description('确认&创建EUR法币提现交易-iban和bic不匹配')
    def test_payout_cash_abnormal_015(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
        with allure.step("法币提现交易-iban和bic不匹配"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            headers['X-Mfa-Otp'] = get_mfa_code()
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "EUR",
                "amount": "25.61",
                "payment_method": "SEPA",
                "account_name": account_name[0],
                "iban": "BG12345678901234567890",
                "bic": "ZXCVGB12"
            }
            with allure.step("确认EUR法币提现交易-iban和bic不匹配"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103037', "确认EUR法币提现交易-iban和bic不匹配错误，返回值是{}".format(r.text)
            with allure.step("创建EUR法币提现交易-iban和bic不匹配"):
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    if r2.status_code == 504 and r.json()['message'] == 'context deadline exceeded':
                        pytest.skip(msg='后端接口不稳定导致504')
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103037', \
                        "创建EUR法币提现交易-iban和bic不匹配，返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_016')
    @allure.description('确认&创建EUR法币提现交易-使用非SEPA地区iban')
    def test_payout_cash_abnormal_016(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
        with allure.step("法币提现交易-使用非SEPA地区iban"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            headers['X-Mfa-Otp'] = get_mfa_code()
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "EUR",
                "amount": "25.61",
                "payment_method": "SEPA",
                "account_name": account_name[0],
                "iban": "BB09967206444557",
                "bic": "TRWIBBB1XXX"
            }
            with allure.step("确认EUR法币提现交易-使用非SEPA地区iban"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103036', "确认EUR法币提现交易-使用非SEPA地区iban，返回值是{}".format(r.text)
            with allure.step("创建EUR法币提现交易-使用非SEPA地区iban"):
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103036',\
                        "创建EUR法币提现交易-使用非SEPA地区iban，返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_017')
    @allure.description('确认&创建EUR法币提现，用户名字带有中文字符提现失败')
    def test_payout_cash_abnormal_017(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
            logger.info('提款名字是{}'.format(account_name))
        with allure.step("法币提现交易-用户名字带有中文字符提现失败错误"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            headers['X-Mfa-Otp'] = get_mfa_code()
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "EUR",
                "amount": "25.61",
                "payment_method": "SEPA",
                "account_name": account_name[2],
                "iban": "BG12345678901234567890",
                "bic": "ZXCVBG12"
            }
            with allure.step("确认EUR法币提现交易-用户名字带有中文字符提现失败错误"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103015', "确认EUR法币提现交易-用户名字带有中文字符提现失败错误，返回值是{}".format(r.text)
            with allure.step("创建EUR法币提现交易-用户名字带有中文字符提现失败错误"):
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103015', \
                        "创建EUR法币提现交易-用户名字带有中文字符提现失败错误，返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_018')
    @allure.description('确认&创建GBP法币提现交易-(提现金额小于最小金额or大于最大金额)')
    def test_payout_cash_abnormal_018(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step('获取法币最小和最大提现金额'):
            params = {
                'code': 'GBP'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params,
                                headers=headers)
            amount_min = r.json()['payment_methods'][r.json()['supported_payment_methods']]['min']
            amount_max = r.json()['payment_methods'][r.json()['supported_payment_methods']]['max']
            amount_list = [str(int(amount_min)-1), str(int(amount_max)+1)]
        for i in amount_list:
            data = {
                "code": "GBP",
                "amount": i,
                "payment_method": "Faster Payments",
                "account_name": "Richard External QA",
                "account_number": "00003162",
                "sort_code": "040541"
            }
            with allure.step("确认GBP法币提现交易(提现金额小于最小金额or大于最大金额)"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r.json()['code'] == '103001', "确认GBP法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(
                            r.text)
                    else:
                        assert r.json()['code'] == '103002', "确认GBP法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(
                            r.text)
            with allure.step("创建GBP法币提现交易-失败(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                    if i == amount_list[0]:
                        assert r2.json()['code'] == '103001', "创建GBP法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建GBP法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_019')
    @allure.description('确认&创建GBP法币提现交易-错误account name')
    def test_payout_cash_abnormal_019(self):
        with allure.step("法币提现交易-错误account name"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "GBP",
                "amount": '25',
                "payment_method": "Faster Payments",
                "account_name": "Richard External AQ",
                "account_number": "00003162",
                "sort_code": "040541"
            }
            with allure.step("确认GBP法币提现交易-错误account name"):
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
                        "确认GBP法币提现交易-错误account name返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建GBP法币提现交易-错误account name"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                        "创建GBP法币提现交易-错误account name返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_020')
    @allure.description('确认&创建GBP法币提现交易-错误account_number')
    def test_payout_cash_abnormal_020(self):
        with allure.step("法币提现交易-错误account_number"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
            data = {
                "code": "GBP",
                "amount": '25',
                "payment_method": "Faster Payments",
                "account_name": "Richard External QA",
                "account_number": "3162",
                "sort_code": "040541"
            }
            with allure.step("确认GBP法币提现交易-错误account_number"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103024', "确认GBP法币提现交易-错误account_number返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建GBP法币提现交易-错误account_number"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103024', "创建GBP法币提现交易-错误account_number返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_021')
    @allure.description('确认&创建GBP法币提现交易-错误sort_code')
    def test_payout_cash_abnormal_021(self):
        with allure.step("法币提现交易-错误sort_code"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "GBP",
                "amount": '25',
                "payment_method": "Faster Payments",
                "account_name": "Richard External QA",
                "account_number": "00003162",
                "sort_code": "0405"
            }
            with allure.step("确认GBP法币提现交易-错误sort_code"):
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
                    assert r.json()['code'] == '103026', \
                        "确认GBP法币提现交易-错误sort_code返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建GBP法币提现交易-错误sort_code"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                headers['X-Mfa-Otp'] = get_mfa_code()
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103026', \
                        "创建GBP法币提现交易-错误sort_code返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_022')
    @allure.description('确认&创建GBP法币提现，用户名字带有中文字符提现失败')
    def test_payout_cash_abnormal_022(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'GBP'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
            logger.info('提款名字是{}'.format(account_name))
        with allure.step("法币提现交易-用户名字带有中文字符提现失败错误"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            headers['X-Mfa-Otp'] = get_mfa_code()
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "GBP",
                "amount": "26.81",
                "payment_method": "Faster Payments",
                "account_name": account_name[2],
                "account_number": "00003162",
                "sort_code": "040541"
            }
            with allure.step("确认GBP法币提现交易-用户名字带有中文字符提现失败错误"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103015', "确认GBP法币提现交易-用户名字带有中文字符提现失败错误，返回值是{}".format(r.text)
            with allure.step("创建EUR法币提现交易-用户名字带有中文字符提现失败错误"):
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    if r.status_code == 504 and r.json()['message'] == 'context deadline exceeded':
                        pytest.skip(msg='后端接口不稳定导致504')
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103015', \
                        "创建GBP法币提现交易-用户名字带有中文字符提现失败错误，返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_023')
    @allure.description('确认&创建CHF法币提现交易-(提现金额小于最小金额or大于最大金额)')
    def test_payout_cash_abnormal_023(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step('获取法币最小和最大提现金额'):
            params = {
                'code': 'CHF'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params,
                                headers=headers)
            account_name = r.json()['name_list']
            amount_min = r.json()['payment_methods']['SIC']['min']
            amount_max = r.json()['payment_methods']['SIC']['max']
            amount_list = [str(int(amount_min)-1), str(int(amount_max)+1)]
        for i in amount_list:
            data = {
                "code": "CHF",
                "amount": i,
                "payment_method": "SIC",
                "account_name": account_name[0],
                "iban": "AT234567891827364532",
                "bic": "bkauatwwxxx"
            }
            with allure.step("确认CHF法币提现交易(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                        assert r.json()['code'] == '103001', "确认CHF法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(
                            r.text)
                    else:
                        assert r.json()['code'] == '103002', "确认CHF法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(
                            r.text)
            with allure.step("创建CHF法币提现交易-失败(提现金额小于最小金额or大于最大金额)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("校验状态码"):
                    if r2.status_code == 504 and r.json()['message'] == 'context deadline exceeded':
                        pytest.skip(msg='后端接口不稳定导致504')
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验返回值"):
                    if i == amount_list[0]:
                        assert r2.json()['code'] == '103001', "创建CHF法币提现交易-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(r2.text)
                    else:
                        assert r2.json()['code'] == '103002', "创建CHF法币提现交易-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_024')
    @allure.description('确认&创建CHF法币提现交易-错误account name')
    def test_payout_cash_abnormal_024(self):
        with allure.step("法币提现交易-错误account name"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "CHF",
                "amount": "25",
                "payment_method": "SIC",
                "account_name": 'Richard External AQ',
                "iban": "AT234567891827364532",
                "bic": "bkauatwwxxx"
            }
            with allure.step("确认CHF法币提现交易-错误account name"):
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
                        "确认CHF法币提现交易-错误account name返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建EUR法币提现交易-错误account name"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    if r2.status_code == 504 and r.json()['message'] == 'context deadline exceeded':
                        pytest.skip(msg='后端接口不稳定导致504')
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103015',\
                        "创建CHF法币提现交易-错误account name返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_025')
    @allure.description('确认&创建CHF法币提现交易-错误payment method')
    def test_payout_cash_abnormal_025(self):
        with allure.step("法币提现交易-错误payment method"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "CHF",
                "amount": "25",
                "payment_method": "Faster Payments",
                "account_name": "Richard External QA",
                "iban": "BG12345678901234567890",
                "bic": "ZXCVBG12"
            }
            with allure.step("确认CHF法币提现交易-错误payment method"):
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
                    assert r.json()['code'] == '103022',\
                        "确认CHF法币提现交易-错误payment method返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建CHF法币提现交易-错误payment method"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    if r2.status_code == 504 and r.json()['message'] == 'context deadline exceeded':
                        pytest.skip(msg='后端接口不稳定导致504')
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103022',\
                        "创建CHF法币提现交易-错误payment method返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_026')
    @allure.description('确认&创建CHF法币提现交易-CHF的iban前两位非sepa地区')
    def test_payout_cash_abnormal_026(self):
        with allure.step("法币提现交易-CHF的iban没有校验规则"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "CHF",
                "amount": "25",
                "payment_method": "SIC",
                "account_name": "Richard External QA",
                "iban": "BB12345678901234567890",
                "bic": "ZXCVBB12"
            }
            with allure.step("确认CHF法币提现交易-CHF的iban前两位非sepa地区"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == '103055',\
                        "确认CHF法币提现交易-CHF的iban前两位非sepa地区，接口返回值是{}".format(r.text)
            with allure.step("创建CHF法币提现交易-CHF的iban没有校验规则"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('trace id是{}'.format(str(r2.headers['Traceparent'])))
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert r2.json()['code'] == '103055',\
                        "创建CHF法币提现交易-CHF的iban前两位非sepa地区，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_027')
    @allure.description('确认&创建CHF法币提现交易-使用account number(bic格式错误)')
    def test_payout_cash_abnormal_027(self):
        with allure.step("法币提现交易-错误bic"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
            data = {
                "code": "CHF",
                "amount": "25",
                "payment_method": "SIC",
                "account_name": "Richard External QA",
                "iban": "12345678",
                "bic": "ZXX"
            }
            with allure.step("确认CHF法币提现交易-使用account number(bic格式错误)"):
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
                    assert r.json() == {},\
                        "确认CHF法币提现交易-使用account number(bic格式错误)返回值错误，接口返回值是{}".format(r.text)
            with allure.step("创建CHF法币提现交易-使用account number(bic格式错误)"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                    assert r2.json() == {},\
                        "创建CHF法币提现交易-使用account number(bic格式错误)返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_028')
    @allure.description('确认&创建CHF法币提现交易-使用无效iban(非iban也非account number)')
    def test_payout_cash_abnormal_027(self):
        with allure.step("法币提现交易-使用无效iban"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "CHF",
                "amount": "25",
                "payment_method": "SIC",
                "account_name": "Richard External QA",
                "iban": "BG123",
                "bic": "123VBG12"
            }
            with allure.step("确认CHF法币提现交易-使用无效iban"):
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
                    assert r.json()['code'] == '103055', \
                        "确认CHF法币提现交易-使用无效iban，接口返回值是{}".format(r.text)
            with allure.step("创建CHF法币提现交易-使用无效iban"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
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
                    assert r2.json()['code'] == '103055', \
                        "创建CHF法币提现交易-使用无效iban返回值错误，接口返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_abnormal_029')
    @allure.description('开启法币提现画面，不传code')
    def test_payout_cash_abnormal_029(self):
        with allure.step("开启法币提现画面，不传code，不传code"):
            data = {
                'code': '',
                'payment_method': ''
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json()['code'] == '100000', "开启法币提现画面，不传code，不传code错误，返回值是{}".format(r.text)
