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
                            assert r.json()['payment_methods']['Bank Transfer'] == {'min': '20000', 'max': '300000000',
                                                                                    'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['fee_rule']['percentage_charge_rule']['percentage'] == '2', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())

    @allure.title('test_payout_cash_004')
    @allure.description('确认BRL 提现')
    def test_payout_cash_004(self):
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
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['message'] == 'BRL withdraw currently is disabled to you.', "预校验BRL提现错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_005')
    @allure.description('创建Payme VND法币提现交易')
    def test_payout_cash_005(self):
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

    @allure.title('test_payout_cash_006')
    @allure.description('确认Payme VND法币提现交易')
    def test_payout_cash_006(self):
        with allure.step("确认法币提现交易"):
            headers['Accept-Language'] = 'zh-TW'
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

    @allure.title('test_payout_cash_007')
    @allure.description('确认Payme VND法币提现交易-错误account name')
    def test_payout_cash_007(self):
        with allure.step("确认法币提现交易"):
            headers['Accept-Language'] = 'en-US'
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
                assert r.json()['message'] == 'Invalid account name',\
                    "确认Payme VND法币提现交易-错误account name返回值错误，接口返回值是{}".format(r.text)

    @allure.title('test_payout_cash_008')
    @allure.description('确认Payme VND法币提现交易-错误Account number')
    def test_payout_cash_008(self):
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
                assert r.json()['message'] == 'Invalid account number', \
                    "确认Payme VND法币提现交易-错误account number返回值错误，接口返回值是{}".format(r.text)

    @allure.title('test_payout_cash_009')
    @allure.description('确认Payme VND法币提现交易-错误Swift code')
    def test_payout_cash_009(self):
        headers['Accept-Language'] = 'en-US'
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
                assert r.json()['message'] == 'Invalid bic (swift)', \
                    "确认Payme VND法币提现交易-错误Swift code返回值错误，接口返回值是{}".format(r.text)

    @allure.title('test_payout_cash_010')
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
                assert r.json()['message'] == 'Invalid beneficiary', \
                    "确认Payme VND法币提现交易-错误Payment method返回值错误，接口返回值是{}".format(r.text)
