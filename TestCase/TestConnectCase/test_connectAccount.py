from Function.api_function import *
from Function.operate_sql import *


# Connect相关cases
class TestConnectAccountApi:

    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.testcase('test_connect_account_001 获取未关联用户状况')
    def test_connect_account_001(self):
        with allure.step("测试用户的account_id"):
            account_id = get_json()['email']['accountId']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取未关联用户状况"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '' == r.text, "获取未关联用户状况错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_002 获取关联用户状况')
    def test_connect_account_002(self):
        with allure.step("测试用户的account_id"):
            account_id = 'ec50fed7-c7aa-43a7-a44f-da44e05726b5'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/accounts/{}/detail'.format(account_id), nonce=nonce)
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况"):
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'MATCHED', "获取关联用户状况错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_003 获取关联用户状况，用户成功连接，还未在 Cabital 提交 KYC')
    def test_connect_account_003(self):
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
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'INITIALIZED', "获取关联用户状况，用户成功连接，还未在 Cabital 提交 KYC错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_005 获取关联用户状况，Cabital处理用户材料中')
    def test_connect_account_005(self):
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
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
            
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'PENDING', "获取关联用户状况，Cabital处理用户材料中错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_006 获取关联用户状况，用户被 Cabital 要求提供正确材料')
    def test_connect_account_006(self):
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
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'TEMPORARY_REJECTED', "获取关联用户状况，Cabital处理用户材料中错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_007 获取关联用户状况，用户被 Cabital 最终拒绝开户')
    def test_connect_account_007(self):
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
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'FINAL_REJECTED', "获取关联用户状况，用户被 Cabital 最终拒绝开户错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_008 获取关联用户状况，用户成功 KYC，Cabital 账户开通，等待合作方提交同名验证。')
    def test_connect_account_008(self):
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
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'CREATED', "获取关联用户状况，用户成功 KYC，Cabital 账户开通，等待合作方提交同名验证。错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_009 获取关联用户状况，合作方已提交，同名验证人工审核中')
    def test_connect_account_009(self):
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
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'MATCHING', "获取关联用户状况，合作方已提交，同名验证人工审核中错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_010 获取关联用户状况，同名验证通过，完全开通同账户转账')
    def test_connect_account_010(self):
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
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'MATCHED', "获取关联用户状况，同名验证通过，完全开通同账户转账错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_011 获取关联用户状况，同名验证拒绝，多种因素')
    def test_connect_account_011(self):
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
            r = session.request('GET', url='{}/api/v1/accounts/{}/detail'.format(self.url, account_id), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['account_status'] == 'MISMATCHED', "获取关联用户状况，同名验证拒绝，多种因素错误，返回值是{}".format(r.text)

    @allure.testcase('test_connect_account_012 关联已经关联过的用户')
    def test_connect_account_012(self):
        with allure.step("测试用户的account_id"):
            account_id = '63254fe2-8a65-457b-b6bd-075ca7160f26'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            data = {
                'name': 'winniekyc06 TEST',
                'id': 'DFKM55645',
                'id_document': 'PASSPORT',
                'issued_by': 'HONGKONG',
                'dob': '19790606'
            }
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT', url='/api/v1/accounts/{}/match'.format(account_id), nonce=nonce, body=json.dumps(data))
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("获取关联用户状况，同名验证拒绝，多种因素"):
            r = session.request('PUT', url='{}/api/v1/accounts/{}/match'.format(self.url, account_id), data=json.dumps(data), headers=connect_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['mismatch_fields'] == 'null', "获取关联用户状况，同名验证拒绝，多种因素错误，返回值是{}".format(r.text)

