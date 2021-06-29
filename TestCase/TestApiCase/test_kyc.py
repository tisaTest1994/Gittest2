import json
import http.client
from Function.api_function import *
from run import *
from Function.log import *
import allure


# kyc相关cases
class TestKycApi:

    kyc_url = get_json()['kycUrl']
    kyc_headers = get_json()['kycHeaders']

    # 初始化class
    def setup_class(self):
        AccountFunction.add_headers()

    @allure.testcase('test_kyc_001 通过kyc的用户，获取kyc上传token失败')
    def test_kyc_001(self):
        with allure.step("随机获得国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
            data = {
                "citizenCountryCode": citizenCountryCode
            }
        with allure.step("通过kyc的用户，获取kyc上传token失败"):
            r = session.request('POST', url='{}/kyc/case/start'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Exist pass case.' in r.text, "通过kyc的用户，获取kyc上传token失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_002 未通过kyc的用户，获取kyc上传token')
    def test_kyc_002(self):
        account = generate_email()
        password = 'Abc112233'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("未通过kyc的用户，获取kyc上传token"):
            data = {
                "citizenCountryCode": citizenCountryCode
            }
            r = session.request('POST', url='{}/kyc/case/start'.format(env_url), data=json.dumps(data), headers=headers)
        AccountFunction.get_account_token()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Cabital_LT_KYC_Mobile_Basic' in r.text, "通过kyc的用户，获取kyc上传token错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_003 未申请kyc获取kyc-case信息失败')
    def test_kyc_003(self):
        account = generate_email()
        password = 'Abc112233'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        allure.dynamic.description("调用kyc")
        with allure.step("未申请kyc获取kyc-case失败"):
            data = {
            }
            r = session.request('POST', url='{}/kyc/case/get'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'informations' in r.text, "未申请kyc获取kyc-case信息失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_004 获取kyc-case信息')
    def test_kyc_004(self):
        with allure.step("获取kyc-case信息"):
            data = {
            }
            r = session.request('POST', url='{}/kyc/case/get'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'id' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)

# 以下是提供给bybit的kyc接口

    @allure.testcase('test_kyc_005 创建Kyc case')
    def test_kyc_005(self):
        externalCaseId = generate_string(30)
        kyc_headers = self.kyc_headers
        data = {
            "externalCaseId": externalCaseId,
            "screenType": "INDIVIDUAL",
            "fullName": "John Doe",
            "individualInfo": {
                "gender": "MALE",
                "dob": "2002-02-02",
                "nationality": "JPN",
                "residentialCountry": "HKG"
            },
            "organizationInfo": {
                "registeredCountry": "HKG"
            }
        }
        unix_time = int(time.time())
        sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/cases', body=json.dumps(data))
        kyc_headers['ACCESS-SIGN'] = sign
        kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        r = session.request('POST', url='{}/cases'.format(self.kyc_url), data=json.dumps(data), headers=kyc_headers)
        print(r.url)
        print(r.text)


        conn = http.client.HTTPSConnection('api.pipedream.com')
        conn.request("GET", '/v1/sources/dc_yLujK7K/event_summaries?expand=event', '', {
            'Authorization': 'Bearer <api_key>',
        })

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

    @allure.testcase('test_kyc_006 查询Kyc case')
    def test_kyc_006(self):
        kyc_headers = self.kyc_headers
        unix_time = int(time.time())
        sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='{}/cases'.format(self.kyc_url))
        caseSystemId = '509ec7ae-e9e1-4c8e-899b-9c861c6bf64b'
        kyc_headers['ACCESS-SIGN'] = sign
        kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        r = session.request('GET', url='{}/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
        print(r.text)

    @allure.testcase('test_kyc_007 打开特定 KYC Case 的持续性扫描')
    def test_kyc_007(self):
        kyc_headers = self.kyc_headers
        caseSystemId = '509ec7ae-e9e1-4c8e-899b-9c861c6bf64b'
        r = session.request('POST', url='{}/cases/{}/ogs'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
        print(r.text)

    @allure.testcase('test_kyc_008 关闭特定 KYC Case 的持续性扫描')
    def test_kyc_008(self):
        kyc_headers = self.kyc_headers
        caseSystemId = '509ec7ae-e9e1-4c8e-899b-9c861c6bf64b'
        r = session.request('DELETE', url='{}/cases/{}/ogs'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
        print(r.text)

    @allure.testcase('test_kyc_008 关闭特定 KYC Case 的持续性扫描')
    def test_kyc_009(self):
        kyc_headers = self.kyc_headers
        caseSystemId = '509ec7ae-e9e1-4c8e-899b-9c861c6bf64b'
        data = {
            "decision": "ACCEPT",
            "comment": "决策备注"
        }
        r = session.request('POST', url='{}/cases/{}/decision'.format(self.kyc_url, caseSystemId), data=json.dumps(data), headers=kyc_headers)
        print(r.text)


    def test_kyc_015(self):
        conn = http.client.HTTPSConnection('api.pipedream.com')
        conn.request("GET", '/v1/sources/dc_yLujK7K/event_summaries?expand=event', '', {
            'Authorization': 'Bearer 7759a7e3653dcef8500ffe2c577102e6',
        })
        res = conn.getresponse()
        data = res.read()


        print(data.decode("utf-8"))
