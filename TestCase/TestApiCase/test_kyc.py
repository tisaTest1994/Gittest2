from Function.api_function import *
from Function.operate_sql import *


# kyc相关cases
class TestKycApi:
    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_kyc_001 通过kyc的用户，获取kyc上传token失败')
    def test_kyc_001(self):
        with allure.step("随机获得国家代码"):
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
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

    @allure.title('test_kyc_002 未通过kyc的用户，获取kyc上传token')
    def test_kyc_002(self):
        account = generate_email()
        password = 'Abc112233'
        with allure.step("提前先注册好"):
            ApiFunction.sign_up(account, password)
        with allure.step("获得token"):
            accessToken = ApiFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
        with allure.step("未通过kyc的用户，获取kyc上传token"):
            data = {
                "citizenCountryCode": citizenCountryCode
            }
            r = session.request('POST', url='{}/kyc/case/start'.format(env_url), data=json.dumps(data), headers=headers)
        ApiFunction.get_account_token()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == '002012', "通过kyc的用户，获取kyc上传token错误，返回值是{}".format(r.text)
