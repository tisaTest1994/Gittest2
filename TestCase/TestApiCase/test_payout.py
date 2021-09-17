import json

from Function.api_function import *
from Function.operate_sql import *


class TestPayoutApi:

    # 初始化class
    def setup_method(self):
        AccountFunction.add_headers()

    @allure.testcase('test_payout_001 没有Kyc用户添加常用收款地址失败')
    @pytest.mark.multiprocess
    def test_payout_001(self):
        account = generate_email()
        password = get_json()['email']['password']
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("没有Kyc用户添加常用收款地址失败"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "USDT",
                "method": "ERC20",
                "address": "0xf4af4d6dfcba0844d78bf091070d33c0e378cc88"
            }
            r = session.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                                headers=headers)
        AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_FORBIDDEN' in r.text, "没有Kyc用户添加常用收款地址失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_002 获取存储的常用收款地址list')
    @pytest.mark.multiprocess
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

    @allure.testcase('test_payout_003 获取某个常用收款地址')
    @pytest.mark.multiprocess
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

    @allure.testcase('test_payout_004 使用不存在id获取常用收款地址')
    @pytest.mark.multiprocess
    def test_payout_004(self):
        with allure.step("使用不存在id获取常用收款地址"):
            r = session.request('GET', url='{}/account/myPayee/{}'.format(env_url, '1111300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'This address is not exist, please refresh and retry.' in r.text, "使用不存在id获取常用收款地址错误，返回值是{}".format(
                r.text)

    @allure.testcase('test_payout_005 删除不存在的收款地址')
    @pytest.mark.multiprocess
    def test_payout_005(self):
        with allure.step("凭借空id号删除地址"):
            r = session.request('DELETE', url='{}/account/myPayee/{}'.format(env_url, '123131300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'This address is not exist, please refresh and retry.' in r.text, "删除收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_06 获取提现费率和提现限制')
    @pytest.mark.multiprocess
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
            assert '"code":"ETH"' in r.text, "获取提现费率和提现限制错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_007 MFA认证提现ETH成功')
    @pytest.mark.multiprocess
    def test_payout_007(self):
        transaction_id = AccountFunction.get_payout_transaction_id(amount='0.03123452345',
                                                                   address='0x38c838b19BEEa501Cf051b094Bc53f9E23ae1560')
        logger.info('transaction_id是{}'.format(transaction_id))
        with allure.step("p/l验证"):
            sleep(5)
            sql = "select * from transaction_history where transaction_id='{}';".format(transaction_id)
            logger.info(sql)
            sql_info = sqlFunction.connect_mysql(db='assetstat', sql=sql)
            assert sql_info[0] is not None, "payout的P/L错误，sql命令是{}".format(sql)
        with allure.step("wallet internal_balance验证"):
            sleep(5)
            sql = "select wallet_id from internal_balance where transaction_id='{}';".format(transaction_id)
            sql_info = sqlFunction.connect_mysql(db='wallet', sql=sql)
            for i in sql_info:
                assert i['wallet_id'] is not None, "payout的P/L错误，sql命令是{}".format(sql)

    @allure.testcase('test_payout_008 查询提现详情')
    @pytest.mark.multiprocess
    def test_payout_008(self):
        with allure.step("获得交易transaction_id"):
            transaction_id = AccountFunction.get_payout_transaction_id()
            logger.info('transaction_id是{}'.format(transaction_id))
            headers['Authorization'] = "Bearer " + AccountFunction.get_account_token()
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url, transaction_id),
                                headers=headers)
            AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'status' in r.text, "查询提现详情错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_009 使用错误id查询提现详情')
    @pytest.mark.multiprocess
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

    @allure.testcase('test_payout_010 法币提现获得信息')
    @pytest.mark.multiprocess
    def test_payout_010(self):
        with allure.step("法币提现获得信息"):
            data = {
                'code': 'EUR',
                'payment_method': 'SEPA'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
            AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            account_names = r.json()['account_names']
            name_list = account_names.keys()
            for i in len(name_list):
                if account_names[name_list[i]] == 0:
                    print(i)

    @allure.testcase('test_payout_011 预校验法币提现')
    @pytest.mark.multiprocess
    def test_payout_011(self):
        with allure.step("法币提现获得信息"):
            with allure.step("获得token"):
                accessToken = AccountFunction.get_account_token(account='yilei6@cabital.com')
            with allure.step("把token写入headers"):
                headers['Authorization'] = "Bearer " + accessToken
            data = {
                "code": "EUR",
                "amount": "5000"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/verification'.format(env_url), data=json.dumps(data),
                                headers=headers)
            AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['fee']['code'] == 'EUR', "预校验法币提现错误，返回值是{}".format(r.text)
            assert r.json()['fee']['amount'] == '2.5', "预校验法币提现错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_012 获得法币提现币种')
    @pytest.mark.multiprocess
    @pytest.mark.pro
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

    @allure.testcase('test_payout_013 获得数字货币提现币种')
    @pytest.mark.multiprocess
    @pytest.mark.pro
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

    @allure.testcase('test_payout_014 获得全部提现币种')
    @pytest.mark.multiprocess
    @pytest.mark.pro
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

    @allure.testcase('test_payout_015 开启法币提现画面')
    @pytest.mark.multiprocess
    @pytest.mark.pro
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

    # @allure.testcase('test_payout_016 法币提现')
    # @pytest.mark.multiprocess
    # @pytest.mark.pro
    # def test_payout_016(self):
    #     with allure.step("开启法币提现画面"):
    #         headers['Authorization'] = "Bearer " + AccountFunction.get_account_token(account=get_json()['email']['payout_email'])
    #         params = {
    #             'code': 'EUR'
    #         }
    #         r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params, headers=headers)
    #         account_name = r.json()['name_list']
    #     with allure.step("法币提现"):
    #         code = AccountFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
    #         secretKey = get_json()['secretKey']
    #         totp = pyotp.TOTP(secretKey)
    #         mfaVerificationCode = totp.now()
    #         headers['X-Mfa-Otp'] = str(mfaVerificationCode)
    #         headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
    #         data = {
    #             "code": "EUR",
    #             "amount": "2.51",
    #             "payment_method": "SEPA",
    #             "account_name": account_name[0],
    #             "iban": "BE09967206444557"
    #         }
    #         r = session.request('POST', url='{}/pay/withdraw/fiat'.format(env_url), data=json.dumps(data), headers=headers)
    #         AccountFunction.add_headers()
    #         with allure.step("状态码和返回值"):
    #             logger.info('状态码是{}'.format(str(r.status_code)))
    #             logger.info('返回值是{}'.format(str(r.text)))
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert 'txn_id' in r.text, "开启法币提现画面错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_017 确认法币提现交易')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_payout_017(self):
        with allure.step("确认法币提现交易"):
            data = {
                "code": "EUR",
                "amount": "2.51",
                "payment_method": "SEPA",
                "account_name": "yilei",
                "iban": "GB11111111111111111111"
            }
            r = session.request('POST', url='{}/pay/withdraw/fiat/validate'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {} , "开启法币提现画面错误，返回值是{}".format(r.text)
