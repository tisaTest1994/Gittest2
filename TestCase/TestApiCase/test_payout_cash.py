from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout cash 相关 testcases")
class TestPayoutCashApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_cash_001')
    @allure.description('法币获取提现费率和提现限制')
    def test_payout_cash_001(self):
        with allure.step("获取法币列表"):
            for i in get_json()['cash_list']:
                with allure.step("获取提现费率和提现限制"):
                    if i == 'VND':
                        data = {
                            "code": i,
                            "amount": "300000"
                        }
                    else:
                        data = {
                            "code": i,
                            "amount": "100"
                        }
                    r = session.request('POST', url='{}/pay/withdraw/fiat/verification'.format(env_url),
                                        data=json.dumps(data), headers=headers)
                    if i == 'GBP':
                        assert r.json()['fee']['amount'] == '2.5', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)
                    elif i == 'EUR':
                        assert r.json()['fee']['amount'] == '2.5', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)
                    elif i == 'BRL':
                        assert r.json()['fee']['amount'] == '3.6', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)
                    elif i == 'CHF':
                        assert r.json()['fee']['amount'] == '4.5', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)
                    elif i == 'VND':
                        assert r.json()['fee']['amount'] == '6000', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)

    @allure.title('test_payout_cash_002')
    @allure.description('获得法币提现币种')
    def test_payout_cash_002(self):
        with allure.step("提现币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, 'fiat'), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                cash_list = []
                for y in r.json()['fiat']:
                    if y['status'] == 1:
                        cash_list.append(y['name'])
                assert (set(cash_list) == set(get_json()['cash_list'])), '获得法币提现币种错误，接口返回币种是{}'.format(cash_list)

    @allure.title('test_payout_cash_003')
    @allure.description('开启法币提现画面')
    def test_payout_cash_003(self):
        with allure.step("获取法币列表"):
            for i in get_json()['cash_list']:
                with allure.step("开启法币提现画面"):
                    params = {
                        'code': i
                    }
                    r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params,
                                        headers=headers)
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        if i == 'GBP':
                            assert r.json()['supported_payment_methods'] == 'Faster Payments', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(i, r.json())
                            assert r.json()['payment_methods'][r.json()['supported_payment_methods']] == {'min': '20', 'max': '40000', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'EUR':
                            assert r.json()['supported_payment_methods'] == 'SEPA', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(i, r.json())
                            assert r.json()['payment_methods'][r.json()['supported_payment_methods']] == {'max': '50000', 'min': '25', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'CHF':
                            assert r.json()['supported_payment_methods'] == 'SIC or SWIFT', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(i, r.json())
                            assert r.json()['payment_methods']['SIC'] == {'max': '50000', 'min': '25', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'BRL':
                            assert r.json()['supported_payment_methods'] == 'PIX or Bank Transfer', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(i, r.json())
                            assert r.json()['payment_methods']['Bank Transfer'] == {'min': '20', 'max': '300000', 'order': 1}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['payment_methods']['PIX'] == {'min': '20', 'max': '300000', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'VND':
                            assert r.json()[
                                       'supported_payment_methods'] == 'Bank Transfer', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            # vnd提现最小限额是600000，但是为了方便测试，测试环境配的是20000
                            assert r.json()['payment_methods']['Bank Transfer'] == {'min': '600000', 'max': '300000000',
                                                                                    'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['fee_rule']['percentage_charge_rule']['percentage'] == '2', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())

    @allure.title('test_payout_cash_004')
    @allure.description('创建Payme VND法币提现交易')
    def test_payout_cash_004(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "NGUYEN VAN A",
                "account_number": "9704000000000018",
                "bic": "SBITVNVX"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'txn_id' in r.text, "创建Payme VND法币提现交易失败，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_005')
    @allure.description('确认Payme VND法币提现交易')
    def test_payout_cash_005(self):
        with allure.step("确认法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "Richard External QA",
                "account_number": "12345678",
                "bic": "ABCDCH12345"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, "确认Payme VND法币提现交易错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_006')
    @allure.description('确认Payme VND法币提现交易-错误account name')
    def test_payout_cash_006(self):
        with allure.step("确认法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "wrong name",
                "account_number": "12345678",
                "bic": "ABCDCH12345"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103015',\
                    "确认Payme VND法币提现交易-错误account name返回值错误，接口返回值是{}".format(r.text)

    @allure.title('test_payout_cash_007')
    @allure.description('确认Payme VND法币提现交易-错误Account number')
    def test_payout_cash_007(self):
        with allure.step("确认法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "Richard External QA",
                "account_number": "12345678  ",
                "bic": "ABCDCH12345"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103024', \
                    "确认Payme VND法币提现交易-错误account number返回值错误，接口返回值是{}".format(r.text)

    @allure.title('test_payout_cash_008')
    @allure.description('确认Payme VND法币提现交易-错误Swift code')
    def test_payout_cash_008(self):
        with allure.step("确认法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "Bank Transfer",
                "account_name": "Richard External QA",
                "account_number": "12345678",
                "bic": "ABCDCH1234"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103028', \
                    "确认Payme VND法币提现交易-错误Swift code返回值错误，接口返回值是{}".format(r.text)

    @allure.title('test_payout_cash_009')
    @allure.description('确认Payme VND法币提现交易-错误Payment method')
    def test_payout_cash_009(self):
        with allure.step("确认法币提现交易"):
            headers['Accept-Language'] = 'en-US'
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "VND",
                "amount": "600000",
                "payment_method": "SIC",
                "account_name": "Richard External QA",
                "account_number": "12345678",
                "bic": "ABCDCH1234"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103022', \
                    "确认Payme VND法币提现交易-错误Payment method返回值错误，接口返回值是{}".format(r.text)

    @allure.title('test_payout_cash_010')
    @allure.description('创建BRL提现提现交易，BRL-PIX—CPF，cpf状态为5，能够提现成功')
    def test_payout_cash_010(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "BRL",
                "amount": "20",
                "payment_method": "PIX",
                "pix_key_type": 1,
                "cpf": "718.638.715-27",
                "account_name": "Richard External QA"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'txn_id' in r.text, "创建BRL提现提现交易，提现-BRL-PIX—CPF失败，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_011')
    @allure.description('创建BRL提现提现交易，BRL-Ted cpf状态为5，能够提现成功')
    def test_payout_cash_011(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "BRL",
                "amount": "20",
                "payment_method": "Bank Transfer",
                "cpf": "718.638.715-27",
                "bank_name": "Banco BMG S.A.",
                "bank_code": "318",
                "branch_code": "0123",
                "account_type": 2,
                "account_name": "Richard External QA",
                "account_number": "1234567890"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'txn_id' in r.text, "创建BRL提现提现交易，提现-BRL-PIX—CPF失败，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_012')
    @allure.description('创建BRL提现提现交易，BRL-PIX—CPF，小于最小可提现金额')
    def test_payout_cash_012(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "BRL",
                "amount": "19",
                "payment_method": "PIX",
                "pix_key_type": 1,
                "cpf": "718.638.715-27",
                "account_name": "Richard External QA"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103001', "创建BRL提现提现交易，提现BRL-PIX—CPF提现最小金额错误，返回值是{}".format(r.json()['message'])

    @allure.title('test_payout_cash_013')
    @allure.description('创建BRL提现提现交易，BRL-PIX—CPF，大于最大可提现金额')
    def test_payout_cash_013(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "BRL",
                "amount": "300001",
                "payment_method": "PIX",
                "pix_key_type": 1,
                "cpf": "718.638.715-27",
                "account_name": "Richard External QA"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103002', "创建BRL提现提现交易，提现BRL-PIX—CPF提现最大金额错误，返回值是{}".format(r.json()['message'])

    @allure.title('test_payout_cash_014')
    @allure.description('创建BRL提现提现交易，BRL-Ted 小于最小可提现金额')
    def test_payout_cash_014(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "BRL",
                "amount": "19",
                "payment_method": "Bank Transfer",
                "cpf": "718.638.715-27",
                "bank_name": "Banco Santander (Brasil) S.A. (033)",
                "bank_code": "90240",
                "branch_code": "0123",
                "account_type": 2,
                "account_name": "Richard External QA",
                "account_number": "1234567890"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103001', "创建BRL提现提现交易，提现BRL-Ted提现最小金额错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_015')
    @allure.description('创建BRL提现提现交易，BRL-Ted 大于最大可提现金额')
    def test_payout_cash_015(self):
        with allure.step("创建法币提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "BRL",
                "amount": "300001",
                "payment_method": "Bank Transfer",
                "cpf": "718.638.715-27",
                "bank_name": "Banco Santander (Brasil) S.A. (033)",
                "bank_code": "90240",
                "branch_code": "0123",
                "account_type": 2,
                "account_name": "Richard External QA",
                "account_number": "1234567890"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103002', "创建BRL提现提现交易，提现BRL-Ted提现最小金额错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_016')
    @allure.description('确认BRL提现-不成功')
    def test_payout_cash_016(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['email']['payout_email'])
        with allure.step("法币提现获得信息"):
            data = {
                "code": "BRL",
                "amount": "21",
                "payment_method": "PIX",
                "pix_key_type": 2,
                "cpf": "976.111.142-99",
                "bank_name": "Banco Santander (Brasil) S.A. (033)",
                "bank_code": "90400888",
                "branch_code": "0123",
                "account_type": 1,
                "account_name": "Richard External QA",
                "account_number": "1234567890"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == '103041', "预校验BRL提现错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_017')
    @allure.description('webhook模拟brl提现')
    @pytest.mark.skip(reason='webhook模拟brl提现，transaction id必须唯一，不唯一就会报错')
    def test_payout_cash_17(self):
        cpf_info = [('yanting.huang+184@cabital.com', 5)]
        for i in cpf_info:
            cpf_account = i[0]
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=cpf_account)
            with allure.step("请求数据"):
                data = {
                    "PaymentGroupId": "a042ae9d-ca53-44e9-8342-ae46572d87f5",
                    "TaxIdCountry": "BRA",
                    "AccountId": "341",
                    "PaymentId": "f4c362ca-d1c5-4834-9d15-9ae2fb1401e5",
                    "Amount": 1009,
                    "AmountNet": 1009,
                    "ExternalId": "d9afd9a6-ac05-424c-8d19-b909f7f0028f",
                    "Currency": "BRL",
                    "Name": "Ting DP184",
                    "TaxId": "173.942.850-14",
                    "BankAccount": "123",
                    "BankBranch": "132",
                    "BankCode": "256",
                    "PaymentStatus": "CompletedWithError",
                    "ReasonsForPaymentRejection": "Invalid TaxId"
                }
            r = session.request('POST', url='https://webhook.latibac.com/mh/transfero/payment_status_changed',
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)