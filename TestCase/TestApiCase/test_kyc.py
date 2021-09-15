from Function.api_function import *
from Function.operate_sql import *


# kyc相关cases
class TestKycApi:
    kyc_url = get_json()['kyc'][get_json()['env']]['kycUrl']
    kyc_headers = get_json()['kyc'][get_json()['env']]['kycHeaders']

    # 初始化class
    def setup_method(self):
        AccountFunction.add_headers()

    @allure.testcase('test_kyc_001 通过kyc的用户，获取kyc上传token失败')
    @pytest.mark.multiprocess
    @pytest.mark.pro
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

    @allure.testcase('test_kyc_002 未通过kyc的用户，获取kyc上传token')
    @pytest.mark.multiprocess
    @pytest.mark.pro
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
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
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
    @pytest.mark.multiprocess
    @pytest.mark.pro
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
    @pytest.mark.multiprocess
    @pytest.mark.pro
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

    @allure.testcase('test_kyc_005 创建直接pass 个人 Kyc case后查询cases,最后发送接受结果信息')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_005(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            kyc_headers = self.kyc_headers
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "INDIVIDUAL",
                "fullName": "John Doe",
                "memo": "L++",
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
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
                caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='ScreenCompleted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='SuggestionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/reviewed', caseSystemId=caseSystemId,
                                               suggestion='SUGGEST_TO_ACCEPT')
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "ACCEPT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/api/v1/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/api/v1/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='ACCEPT',
                                               caseSystemId=caseSystemId)

    @allure.testcase('test_kyc_006 创建直接pass 个人 Kyc case后查询cases,最后发送不接受结果信息')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_006(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
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
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
                caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='ScreenCompleted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='SuggestionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/reviewed', caseSystemId=caseSystemId,
                                               suggestion='SUGGEST_TO_ACCEPT')
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认不接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "REJECT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/api/v1/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/api/v1/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='REJECT',
                                               caseSystemId=caseSystemId)

    @allure.testcase('test_kyc_007打开特定KYC Case的持续性扫描')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_kyc_007(self):
        kyc_headers = self.kyc_headers
        if get_json()['env'] == 'test':
            caseSystemId = '509ec7ae-e9e1-4c8e-899b-9c861c6bf64b'
        elif get_json()['env'] == 'pro':
            caseSystemId = 'b1eb6d06-b86d-4b21-9106-0d47c7d94c19'
        unix_time = int(time.time())
        sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                url='/api/v1/cases/{}/ogs'.format(caseSystemId))
        kyc_headers['ACCESS-SIGN'] = sign
        kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        r = session.request('POST', url='{}/api/v1/cases/{}/ogs'.format(self.kyc_url, caseSystemId),
                            headers=kyc_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '' in r.text, "打开特定KYC Case的持续性扫描错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_008 关闭特定KYC Case的持续性扫描')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_kyc_008(self):
        kyc_headers = self.kyc_headers
        unix_time = int(time.time())
        if get_json()['env'] == 'test':
            caseSystemId = '509ec7ae-e9e1-4c8e-899b-9c861c6bf64b'
        elif get_json()['env'] == 'pro':
            caseSystemId = 'b1eb6d06-b86d-4b21-9106-0d47c7d94c19'
        sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='DELETE',
                                                url='/api/v1/cases/{}/ogs'.format(caseSystemId))
        kyc_headers['ACCESS-SIGN'] = sign
        kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        r = session.request('DELETE', url='{}/api/v1/cases/{}/ogs'.format(self.kyc_url, caseSystemId),
                            headers=kyc_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '' in r.text, "关闭特定KYC Case的持续性扫描错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_009 使用已经创建过的externalCaseId创建Kyc case')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_kyc_009(self):
        with allure.step("准备测试数据"):
            if get_json()['env'] == 'test':
                externalCaseId = 'weoEKFPJPzmhKnXSZTdinkyfJeehLS'
            elif get_json()['env'] == 'pro':
                externalCaseId = 'Y3WZCW0LxN8rDPDb3C1JifwbrA4Sxy'
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
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '"code":"001004"' in r.text, "使用已经创建过的externalCaseId创建Kyc case错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_010 使用不存在的caseSystemId寻找Kyc case')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_kyc_010(self):
        kyc_headers = self.kyc_headers
        unix_time = int(time.time())
        caseSystemId = "7829411a-955a-4ed0-b96c-729c63ea3009"
        sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                url='/api/v1/cases/{}'.format(caseSystemId))
        kyc_headers['ACCESS-SIGN'] = sign
        kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '"code":"001002"' in r.text, "使用不存在的caseSystemId寻找Kyc case错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_011 创建直接pending cases Kyc case后查询cases')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_011(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            kyc_headers = self.kyc_headers
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "INDIVIDUAL",
                "fullName": "James",
                "individualInfo": {"gender": "MALE"}
            }
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
            caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'PENDING' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_012 创建直接pass 企业 Kyc case后查询cases,最后发送接受结果信息')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_012(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            kyc_headers = self.kyc_headers
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "ORGANISATION",
                "fullName": "yilei bigone company",
                "organizationInfo": {
                    "registeredCountry": "CHN"
                }
            }
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
                caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='ScreenCompleted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='SuggestionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/reviewed', caseSystemId=caseSystemId,
                                               suggestion='SUGGEST_TO_ACCEPT')
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "ACCEPT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/api/v1/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/api/v1/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='ACCEPT',
                                               caseSystemId=caseSystemId)

    @allure.testcase('test_kyc_013 创建直接pass 企业 Kyc case后查询cases,最后发送不接受结果信息')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_013(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            kyc_headers = self.kyc_headers
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "ORGANISATION",
                "fullName": "yilei bigone company",
                "organizationInfo": {
                    "registeredCountry": "CHN"
                }
            }
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
                caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='ScreenCompleted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='SuggestionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/reviewed', caseSystemId=caseSystemId,
                                               suggestion='SUGGEST_TO_ACCEPT')
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认不接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "REJECT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/api/v1/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/api/v1/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='REJECT',
                                               caseSystemId=caseSystemId)

    @allure.testcase('test_kyc_014 创建直接pass TNS_STREET case后查询cases,最后发送接受结果信息')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_014(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            kyc_headers = self.kyc_headers
            data = {
                "externalCaseId":  externalCaseId,
                "fullName": "张飞",
                "screenType": "INDIVIDUAL",
                "memo": "1234123123",
                "businessCode": "TNS_TRADER"
            }
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
                caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='ScreenCompleted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='SuggestionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/reviewed', caseSystemId=caseSystemId,
                                               suggestion='SUGGEST_TO_ACCEPT')
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "ACCEPT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/api/v1/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/api/v1/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='ACCEPT',
                                               caseSystemId=caseSystemId)

    @allure.testcase('test_kyc_015 创建直接pass TNS_TRADER case后查询cases,最后发送接受结果信息')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_015(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            kyc_headers = self.kyc_headers
            data = {
                "externalCaseId":  externalCaseId,
                "fullName": "盛邦国际大厦",
                "screenType": "UNSPECIFIED",
                "memo": "1234123123",
                "businessCode": "TNS_STREET"
            }
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
                caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='ScreenCompleted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='SuggestionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/reviewed', caseSystemId=caseSystemId,
                                               suggestion='SUGGEST_TO_ACCEPT')
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "ACCEPT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/api/v1/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/api/v1/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='ACCEPT',
                                               caseSystemId=caseSystemId)

    @allure.testcase('test_kyc_016 创建直接pass TNS_BANK_ACCOUNT_NAME case后查询cases,最后发送接受结果信息')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_016(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            kyc_headers = self.kyc_headers
            data = {
                "externalCaseId":  externalCaseId,
                "fullName": "中国建设银行虹口支行",
                "screenType": "ORGANISATION",
                "memo": "1234123123",
                "businessCode": "TNS_BANK_NAME"
            }
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
                caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='ScreenCompleted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='SuggestionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/reviewed', caseSystemId=caseSystemId,
                                               suggestion='SUGGEST_TO_ACCEPT')
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "ACCEPT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/api/v1/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/api/v1/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='ACCEPT',
                                               caseSystemId=caseSystemId)

    @allure.testcase('test_kyc_017 创建直接pass TNS_BANK_NAME case后查询cases,最后发送接受结果信息')
    @pytest.mark.singleProcess
    @pytest.mark.pro
    def test_kyc_017(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("准备测试数据"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            kyc_headers = self.kyc_headers
            data = {
                "externalCaseId":  externalCaseId,
                "fullName": "Fei Zhang",
                "screenType": "UNSPECIFIED",
                "memo": "1234123123",
                "businessCode": "TNS_BANK_ACCOUNT_NAME"
            }
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/cases',
                                                    body=json.dumps(data))
        with allure.step("把数据写入headers"):
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
        with allure.step("创建Kyc case"):
            r = session.request('POST', url='{}/api/v1/cases'.format(self.kyc_url), data=json.dumps(data),
                                headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'PENDING' in r.text, "获取kyc-case信息错误，返回值是{}".format(r.text)
                caseSystemId = r.json()['caseSystemId']
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Submitted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='Created',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/pending', caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='ScreenCompleted',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='SuggestionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/reviewed', caseSystemId=caseSystemId,
                                               suggestion='SUGGEST_TO_ACCEPT')
        with allure.step("查询case结果"):
            unix_time = int(time.time())
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='GET',
                                                    url='/api/v1/cases/{}'.format(caseSystemId))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('GET', url='{}/api/v1/cases/{}'.format(self.kyc_url, caseSystemId), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert externalCaseId == r.json()['externalCaseId'], "获取case信息错误，返回值是{}".format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "ACCEPT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/api/v1/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            kyc_headers['ACCESS-SIGN'] = sign
            kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/api/v1/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='ACCEPT',
                                               caseSystemId=caseSystemId)





