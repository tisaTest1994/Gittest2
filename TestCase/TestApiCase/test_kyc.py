from Function.api_function import *
from run import *
from Function.log import *
import allure


# kyc相关cases
class TestKycApi:

    @allure.testcase('test_kyc_001 通过kyc的用户，获取kyc上传token失败')
    def test_kyc_001(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("随机获得国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
            data = {
                "citizenCountryCode": citizenCountryCode
            }
        with allure.step("通过kyc的用户，获取kyc上传token失败"):
            r = requests.request('POST', url='{}/kyc/case/start'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'KYC_CASE_000006' in r.text, "通过kyc的用户，获取kyc上传token失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_002 未通过kyc的用户，获取kyc上传token')
    def test_kyc_002(self):
        account = generate_email()
        password = 'Abc112233'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("未通过kyc的用户，获取kyc上传token"):
            data = {
                "citizenCountryCode": citizenCountryCode
            }
            r = requests.request('POST', url='{}/kyc/case/start'.format(env_url), data=json.dumps(data),
                                 headers=headers)
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
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        allure.dynamic.description("调用kyc")
        with allure.step("未申请kyc获取kyc-case失败"):
            data = {
            }
            r = requests.request('POST', url='{}/kyc/case/get'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'informations' in r.text, "未申请kyc获取kyc-case信息失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_004 获取kyc-case信息')
    def test_kyc_004(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取kyc-case信息"):
            data = {
            }
            r = requests.request('POST', url='{}/kyc/case/get'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'id' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)