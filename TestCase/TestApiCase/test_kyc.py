from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api kyc 相关 testcases")
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

    @allure.title('test_kyc_003')
    @allure.description('查询当前用户信息')
    def test_kyc_003(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='richard.wan@cabital.com')
        with allure.step("查询当前用户信息接口/account/info"):
            r = session.request('GET', url='{}/account/info'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info(r.text)
            assert r.json()['user'] is not None

    @allure.title('test_kyc_004 获取用户补充信息，补充信息为空检查')
    @allure.description('用户kyc已过，补充信息未填写')
    def test_kyc_004(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yFnp4dxNs@qq.com')
        with allure.step("获取用户补充信息接口/additional/info"):
            r = session.request('GET', url='{}/account/additional/info'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info(r.text)
            assert r.json()['additionalInfos'] == {}, "获取用户补充信息, 补充信息为空失败，返回值是{}".format(r.text)

    @allure.title('test_kyc_005 获取用户补充信息，补充信息不为空检查')
    @allure.description('用户kyc已过，补充信息已填写')
    def test_kyc_005(self):
        with allure.step("获取用户补充信息接口/additional/info"):
            r = session.request('GET', url='{}/account/additional/info'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            logger.info(r.text)
            logger.info("additionalInfos==>> 期望结果:'PHONE'：'+5512345678901,'TAX_ID': '026.105.214-48'"
                        "实际结果:【'cpf'{}'PHONE'{}'name'{} 】".format(r.json()['additionalInfos']['TAX_ID'],
                                                                  r.json()['additionalInfos']['PHONE'],
                                                                  r.json()['additionalInfos']['CAPITUAL_ACCOUNT_NAME']))
            assert r.json()['additionalInfos']['PHONE'] == '+5512345678901', "获取用户补充信息, 补充信息不为空失败，返回值是{}".format(r.text)
            assert r.json()['additionalInfos']['TAX_ID'] == '026.105.214-48', "获取用户补充信息, 补充信息不为空失败，返回值是{}".format(
                r.text)
            assert r.json()['additionalInfos'][
                       'CAPITUAL_ACCOUNT_NAME'] == 'Wan yilei', "获取用户补充信息, 补充信息不为空失败，返回值是{}".format(
                r.text)

    @allure.title('test_kyc_006 老用户添加补充信息')
    @allure.description('用户kyc已过，填写补充信息')
    def test_kyc_006(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='MCo3Ub@qq.com')
        TAX_ID = '192.168.900-10'
        PHONE = '+5510987659934'
        with allure.step("获取用户补充信息接口/additional/info"):
            data = {
                "additionalInfos":
                    {
                        "TAX_ID": TAX_ID,
                        "PHONE": PHONE
                    }
            }

            r = session.request('PUT', url='{}/account/additional/info/update'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("模拟"):
            logger.info(r.text)

