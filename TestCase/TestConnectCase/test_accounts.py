import pytest

from Function.api_function import *
from Function.operate_sql import *


# Account相关cases
class TestAccountApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    connect_account = [('d0f4335e-cf80-44f1-b79c-cca2cab95cac', 'MATCHED'),
                       ('eb9659ea-0d95-4f0f-83a3-1152c5a90ee9', 'INITIALIZED'),
                       ('358ff717-ea3c-40d4-86da-d73b4a2dce37', 'PENDING'),
                       ('146aa112-2fd7-4cb5-a8ff-bb2fc45f55ed', 'TEMPORARY_REJECTED'),
                       ('1799875b-5749-4056-9cc9-6fba16f0f1e0', 'FINAL_REJECTED'),
                       ('ffa1b49e-46f6-47b3-8ea6-2c41bac6b6ed', 'CREATED'),
                       ('bacf2b3e-6599-44f4-adf6-c4c13ff40946', 'MATCHING'),
                       ('b7ff2c76-5dae-4ea3-bb42-4b355357072a', 'MISMATCHED'),
                       ('3fde7f5f-f7a7-4230-8963-89c2303039e0', 'UNLINKED'),
                       ]

    case_title = ['test_accounts_matched 账户关联同名验证通过，完全开通同账户转账',
                  'test_accounts_initialized 用户成功连接，还未在 Cabital 提交 KYC',
                  'test_accounts_pending Capital处理用户材料中',
                  'test_accounts_temporary_rejected 用户被 Cabital 要求提供正确材料',
                  'test_accounts_final_rejected 用户被 Cabital 最终拒绝开户',
                  'test_accounts_temporary_created 用户成功 KYC，Cabital 账户开通，等待合作方提交同名验证',
                  'test_accounts_temporary_matching 合作方已提交，同名验证人工审核中',
                  'test_accounts_mismatched 同名验证拒绝，多种因素',
                  'test_accounts_unlinked 同用户/Cabital主动关闭与合作方的某账户关联',
                  ]

    @allure.description('账户关联相关--kyc状态检查')
    @allure.testcase('https://whimsical.com/connect-RvyvBQf9aZhV55KqNEALHy', name='点击，跳转测试用例的链接地址')
    @pytest.mark.flaky(reruns=2, reruns_delay=3)  # 遇到失败的用例重跑2次，每次间隔3s
    @pytest.mark.parametrize('account_id,expect_status', connect_account, ids=case_title)
    def test_connect_status_check(self, account_id, expect_status):
        logging.info("********************开始执行用例********************")
        with allure.step("测试账号的account_id"):
            account_id = account_id
        with allure.step("验 签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("请求接口/accounts/{}/detail"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('detail接口返回值是{}'.format(str(r.text)))
            logger.info("connect_status ==>> 期望结果:{},实际结果:【{}】".format(expect_status,
                                                                       r.json()['account_status']))
            assert r.json()['account_status'] == expect_status
            logging.info("********************结束执行用例********************")

    @allure.description('账户关联相关--otp状态检查')
    @allure.title('test_opt_check_001 同名账户关联成功，otp状态true检查')
    def test_otp_status_true(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("请求接口/accounts/{}/detail"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('返回值是{}'.format(str(r.text)))
            logger.info("otp_status ==>> 期望结果:True,实际结果:【{}】".format(r.json()['otp_ready']))
            assert r.json()['otp_ready'] is True

    @allure.description('账户关联相关--otp状态检查')
    @allure.title('test_opt_check_002 同名账户关联成功，otp状态false检查')
    def test_otp_status_false(self):
        with allure.step("测试用户的account_id"):
            account_id = 'd0f4335e-cf80-44f1-b79c-cca2cab95cac'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("请求接口/accounts/{}/detail"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('返回值是{}'.format(str(r.text)))
            logger.info("otp_status ==>> 期望结果:False,实际结果:【{}】".format(r.json()['otp_ready']))
            assert r.json()['otp_ready'] is False

    @allure.description('账户关联相关--同名验证')
    @allure.title('test_information_success_001关联同名账户验证匹配成功')
    @pytest.mark.skip(reason='match只能一次')
    def test_information_match_check_success(self):
        with allure.step("准备 参数"):
            account_id = 'c8dcc6c3-924d-40ef-942a-d1cdc5f880da'
        with allure.step("name match 数据"):
            data = {
                'name': 'qq',
                'id': '1122',
                'id_document': 'PASSPORT',
                'issued_by': 'HKG',
                'dob': '19991111'
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT',
                                                url='/api/v1/accounts/{}/match'.format(account_id), nonce=nonce,
                                                body=json.dumps(data))
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("请求接口{}/accounts/{}/match"):
            r = session.request('PUT', url='{}/accounts/{}/match'.format(self.url, account_id), data=json.dumps(data),
                                headers=connect_headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info('match接口返回值是{}'.format(str(r.text)))
            logger.info("match_status==>> 期望结果:PASS,实际结果:【{}】".format(r.json()['result']))
            assert r.json()['result'] == 'PASS'
