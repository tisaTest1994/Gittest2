from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api kyc 相关 testcases")
class TestKycApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_kyc_001')
    @allure.description('通过kyc的用户，获取kyc上传token失败')
    def test_kyc_001(self):
        with allure.step("随机获得国家代码"):
            citizenCountryCode = random.choice(get_json('country_code_list.json')['citizenCountryCodeList'])
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
            assert r.json()['code'] == '002006', "通过kyc的用户，获取kyc上传token失败错误，返回值是{}".format(r.text)

    @allure.title('test_kyc_002')
    @allure.description('未通过kyc的用户，获取kyc上传token')
    def test_kyc_002(self):
        account = generate_email()
        logger.info('account 是 {}'.format(account))
        password = 'Abc112233'
        with allure.step("提前先注册好"):
            ApiFunction.sign_up(account, password)
        with allure.step("获得token"):
            accessToken = ApiFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(get_json('country_code_list.json')['citizenCountryCodeList'])
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

    @allure.title('test_kyc_003')
    @allure.description('查询当前用户信息')
    def test_kyc_003(self):
        with allure.step("查询当前用户信息接口/account/info"):
            r = session.request('GET', url='{}/account/info'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info(r.text)
            assert r.json()['user'] is not None

    @allure.title('test_kyc_004')
    @allure.description('用户kyc已过，补充信息未填写')
    def test_kyc_004(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yilei3@163.com')
        with allure.step("获取用户补充信息接口/additional/info"):
            r = session.request('GET', url='{}/kyc/user/info/additional'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['additionalInfos'] is None, "获取用户补充信息, 补充信息为空失败，返回值是{}".format(r.text)

    @allure.title('test_kyc_005')
    @allure.description('用户kyc已过，补充信息已填写')
    def test_kyc_005(self):
        with allure.step("获取用户补充信息接口"):
            r = session.request('GET', url='{}/kyc/user/info/additional'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['additionalInfos']['PHONE'] == '+5512345678901', "获取用户补充信息, 补充信息不为空失败，返回值是{}".format(r.text)
            assert r.json()['additionalInfos']['TAX_ID'] == '540.265.205-87', "获取用户补充信息, 补充信息不为空失败，返回值是{}".format(
                r.text)
            assert r.json()['additionalInfos'][
                       'CAPITUAL_ACCOUNT_NAME'] == 'Wan yilei', "获取用户补充信息, 补充信息不为空失败，返回值是{}".format(
                r.text)

    @allure.title('test_kyc_006')
    @allure.description('巴西籍用户填写补充信息检查，用户kyc已过，补充信息已填写，修改cpf name')
    def test_kyc_006(self):
        cpf_name = 'test' + str(random.randint(1, 100))
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yanting.huang+174@cabital.com')
        with allure.step("获取用户补充信息接口/account/additional/info/update"):
            data = {
                "additionalInfos": {
                    "IDENTITY_NAME": cpf_name
                }
            }
            r = session.request('PUT', url='{}/kyc/user/info/additional/update'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):

            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("获取用户补充信息"):
            r2 = session.request('GET', url='{}/kyc/user/info/additional'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r2.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            assert r2.json()['additionalInfos']["IDENTITY_NAME"] == data['additionalInfos']["IDENTITY_NAME"]

    @allure.title('test_kyc_007')
    @allure.description('巴西籍用户填写补充信息检查，用户kyc已过，补充信息已填写')
    def test_kyc_007(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='KdNXYUK6YK@163.com')
        with allure.step("获取用户必填的KYC数据，获取数据为空"):
            r = session.request('GET', url='{}/kyc/user/info/required'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['registryPurpose'] != [], "获取用户必填的KYC数据，获取数据为空失败，返回值是{}".format(r.text)

    @allure.title('test_kyc_008')
    @allure.description('获取用户必填的KYC数据，获取数据为空')
    def test_kyc_008(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='KdNXYUK6YK@163.com')
        with allure.step("获取用户必填的KYC数据，获取数据为空"):
            r = session.request('GET', url='{}/kyc/user/info/required'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['registryPurpose'] != [], "获取用户必填的KYC数据，获取数据为空失败，返回值是{}".format(r.text)

    @allure.title('test_kyc_009')
    @allure.description('获取用户必填的KYC数据，获取全部信息')
    def test_kyc_009(self):
        with allure.step("获取用户必填的KYC数据，获取全部信息"):
            r = session.request('GET', url='{}/kyc/user/info/required'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '"missing":null' in r.text, "获取用户必填的KYC数据，获取全部信息失败，返回值是{}".format(r.text)

    @allure.title('test_kyc_010')
    @allure.description('补充用户必填的kyc数据')
    def test_kyc_010(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yilei33@163.com')
        with allure.step("获取用户必填的KYC数据，获取全部信息"):
            r = session.request('GET', url='{}/kyc/user/info/required'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):

            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['registryPurpose'][2] is not None, "获取用户必填的KYC数据，获取全部信息失败，返回值是{}".format(r.text)

    @allure.title('test_kyc_011')
    @allure.description('获取用户全部补充信息')
    def test_kyc_011(self):
        with allure.step("获取用户必填的KYC数据，获取全部信息"):
            r = session.request('GET', url='{}/kyc/user/info/additional'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):

            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['userId'] is not None and r.json()['additionalInfos'] is not None, "获取用户全部补充信息失败，返回值是{}".format(r.text)

    def test_kyc_test(self):
        pass
    def test_aaa1(self):
        pass