from Function.api_function import *
from Function.operate_sql import *


# Account相关cases
class TestAccountApi:

    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    connect_account = [('5e5a2a0a-a4c3-4ced-8320-118ccbbc1c23', 'NONE', 'yilei24@163.com'),
                       ('d0f4335e-cf80-44f1-b79c-cca2cab95cac', 'MATCHED', 'yanting.huang+310@cabital.com'),
                       ('eb9659ea-0d95-4f0f-83a3-1152c5a90ee9', 'INITIALIZED', 'yanting.huang+301@cabital.com'),
                       ('358ff717-ea3c-40d4-86da-d73b4a2dce37', 'PENDING', 'yanting.huang+302@cabital.com'),
                       ('146aa112-2fd7-4cb5-a8ff-bb2fc45f55ed', 'TEMPORARY_REJECTED', 'yanting.huang+303@cabital.com'),
                       ('1799875b-5749-4056-9cc9-6fba16f0f1e0', 'FINAL_REJECTED', 'yanting.huang+304@cabital.com'),
                       ('ffa1b49e-46f6-47b3-8ea6-2c41bac6b6ed', 'CREATED', 'yanting.huang+305@cabital.com'),
                       ('bacf2b3e-6599-44f4-adf6-c4c13ff40946', 'MATCHING', 'yanting.huang+309@cabital.com'),
                       ('b7ff2c76-5dae-4ea3-bb42-4b355357072a', 'MISMATCHED', 'yanting.huang+311@cabital.com'),
                       ]

    case_title = ['test_accounts_none 用户未进行关联',
                  'test_accounts_matched 账户关联同名验证通过，完全开通同账户转账',
                  'test_accounts_initialized 用户成功连接，还未在 Cabital 提交 KYC',
                  'test_accounts_pending Capital处理用户材料中',
                  'test_accounts_temporary_rejected 用户被 Cabital 要求提供正确材料',
                  'test_accounts_final_rejected 用户被 Cabital 最终拒绝开户',
                  'test_accounts_temporary_created 用户成功 KYC，Cabital 账户开通，等待合作方提交同名验证',
                  'test_accounts_temporary_matching 合作方已提交，同名验证人工审核中',
                  'test_accounts_mismatched 同名验证拒绝，多种因素',
                  ]

    @allure.title('test_account_001')
    @allure.description('获取用户关联状况及partner信息')
    @pytest.mark.parametrize('account_id, expect_status, account_email', connect_account, ids=case_title)
    def test_account_001(self, account_id, expect_status, account_email):
        logging.info("-------------------- 开始执行用例 --------------------")
        with allure.step("测试用户的account_id"):
            account_id = account_id
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_header['ACCESS-SIGN'] = sign
            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_header['ACCESS-NONCE'] = nonce
        with allure.step("获取用户关联状况"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_header)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            if expect_status == "NONE":
                assert r.status_code == 403, "http状态码不对，目前状态码是{}".format(r.status_code)
            else:
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            if expect_status != "NONE":
                assert r.json()['account_status'] == expect_status, "获取关联用户状况,期望状态是{}，返回值是{}".format(expect_status, r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=account_email).format(account_email)
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == expect_status, "获取partner信息错误，期望状态是{},返回值是{}".format(expect_status, r.text)
        logging.info("-------------------- 结束执行用例 --------------------")

    @allure.title('test_connect_account_002')
    @allure.description('查询用户otp状态：otp未绑定（2fa disable）')
    def test_connect_account_002(self):
        with allure.step("测试用户的account_id"):
            account_id = 'eb9659ea-0d95-4f0f-83a3-1152c5a90ee9'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_header['ACCESS-SIGN'] = sign
            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_header['ACCESS-NONCE'] = nonce
        with allure.step("查询用户otp状态"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_header)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['otp_ready'] is False, "查询用户otp状态，otp未绑定错误，返回值是{}".format(r.text)

    @allure.title('test_connect_account_003')
    @allure.description('查询用户otp状态：otp已经绑定（2fa enable）')
    def test_connect_account_003(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_header['ACCESS-SIGN'] = sign
            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_header['ACCESS-NONCE'] = nonce
        with allure.step("查询用户otp状态"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_header)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['otp_ready'] is True, "查询用户otp状态，otp已经绑定错误，返回值是{}".format(r.text)

    # @allure.title('test_connect_account_004')
    # @allure.description('成功解绑+name match用户 pass')
    # def test_connect_account_04(self):
    #     with allure.step("准备参数"):
    #         account_id = 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7'
    #     with allure.step("name match 数据"):
    #         data = {
    #             'name': 'Neo DingTest6',
    #             'id': '356214563',
    #             'id_document': 'PASSPORT',
    #             'issued_by': 'HKG',
    #             'dob': '19910101'
    #         }
    #     with allure.step("验签"):
    #         unix_time = int(time.time())
    #         nonce = generate_string(30)
    #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT', url='/api/v1/accounts/{}/match'.format(account_id), nonce=nonce, body=json.dumps(data))
    #         connect_header['ACCESS-SIGN'] = sign
    #         connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
    #         connect_header['ACCESS-NONCE'] = nonce
    #     with allure.step("name match"):
    #         r = session.request('PUT', url='{}/accounts/{}/match'.format(self.url, account_id), data=json.dumps(data), headers=connect_header)
    #     with allure.step("状态码和返回值"):
    #         # logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
    #     with allure.step("校验返回值"):
    #         assert r.json()['result'] == 'PASS', "name match pass错误，返回值是{}".format(r.text)

    @allure.title('test_connect_account_005')
    @allure.description('获取用户绑定关系新（通过bybit账号获取cabital信息）')
    def test_connect_account_005(self):
        with allure.step("获取cabital账号link bybit账号"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='neoding@yandex.com')
            params = {
                'partner_ids': get_json()['bybit']['partner_id'],
                'user_ext_ref': '76c7006eba45a314687861ef73c6970a',
                'link_mode': '1'
            }
            r = session.request('GET', url='{}/connect/account/links'.format(self.url), params=params, headers=headers)
            logger.info('r.json的返回值是{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['list'][0]['partner_id'] == params['partner_ids'], "获取cabital账号link infinni games账号错误，返回值是{}".format(r.text)
                assert r.json()['list'][0]['account_links'][0]['user_ext_ref'] == get_json()['bybit']['uid_A'], "获取cabital账号link infinni games账号错误，返回值是{}".format(r.text)

    # @allure.title('test_connect_account_006')
    # @allure.description('partner unlink(改account_vid和account)')
    # def test_connect_account_006(self):
    #     headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='neoding3@yeah.net', password='Zcdsw123')
    #     partner_id = get_json()["bybit"]["partner_id"]
    #     account_id = "27fa917f-11d7-4a16-8a13-1fd74268c870"
    #     with allure.step("获得data"):
    #         data = {
    #             "channel": "PARTNER"
    #         }
    #     with allure.step("验签"):
    #         unix_time = int(time.time())
    #         nonce = generate_string(30)
    #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
    #                                             url='/api/v1/accounts/{}/unlink'.format(account_id),
    #                                                 nonce=nonce, body=json.dumps(data))
    #         headers['ACCESS-SIGN'] = sign
    #         headers['ACCESS-TIMESTAMP'] = str(unix_time)
    #         headers['ACCESS-NONCE'] = nonce
    #         headers['ACCESS-KEY'] = partner_id
    #         r = session.request('POST', url='{}/accounts/{}/unlink'.format(self.url, account_id), data=json.dumps(data), headers=headers)
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
