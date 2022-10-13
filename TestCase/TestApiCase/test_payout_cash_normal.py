import pytest_assume.plugin

from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout cash normal相关 testcases")
class TestPayoutCashNormalApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_cash_normal_001')
    @allure.description('计算法币提现交易费率')
    def test_payout_cash_normal_001(self):
        with allure.step("获取法币列表"):
            for i in get_json()['cash_list']:
                with allure.step("计算法币提现交易费率"):
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
                    with allure.step("状态码和返回值"):
                        logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
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
                    elif i == 'USD':
                        assert r.json()['fee']['amount'] == '40', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)

    @allure.title('test_payout_cash_normal_002')
    @allure.description('获得法币提现币种')
    def test_payout_cash_normal_002(self):
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

    @allure.title('test_payout_cash_normal_003')
    @allure.description('开启法币提现画面')
    def test_payout_cash_normal_003(self):
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
                            assert r.json()[
                                       'supported_payment_methods'] == 'Faster Payments', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['payment_methods'][r.json()['supported_payment_methods']] == {'min': '20',
                                                                                                          'max': '40000',
                                                                                                          'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'EUR':
                            assert r.json()['supported_payment_methods'] == 'SEPA', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['payment_methods'][r.json()['supported_payment_methods']] == {
                                'max': '50000', 'min': '25', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'CHF':
                            assert r.json()[
                                       'supported_payment_methods'] == 'SIC or SWIFT', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['payment_methods']['SIC'] == {'max': '50000', 'min': '25',
                                                                          'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'BRL':
                            assert r.json()[
                                       'supported_payment_methods'] == 'PIX or Bank Transfer', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['payment_methods']['Bank Transfer'] == {'min': '130', 'max': '300000',
                                                                                    'order': 1}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['payment_methods']['PIX'] == {'min': '130', 'max': '300000',
                                                                          'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'VND':
                            assert r.json()[
                                       'supported_payment_methods'] == 'Bank Transfer', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            # vnd提现最小限额是600000，但是为了方便测试，测试环境配的是20000
                            assert r.json()['payment_methods']['Bank Transfer'] == {'min': '600000', 'max': '300000000',
                                                                                    'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['fee_rule']['percentage_charge_rule'][
                                       'percentage'] == '2', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())

    @allure.title('test_payout_cash_normal_004')
    @allure.description('确认&创建Payme VND法币提现交易')
    @pytest.mark.skip(reason='提现现在未开放vnd，先不管')
    def test_payout_cash_normal_004(self):
        with allure.step("VND法币提现"):
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
            with allure.step("确认VND法币提现交易"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认Payme VND法币提现交易错误，返回值是{}".format(r.text)
            with allure.step("创建VND法币提现交易"):
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
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert 'txn_id' in r2.text, "创建Payme VND法币提现交易失败，返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_normal_005')
    @allure.description('确认&创建BRL法币提现交易，BRL-PIX—CPF，cpf状态为5')
    def test_payout_cash_normal_005(self):
        with allure.step("创建BRL法币提现，BRL-PIX—CPF提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "BRL",
                "amount": "130",
                "payment_method": "PIX",
                "pix_key_type": 1,
                "cpf": "718.638.715-27",
                "account_name": "Richard External QA"
            }
            with allure.step("确认BRL法币提现，BRL-PIX—CPF"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认BRL法币提现交易错误，返回值是{}".format(r.text)
            with allure.step("创建BRL法币提现，BRL-PIX—CPF"):
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
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert 'txn_id' in r2.text, "创建BRL提现提现交易，BRL-PIX—CPF失败，返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_normal_006')
    @allure.description('确认&创建BRL法币提现交易，BRL-TED，cpf状态为5')
    def test_payout_cash_normal_006(self):
        with allure.step("创建BRL法币提现，BRL-TED提现交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            data = {
                "code": "BRL",
                "amount": "130",
                "payment_method": "Bank Transfer",
                "cpf": "718.638.715-27",
                "bank_name": "Banco BMG S.A.",
                "bank_code": "318",
                "branch_code": "0123",
                "account_type": 2,
                "account_name": "Richard External QA",
                "account_number": "1234567890"
            }
            with allure.step("确认BRL法币提现，BRL-TED"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                    headers=headers)
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认BRL法币提现交易错误，返回值是{}".format(r.text)
            with allure.step("创建BRL法币提现，BRL-TED"):
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('trace id是{}'.format(str(r2.headers['Traceparent'])))
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    if r2.status_code == 504 and r2.json()['message'] == 'context deadline exceeded':
                        pytest.skip(msg='后端接口不稳定导致504')
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert 'txn_id' in r2.text, "创建BRL提现提现交易，BRL-TED失败，返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_normal_007')
    @allure.description('webhook模拟brl提现')
    @pytest.mark.skip(reason='webhook模拟brl提现，transaction id必须唯一，不唯一就会报错, 现在不可用')
    def test_payout_cash_normal_007(self):
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

    @allure.title('test_payout_cash_normal_008')
    @allure.description('BRL支持银行列表')
    def test_payout_cash_normal_008(self):
        with allure.step("BRL支持银行列表"):
            r = session.request('GET', url='{}/pay/banks/{}'.format(env_url, 'BRL'), headers=headers)
        with allure.step("校验状态码"):
            if r.status_code == 504 and r.json()['message'] == 'context deadline exceeded':
                pytest.skip(msg='后端接口不稳定导致504')
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['banks'] is not None, "BRL支持银行列表错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_normal_009')
    @allure.description('确认&创建EUR法币提现交易')
    def test_payout_cash_normal_009(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
        with allure.step("法币EUR提现"):
            data = {
                "code": "EUR",
                "amount": "25.61",
                "payment_method": "SEPA",
                "account_name": account_name[0],
                "iban": "BE09967206444557",
                "bic": "TRWIBEB1XXX"
            }
            with allure.step("确认EUR法币提现交易"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data), headers=headers)
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认EUR法币提现交易错误，返回值是{}".format(r.text)
            with allure.step("创建EUR法币提现交易"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('trace id是{}'.format(str(r2.headers['Traceparent'])))
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert 'txn_id' in r2.text, "创建EUR法币提现交易失败，返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_normal_010')
    @allure.description('确认&创建GBP法币提现交易')
    def test_payout_cash_normal_010(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'GBP'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            account_name = r.json()['name_list']
        with allure.step("法币GBP提现"):
            data = {
                "code": "GBP",
                "amount": "25",
                "payment_method": "Faster Payments",
                "account_name": account_name[0],
                "account_number": "00003162",
                "sort_code": "040541"
            }
            with allure.step("确认GBP法币提现交易"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data), headers=headers)
                logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认GBP法币提现交易错误，返回值是{}".format(r.text)
            with allure.step("创建GBP法币提现交易"):
                code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
                mfaVerificationCode = get_mfa_code()
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
                r2 = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('trace id是{}'.format(str(r2.headers['Traceparent'])))
                    logger.info('状态码是{}'.format(str(r2.status_code)))
                    logger.info('返回值是{}'.format(str(r2.text)))
                with allure.step("校验状态码"):
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert 'txn_id' in r2.text, "创建GBP法币提现交易失败，返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_normal_011')
    @allure.description('确认&创建CHF法币提现交易-iban')
    # 说明：Cabinet payout order detail中的Payment Method是SWIFT
    def test_payout_cash_normal_011(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'CHF'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
        with allure.step("法币CHF提现"):
            data = {
                "code": "CHF",
                "amount": "35.51",
                "payment_method": "SIC",
                "account_name": account_name[0],
                "iban": "AT234567891827364532",
                "bic": "bkauatwwxxx"
            }
            with allure.step("确认CHF法币提现交易"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认CHF法币提现交易错误，返回值是{}".format(r.text)
            with allure.step("创建CHF法币提现交易"):
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
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert 'txn_id' in r2.text, "创建CHF法币提现交易失败，返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_normal_012')
    @allure.description('确认&创建CHF法币提现交易-account number（bic第五第六位非ch）')
    # 说明：Cabinet payout order detail中的Payment Method是SWIFT
    def test_payout_cash_normal_012(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'CHF'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
        with allure.step("法币GBP提现"):
            data = {
                "code": "CHF",
                "amount": "35.51",
                "payment_method": "SIC",
                "account_name": account_name[0],
                "iban": "12345678",
                "bic": "bkauatwwxxx",
                "partner_id": '800b482d-0a88-480a-aae7-741f77a572f4',
                'user_ext_ref': '988518746672869376'
            }
            with allure.step("确认CHF法币提现交易"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认CHF法币提现交易错误，返回值是{}".format(r.text)
            with allure.step("创建CHF法币提现交易"):
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
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert 'txn_id' in r2.text, "创建CHF法币提现交易失败，返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_normal_013')
    @allure.description('确认&创建CHF法币提现交易-account number（bic第五第六位为ch）')
    # 说明：Cabinet payout order detail中的Payment Method是LOCAL
    def test_payout_cash_normal_013(self):
        with allure.step("从开启法币提现画面接口获取name list"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'CHF'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
        with allure.step("法币GBP提现"):
            data = {
                "code": "CHF",
                "amount": "35.51",
                "payment_method": "SIC",
                "account_name": account_name[0],
                "iban": "12345678",
                "bic": "bkauchwwxxx"
            }
            with allure.step("确认CHF法币提现交易"):
                r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url),
                                    data=json.dumps(data),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认CHF法币提现交易错误，返回值是{}".format(r.text)
            with allure.step("创建CHF法币提现交易"):
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
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                with allure.step("校验返回值"):
                    assert 'txn_id' in r2.text, "创建CHF法币提现交易失败，返回值是{}".format(r2.text)

    @allure.title('test_payout_cash_normal_014')
    @allure.description('法币提现获得信息，白名单排序(有效的在前面，无效的在后面)')
    def test_payout_cash_normal_014(self):
        with allure.step("法币提现获得信息"):
            data = {
                'code': 'EUR',
                'payment_method': 'SEPA'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        a = 1
        print(r.json()['account_names'])
        with allure.step("确保1在前，0在后"):
            # 循环确保无效name后不会有有效的name
            for i in r.json()['account_names']:
                if a == 1:
                    if i['status'] == 0:
                        a = 0
                elif a == 0:
                    assert i['status'] == 0, '白名单排序问题，没1在前0在后。'

    @allure.title('test_payout_cash_normal_015')
    @allure.description('获取用户提现白名单')
    def test_payout_cash_normal_015(self):
        # headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
        #     account=get_json()['email']['payout_email'])
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='alice1012001@cabital.com', password='Zcdsw123')
        with allure.step("获取用户提现白名单"):
            r = session.request('GET', url='{}/pay/user-whitelist'.format(env_url), headers=headers)
            print(r.json())
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['name_list'] is not None, "获取用户提现白名单错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_normal_016')
    @allure.description('开启USD提现画面')
    def test_payout_cash_normal_016(self):
        params = {
            'code': 'USD',
            'payment_method': 'SWIFT'
        }
        with allure.step("开启USD提现画面"):
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['bound_bank_account_max_cnt'] == 3, "开启USD提现画面错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_normal_017')
    @allure.description('确认USD法币提现交易')
    def test_payout_cash_normal_017(self):
        data = {
            "code": "USD",
            "amount": "200",
            "payment_method": "SWIFT",
            "account_name": "kimi w",
            "bank_account_id": "b2e00af4-e1c2-4c46-8171-c9bf30e7b588"
        }
        with allure.step("确认USD法币提现交易"):
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), headers=headers, data=json.dumps(data))
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "确认USD法币提现交易错误，返回值是{}".format(r.text)

    @allure.title('test_payout_cash_normal_017')
    @allure.description('创建USD法币提现交易')
    def test_payout_cash_normal_017(self):
        
        data = {
            "code": "USD",
            "amount": "200",
            "payment_method": "SWIFT",
            "account_name": "kimi w",
            "bank_account_id": "b2e00af4-e1c2-4c46-8171-c9bf30e7b588"
        }
        with allure.step("确认USD法币提现交易"):
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), headers=headers, data=json.dumps(data))
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "确认USD法币提现交易错误，返回值是{}".format(r.text)