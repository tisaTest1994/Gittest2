from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout 相关 testcases")
class TestPayoutApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_001')
    @allure.description('没有Kyc用户添加常用收款地址失败')
    def test_payout_001(self):
        account = generate_email()
        password = get_json()['email']['password']
        with allure.step("提前先注册好"):
            ApiFunction.sign_up(account, password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account, password=password)
        with allure.step("没有Kyc用户添加常用收款地址失败"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "USDT",
                "method": "ERC20",
                "address": "0xf4af4d6dfcba0844d78bf091070d33c0e378cc88"
            }
            r = session.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                                headers=headers)
        ApiFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'ACC_FORBIDDEN', "没有Kyc用户添加常用收款地址失败错误，返回值是{}".format(r.text)

    @allure.title('test_payout_002 获取存储的常用收款地址list')
    @allure.description('获取存储的常用收款地址list')
    def test_payout_002(self):
        with allure.step("获取存储的常用收款地址list"):
            r = session.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['payeeList'] is not None, "获取存储的常用收款地址list错误，返回值是{}".format(r.text)

    @allure.title('test_payout_003')
    @allure.description('获取某个常用收款地址')
    def test_payout_003(self):
        with allure.step("获取收款地址list"):
            r = session.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
        with allure.step("获取单个收款地址id"):
            id = r.json()['payeeList'][0]['id']
        with allure.step("获取某个常用收款地址"):
            r = session.request('GET', url='{}/account/myPayee/{}'.format(env_url, id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['payeeList'] is not None, "获取某个常用收款地址错误，返回值是{}".format(r.text)

    @allure.title('test_payout_004')
    @allure.description('使用不存在id获取常用收款地址')
    def test_payout_004(self):
        with allure.step("使用不存在id获取常用收款地址"):
            r = session.request('GET', url='{}/account/myPayee/{}'.format(env_url, '1111300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == '0010015', "使用不存在id获取常用收款地址错误，返回值是{}".format(r.text)

    @allure.title('test_payout_005')
    @allure.description('删除不存在的收款地址')
    def test_payout_005(self):
        with allure.step("凭借空id号删除地址"):
            r = session.request('DELETE', url='{}/account/myPayee/{}'.format(env_url, '123131300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == '0010015', "删除收款地址错误，返回值是{}".format(r.text)

    @allure.title('test_payout_006')
    @allure.description('获取提现费率和提现限制')
    def test_payout_006(self):
        with allure.step("获取提现费率和提现限制"):
            data = {
                "amount": "0.11",
                "code": "ETH",
                "address": "0x623089BFb1dc2d3023Ba4bd0f42F61d66826994eu",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/verification'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == 'ETH', "获取提现费率和提现限制错误，返回值是{}".format(r.text)

    @allure.title('test_payout_008')
    @allure.description('查询提现详情')
    def test_payout_008(self):
        with allure.step("获得交易transaction_id"):
            transaction_id = ApiFunction.get_payout_transaction_id()
            logger.info('transaction_id是{}'.format(transaction_id))
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token()
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url, transaction_id),
                                headers=headers)
            ApiFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'status' in r.text, "查询提现详情错误，返回值是{}".format(r.text)

    @allure.title('test_payout_009')
    @allure.description('使用错误id查询提现详情')
    def test_payout_009(self):
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url,
                                                                                    '4684225231310-3fa0-4bd1-9d46-4467dfa9ce52'),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'no rows in result set' in r.text, "使用错误id查询提现详情错误，返回值是{}".format(r.text)

    @allure.title('test_payout_010')
    @allure.description('法币提现获得信息，白名单排序')
    def test_payout_010(self):
        with allure.step("法币提现获得信息"):
            data = {
                'code': 'EUR',
                'payment_method': 'SEPA'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        a = 1
        with allure.step("确保1在前，0在后"):
            for i in r.json()['account_names']:
                if a == 1:
                    if i['status'] == 0:
                        a = 0
                elif a == 0:
                    assert i['status'] == 0, '白名单排序问题，没1在前0在后。'

    @allure.title('test_payout_011 预校验法币提现')
    @allure.description('预校验法币提现')
    def test_payout_011(self):
        with allure.step("法币提现获得信息"):
            data = {
                "code": "EUR",
                "amount": "5000"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/verification'.format(env_url), data=json.dumps(data),
                                headers=headers)
            ApiFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['fee']['code'] == 'EUR', "预校验法币提现错误，返回值是{}".format(r.text)
            assert r.json()['fee']['amount'] == '2.5', "预校验法币提现错误，返回值是{}".format(r.text)

    @allure.title('test_payout_012 获得法币提现币种')
    @allure.description('获得法币提现币种')
    def test_payout_012(self):
        with allure.step("提现币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, 'fiat'), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'fiat' in r.text, "获得法币提现币种错误，返回值是{}".format(r.text)

    @allure.title('test_payout_013')
    @allure.description('获得数字货币提现币种')
    def test_payout_013(self):
        with allure.step("提现币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, 'crypto'), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'crypto' in r.text, "获得数字货币提现币种错误，返回值是{}".format(r.text)

    @allure.title('test_payout_014')
    @allure.description('获得全部提现币种')
    def test_payout_014(self):
        with allure.step("提现币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, ''), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'fiat' in r.text, "获得全部提现币种错误，返回值是{}".format(r.text)
                assert 'crypto' in r.text, "获得全部提现币种错误，返回值是{}".format(r.text)

    @allure.title('test_payout_015')
    @allure.description('开启法币提现画面')
    def test_payout_015(self):
        with allure.step("开启法币提现画面"):
            params = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'SEPA' in r.text, "开启法币提现画面错误，返回值是{}".format(r.text)

    @allure.title('test_payout_016')
    @allure.description('BCB EUR法币提现')
    def test_payout_016(self):
        with allure.step("开启法币提现画面"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
        with allure.step("法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "EUR",
                "amount": "2.61",
                "payment_method": "SEPA",
                "account_name": account_name[0],
                "iban": "BE09967206444557",
                "bic": "TRWIBEB1XXX"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'txn_id' in r.text, "开启法币提现画面错误，返回值是{}".format(r.text)

    @allure.title('test_payout_017')
    @allure.description('GBP法币提现、')
    def test_payout_017(self):
        with allure.step("开启GBP法币提现画面"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'GBP'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
        with allure.step("GBP法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "GBP",
                "amount": "2.61",
                "payment_method": "Faster Payments",
                "account_name": account_name[0],
                "account_number": "00003162",
                "sort_code": "040541"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            ApiFunction.add_headers()
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'txn_id' in r.text, "开启法币提现画面错误，返回值是{}".format(r.text)

    @allure.title('test_payout_018')
    @allure.description('确认法币提现交易')
    def test_payout_018(self):
        with allure.step("确认法币提现交易"):
            data = {
                "code": "EUR",
                "amount": "2.51",
                "payment_method": "SEPA",
                "account_name": "yilei",
                "iban": "AT234567891827364532",
                "bic": "BKAUATWWXXX"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, "开启法币提现画面错误，返回值是{}".format(r.text)

    @allure.title('test_payout_019')
    @allure.description('法币提现获得信息，不传code')
    def test_payout_019(self):
        with allure.step("法币提现获得信息，不传code"):
            data = {
                'code': '',
                'payment_method': ''
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json()['code'] == '100000', "法币提现获得信息，不传code错误，返回值是{}".format(r.text)

    @allure.title('test_payout_020')
    @allure.description('法币提现英镑获得信息，白名单排序')
    def test_payout_020(self):
        with allure.step("法币提现英镑获得信息，白名单排序"):
            data = {
                'code': 'GBP',
                'payment_method': 'Faster Payments'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert "Faster Payments" in r.text, "法币提现英镑获得信息，白名单排序错误，返回值是{}".format(r.text)
        a = 1
        with allure.step("确保1在前，0在后"):
            for i in r.json()['account_names']:
                if a == 1:
                    if i['status'] == 0:
                        a = 0
                elif a == 0:
                    assert i['status'] == 0, '白名单排序问题，没1在前0在后。'

    @allure.title('test_payout_021 预校验英镑提现')
    @allure.description('预校验英镑提现')
    def test_payout_021(self):
        with allure.step("法币提现获得信息"):
            data = {
                "code": "GBP",
                "amount": "5000"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/verification'.format(env_url), data=json.dumps(data),
                                headers=headers)
            ApiFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['fee']['code'] == 'GBP', "预校验英镑提现错误，返回值是{}".format(r.text)
            assert r.json()['fee']['amount'] == '2.5', "预校验英镑提现错误，返回值是{}".format(r.text)

    @allure.title('test_payout_022')
    @allure.description('开启英镑法币提现画面')
    def test_payout_022(self):
        with allure.step("开启英镑法币提现画面"):
            params = {
                'code': 'GBP'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'Faster Payments' in r.text, "开启英镑法币提现画面错误，返回值是{}".format(r.text)

    @allure.title('test_payout_023 GBP法币用户名字带有中文字符提现失败')
    @allure.description('BCB EUR法币提现')
    def test_payout_023(self):
        with allure.step("开启GBP法币提现画面"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'GBP'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
            logger.info('提款名字是{}'.format(account_name))
        with allure.step("GBP法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "GBP",
                "amount": "2.81",
                "payment_method": "Faster Payments",
                "account_name": account_name[3],
                "account_number": "00003162",
                "sort_code": "040541"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            ApiFunction.add_headers()
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103015', "GBP法币用户名字带有中文字符提现失败错误，返回值是{}".format(r.text)

    @allure.title('test_payout_024 BCB GBP法币提现')
    @allure.description('BCB EUR法币提现')
    def test_payout_024(self):
        with allure.step("开启EUR法币提现画面"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                'code': 'GBP'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
            account_name = r.json()['name_list']
            logger.info('account_name是{}'.format(account_name))
        with allure.step("BCB GBP法币提现"):
            code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
            data = {
                "code": "GBP",
                "amount": "2.81",
                "payment_method": "Faster Payments",
                "account_name": account_name[0],
                "account_number": "00003162",
                "sort_code": "040541"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'txn_id' in r.text, "BCB GBP法币提现错误，返回值是{}".format(r.text)

    @allure.title('test_payout_025 BTC确认Crypto提现交易超过每日限额')
    @allure.description('BTC确认Crypto提现交易超过每日限额')
    def test_payout_025(self):
        with allure.step("BTC确认Crypto提现交易"):
            data = {
                "amount": "2",
                "code": "BTC",
                "address": "tb1q38mwu50xludgz4r52n2v0q6jwlysjgz4zkk3kl",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103031', "BTC确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)

    @allure.title('test_payout_026')
    @allure.description('ETH确认Crypto提现交易超过每日限额')
    def test_payout_026(self):
        with allure.step("ETH确认Crypto提现交易"):
            data = {
                "amount": "40.018",
                "code": "ETH",
                "address": "0xA7185FBEE96B605709D9659894066dF21cc87f05",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103031', "ETH确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)

    @allure.title('test_payout_027')
    @allure.description('USDT确认Crypto提现交易超过每日限额')
    def test_payout_027(self):
        with allure.step("USDT确认Crypto提现交易"):
            data = {
                "amount": "20000",
                "code": "USDT",
                "address": "0xA7185FBEE96B605709D9659894066dF21cc87f05",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/crypto/validate'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '103031', "USDT确认Crypto提现交易超过每日限额错误，返回值是{}".format(r.text)

    @allure.title('test_payout_028')
    @allure.description('MFA认证提现ETH成功')
    def test_payout_028(self):
        ApiFunction.get_payout_transaction_id(amount='0.01', address='0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C', code_type='ETH')

    @allure.title('test_payout_029')
    @allure.description('MFA认证提现BTC成功')
    def test_payout_029(self):
        ApiFunction.get_payout_transaction_id(amount='0.01', address='tb1q3fhjd9f0th907cuym9dtyzpy3zu9tn6205jhwm', code_type='BTC')

    @allure.title('test_payout_030')
    @allure.description('MFA认证提现USDT成功')
    def test_payout_030(self):
        ApiFunction.get_payout_transaction_id(amount='30.01', address='0x0f841561A9e5c95926b234FC5fA12cDcf9BEB378', code_type='USDT')
