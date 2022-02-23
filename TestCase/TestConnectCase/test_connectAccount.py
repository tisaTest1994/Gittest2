from Function.api_function import *
from Function.operate_sql import *


# Connect相关cases
class TestConnectAccountApi:

    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_connect_account_001 获取未关联用户状况及partner信息')
    def test_connect_account_001(self):
        with allure.step("测试用户的account_id"):
            account_id = '5e5a2a0a-a4c3-4ced-8320-118ccbbc1c23'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='{}/accounts/{}/detail'.format(self.url, account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取未关联用户状况"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '' == r.text, "获取未关联用户状况错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yilei24@163.com')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'NONE', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_002 获取关联用户状况，用户成功连接，还未在 Cabital 提交 KYC')
    def test_connect_account_002(self):
        with allure.step("测试用户的account_id"):
            account_id = 'e19a6fa7-1b7d-4396-a8cf-f641467a910b'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，用户成功连接，还未在 Cabital 提交 KYC"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'INITIALIZED', "获取关联用户状况，用户成功连接，还未在 Cabital 提交 KYC错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc01@test.com', password='A!234sdfg')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'INITIALIZED', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_003 获取关联用户状况，Cabital处理用户材料中')
    def test_connect_account_003(self):
        with allure.step("测试用户的account_id"):
            account_id = 'ba524ba1-5887-4920-b1c4-242badfcb2ed'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，Cabital处理用户材料中"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'PENDING', "获取关联用户状况，Cabital处理用户材料中错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc02@test.com', password='A!234sdfg')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'PENDING', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_004 获取关联用户状况，用户被 Cabital 要求提供正确材料')
    def test_connect_account_004(self):
        with allure.step("测试用户的account_id"):
            account_id = '54979397-8ee0-4b61-8c78-cac78116e898'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，用户被 Cabital 要求提供正确材料"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'TEMPORARY_REJECTED', "获取关联用户状况，Cabital处理用户材料中错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc03@test.com', password='A!234sdfg')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'TEMPORARY_REJECTED', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_005 获取关联用户状况，用户被 Cabital 最终拒绝开户')
    def test_connect_account_005(self):
        with allure.step("测试用户的account_id"):
            account_id = 'c7916ad3-36a8-48cd-83d3-fff5a911fcc7'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，用户被 Cabital 最终拒绝开户"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'FINAL_REJECTED', "获取关联用户状况，用户被 Cabital 最终拒绝开户错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc04@test.com', password='A!234sdfg')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'FINAL_REJECTED', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_006 获取关联用户状况，用户成功 KYC，Cabital 账户开通，等待合作方提交同名验证。')
    def test_connect_account_006(self):
        with allure.step("测试用户的account_id"):
            account_id = '90da0a64-4871-4d7e-b4a5-c80bf4ec9d5e'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，用户成功 KYC，Cabital 账户开通，等待合作方提交同名验证。"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'CREATED', "获取关联用户状况，用户成功 KYC，Cabital 账户开通，等待合作方提交同名验证。错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc05@test.com', password='A!234sdfg')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'CREATED', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_007 获取关联用户状况，合作方已提交，同名验证人工审核中')
    def test_connect_account_007(self):
        with allure.step("测试用户的account_id"):
            account_id = '63254fe2-8a65-457b-b6bd-075ca7160f26'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，合作方已提交，同名验证人工审核中"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'MATCHING', "获取关联用户状况，合作方已提交，同名验证人工审核中错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc06@test.com', password='A!234sdfg')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'MATCHING', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_008 获取关联用户状况，同名验证通过，完全开通同账户转账')
    def test_connect_account_008(self):
        with allure.step("测试用户的account_id"):
            account_id = '3853a783-3a36-4713-b62a-c44960a9ed9d'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，同名验证通过，完全开通同账户转账"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'MATCHED', "获取关联用户状况，同名验证通过，完全开通同账户转账错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc07@test.com', password='A!234sdfg')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'MATCHED', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_009 获取关联用户状况，同名验证拒绝，多种因素')
    def test_connect_account_009(self):
        with allure.step("测试用户的account_id"):
            account_id = 'eed8b5fe-9242-4fbf-99f1-3bae94b3176c'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，同名验证拒绝，多种因素"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'MISMATCHED', "获取关联用户状况，同名验证拒绝，多种因素错误，返回值是{}".format(r.text)
        with allure.step("获取partner信息"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='winniekyc08@test.com', password='A!234sdfg')
            r = session.request('GET', url='{}/connect/account/info'.format(self.url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            for i in r.json()['account_bindings']:
                if i['partner_id'] == get_json()['connect']['test']['bybit']['Headers']['ACCESS-KEY']:
                    assert i['status'] == 'MISMATCHED', "获取未关联用户状况及partner信息失败，返回值是{}".format(r.text)

    @allure.title('test_connect_account_010 查询用户otp状态，otp未绑定')
    def test_connect_account_010(self):
        with allure.step("测试用户的account_id"):
            account_id = 'e19a6fa7-1b7d-4396-a8cf-f641467a910b'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，用户成功连接，还未在 Cabital 提交 KYC"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['otp_ready'] is False, "查询用户otp状态，otp未绑定错误，返回值是{}".format(r.text)

    @allure.title('test_connect_account_011 查询用户otp状态，otp已经绑定')
    def test_connect_account_011(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，用户成功连接，还未在 Cabital 提交 KYC"):
            r = session.request('GET', url='{}/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['otp_ready'] is True, "查询用户otp状态，otp已经绑定错误，返回值是{}".format(r.text)

    # @allure.title('test_connect_account_012 使用错误account_id导致解除绑定失败')
    # def test_connect_account_012(self):
    #     with allure.step("测试用户的account_id"):
    #         partner_id = get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']
    #     with allure.step("验签"):
    #         unix_time = int(time.time())
    #         nonce = generate_string(30)
    #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/connect/account/{}/unlink'.format(partner_id), nonce=nonce)
    #         connect_headers['ACCESS-SIGN'] = sign
    #         connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
    #         connect_headers['ACCESS-NONCE'] = nonce
    #     with allure.step("使用错误account_id导致解除绑定失败"):
    #         r = session.request('POST', url='{}/connect/account/{}/unlink'.format(self.url, partner_id), headers=connect_headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 401, "http状态码不对，目前状态码是{}".format(r.status_code)
    #     with allure.step("校验返回值"):
    #         assert r.json()['otp_ready'] is True, "查询用户otp状态，otp已经绑定错误，返回值是{}".format(r.text)

    @allure.title('test_connect_account_013 成功解绑+name match用户 pass')
    def test_connect_account_013(self):
        with allure.step("准备参数"):
            account_id = '95c3f010-b008-40f1-bd80-40713e2f1aa8'
        with allure.step("name match 数据"):
            data = {
                'name': 'yanting37 huang3',
                'id': '12345678',
                'id_document': 'PASSPORT',
                'issued_by': 'HKG',
                'dob': '19860101'
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT', url='/api/v1/accounts/{}/match'.format(account_id), nonce=nonce, body=json.dumps(data))
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("name match"):
            r = session.request('PUT', url='{}/accounts/{}/match'.format(self.url, account_id), data=json.dumps(data), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['result'] == 'PASS', "name match pass错误，返回值是{}".format(r.text)
    #
    # @allure.title('test_connect_account_014 成功解绑+name match用户mismatch')
    # def test_connect_account_014(self):
    #     with allure.step("准备参数"):
    #         partner_id = get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']
    #         headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yanting.huang@cabital.com', password='85600327158Hyt')
    #     with allure.step("unlink the cabital connect"):
    #         r = session.request('POST', url='{}/connect/account/{}/unlink'.format(self.url, partner_id), headers=headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码和返回值"):
    #         if r.status_code == 200:
    #             assert r.json() == {}, "unlink the cabital connect错误，返回值是{}".format(r.text)
    #         elif r.status_code == 400:
    #             assert r.json()['code'] == '109001', "unlink the cabital connect错误，返回值是{}".format(r.text)
    #     with allure.step("name match 数据"):
    #         data = {
    #             'name': 'alice333 wang222',
    #             'id': '14666',
    #             'id_document': 'PASSPORT',
    #             'issued_by': 'HKG',
    #             'dob': '19920202'
    #         }
    #     with allure.step("验签"):
    #         unix_time = int(time.time())
    #         nonce = generate_string(30)
    #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT', url='/api/v1/accounts/{}/match'.format(account_id), nonce=nonce, body=json.dumps(data))
    #         connect_headers['ACCESS-SIGN'] = sign
    #         connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
    #         connect_headers['ACCESS-NONCE'] = nonce
    #         print(connect_headers)
    #     with allure.step("name match"):
    #         r = session.request('PUT', url='{}/accounts/{}/match'.format(self.url, account_id), data=json.dumps(data), headers=connect_headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
    #     with allure.step("校验返回值"):
    #         assert r.json()['result'] == 'MISMATCH', "name match pass错误，返回值是{}".format(r.text)
    #
    # @allure.title('test_connect_account_015 成功解绑+name match用户matching')
    # def test_connect_account_015(self):
    #     with allure.step("准备参数"):
    #         partner_id = get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']
    #         headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='alice.wang@cabital.com')
    #         account_id = '2d41bbd6-8298-43e5-81a9-ca1b359c421f'
    #     with allure.step("unlink the cabital connect"):
    #         r = session.request('POST', url='{}/connect/account/{}/unlink'.format(self.url, partner_id), headers=headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码和返回值"):
    #         if r.status_code == 200:
    #             assert r.json() == {}, "unlink the cabital connect错误，返回值是{}".format(r.text)
    #         elif r.status_code == 400:
    #             assert r.json()['code'] == '109001', "unlink the cabital connect错误，返回值是{}".format(r.text)
    #     with allure.step("name match 数据"):
    #         data = {
    #             'name': 'alice3331 wang222',
    #             'id': '124666',
    #             'id_document': 'PASSPORT',
    #             'issued_by': 'HKG',
    #             'dob': '19980202'
    #         }
    #     with allure.step("验签"):
    #         unix_time = int(time.time())
    #         nonce = generate_string(30)
    #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT', url='/api/v1/accounts/{}/match'.format(account_id), nonce=nonce, body=json.dumps(data))
    #         connect_headers['ACCESS-SIGN'] = sign
    #         connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
    #         connect_headers['ACCESS-NONCE'] = nonce
    #         print(connect_headers)
    #     with allure.step("name match"):
    #         r = session.request('PUT', url='{}/accounts/{}/match'.format(self.url, account_id), data=json.dumps(data), headers=connect_headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
    #     with allure.step("校验返回值"):
    #         assert r.json()['result'] == 'MISMATCH', "name match pass错误，返回值是{}".format(r.text)
    #
    # @allure.title('test_connect_account_016 成功解绑+name match用户pending')
    # def test_connect_account_016(self):
    #     with allure.step("准备参数"):
    #         partner_id = get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']
    #         headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='alice.wang+21@cabital.com')
    #         account_id = '5d1e1145-b470-4fca-b9dc-b7ed3d3ccd0e'
    #     with allure.step("unlink the cabital connect"):
    #         r = session.request('POST', url='{}/connect/account/{}/unlink'.format(self.url, partner_id), headers=headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码和返回值"):
    #         if r.status_code == 200:
    #             assert r.json() == {}, "unlink the cabital connect错误，返回值是{}".format(r.text)
    #         elif r.status_code == 400:
    #             assert r.json()['code'] == '109001', "unlink the cabital connect错误，返回值是{}".format(r.text)
    #     with allure.step("name match 数据"):
    #         data = {
    #             'name': 'alice3331 wang222',
    #             'id': '124666',
    #             'id_document': 'PASSPORT',
    #             'issued_by': 'HKG',
    #             'dob': '19980202'
    #         }
    #     with allure.step("验签"):
    #         unix_time = int(time.time())
    #         nonce = generate_string(30)
    #         sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT', url='/api/v1/accounts/{}/match'.format(account_id), nonce=nonce, body=json.dumps(data))
    #         connect_headers['ACCESS-SIGN'] = sign
    #         connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
    #         connect_headers['ACCESS-NONCE'] = nonce
    #         print(connect_headers)
    #     with allure.step("name match"):
    #         r = session.request('PUT', url='{}/accounts/{}/match'.format(self.url, account_id), data=json.dumps(data), headers=connect_headers)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
    #     with allure.step("校验返回值"):
    #         assert r.json()['result'] == 'PENDING', "name match pass错误，返回值是{}".format(r.text)