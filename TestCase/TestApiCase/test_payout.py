from Function.api_function import *
from Function.operate_sql import *
from run import *
from Function.log import *
import allure
import pyotp


class TestPayoutApi:

    # 初始化class
    def setup_class(self):
        AccountFunction.add_headers()

    @allure.testcase('test_payout_001 没有Kyc用户添加常用收款地址失败')
    def test_payout_001(self):
        account = generate_email()
        password = 'Abc112233'
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
            r = session.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data), headers=headers)
        AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_FORBIDDEN' in r.text, "没有Kyc用户添加常用收款地址失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_002 获取存储的常用收款地址list')
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
    def test_payout_004(self):
        with allure.step("使用不存在id获取常用收款地址"):
            r = session.request('GET', url='{}/account/myPayee/{}'.format(env_url, '1111300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'This address is not exist, please refresh and retry.' in r.text, "使用不存在id获取常用收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_005 删除不存在的收款地址')
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
    def test_payout_006(self):
        with allure.step("获取提现费率和提现限制"):
            data = {
                "amount": "0.11",
                "code": "ETH",
                "address": "0x623089BFb1dc2d3023Ba4bd0f42F61d66826994eu",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/verification'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '"code":"ETH"' in r.text, "获取提现费率和提现限制错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_007 MFA认证提现ETH成功')
    def test_payout_007(self):
        run.accountToken = AccountFunction.get_account_token(account=get_json()['email']['payout_email'])
        headers['Authorization'] = "Bearer " + run.accountToken
        with allure.step("发邮件"):
            requests.request('GET', url='{}/account/security/mfa/email/sendVerificationCode'.format(env_url), headers=headers)
            sleep(30)
        with allure.step("获取邮件中的验证码"):
            sleep_time = 0
            while sleep_time < 80:
                sleep_time = sleep_time + 5
                sleep(5)
                email_info = get_email()
                if '[Cabital] Verify Your Email' in email_info['title']:
                    break
            assert '[Cabital] Verify Your Email' in email_info['title'], '邮件验证码获取失败，获取的邮件标题是是{}'.format(email_info['title'])
            code = str(email_info['body']).split('"code":')[1].split('"')[1]
            secretKey = get_json()['secretKey']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
        with allure.step("提现ETH成功"):
            data = {
                "amount": "0.52",
                "code": "ETH",
                "address": "0x8D62b7C60491e5295c90D544B11F33966a3B2B7b",
                "method": "ERC20"
            }
            r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data), headers=headers)
        AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transaction_id'] is not None, "MFA认证提现ETH成功错误，返回值是{}".format(r.text)
        # with allure.step("p/l验证"):
        #     sleep(5)
        #     sql = "select * from transaction_history where transaction_id='{}';".format(r.json()['transaction_id'])
        #     print(sql)
        #     sql_info = sqlFunction.connect_mysql(db='assetstat', sql=sql)
        #     assert sql_info[0] is not None, "payout的P/L错误，sql命令是{}".format(sql)
        # with allure.step("wallet internal_balance验证"):
        #     sleep(5)
        #     sql = "select wallet_id from internal_balance where transaction_id='{}';".format(r.json()['transaction_id'])
        #     sql_info = sqlFunction.connect_mysql(db='wallet', sql=sql)
        #     for i in sql_info:
        #         assert i['wallet_id'] is not None, "payout的P/L错误，sql命令是{}".format(sql)

    @allure.testcase('test_payout_008 查询提现详情')
    def test_payout_008(self):
        with allure.step("获得交易transaction_id"):
            transaction_id = AccountFunction.get_payout_transaction_id()
            logger.info('transaction_id是{}'.format(transaction_id))
            run.accountToken = AccountFunction.get_account_token(account=get_json()['email']['payout_email'])
            headers['Authorization'] = "Bearer " + run.accountToken
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url, transaction_id), headers=headers)
            AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'status' in r.text, "查询提现详情错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_009 使用错误id查询提现详情')
    def test_payout_009(self):
        with allure.step("查询提现详情"):
            r = session.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url, '4684225231310-3fa0-4bd1-9d46-4467dfa9ce52'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'no rows in result set' in r.text, "使用错误id查询提现详情错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_010 法币提现获得信息')
    def test_payout_010(self):
        with allure.step("法币提现获得信息"):
            with allure.step("获得token"):
                accessToken = AccountFunction.get_account_token(account='yilei6@cabital.com')
            with allure.step("把token写入headers"):
                headers['Authorization'] = "Bearer " + accessToken
            data = {
                'code': 'EUR'
            }
            r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=data, headers=headers)
            AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'SEPA' in r.text, "法币提现获得信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_011 预交验法币提现')
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
            r = session.request('POST', url='{}/pay/withdraw/fiat/verification'.format(env_url), data=json.dumps(data), headers=headers)
            AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['fee'] == {"code":"EUR","amount":"0"}, "预交验法币提现错误，返回值是{}".format(r.text)

