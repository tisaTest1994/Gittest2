import json

from Function.api_function import *
from Function.operate_sql import *


# saving相关cases
class TestMonitorApi:

    kyc_url = get_json()['kyc'][get_json()['env']]['kycUrl']
    kyc_headers = get_json()['kyc'][get_json()['env']]['kycHeaders']

    # 初始化
    def setup_method(self):
        self.kyc_headers['Authorization'] = "Bearer " + AccountFunction.get_account_token(account='kimi.gong@cabital.com', password=get_json()['kyc'][get_json()['env']]['password'], type='monitor')

    @allure.testcase('test_monitor_001 创建直接pass 个人 Kyc case后查询cases,最后发送接受结果信息')
    @pytest.mark.singleProcess
    def test_monitor_001(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("创建case"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "INDIVIDUAL",
                "fullName": "yuke zhang",
                "memo": "L++",
                "individualInfo": {
                    "gender": "MALE",
                    "dob": "1984-01-20",
                    "nationality": "USA",
                    "residentialCountry": "USA"
                },
                "organizationInfo": {
                    "registeredCountry": "USA"
                },
                "partnerId": get_json()['kyc'][get_json()['env']]['partnerId']
            }
            r = session.request('POST', url='{}/operator/cases'.format(get_json()['kyc'][get_json()['env']]['monitorUrl']), data=json.dumps(data),
                                headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['caseSystemId'] is not None, '获取kyc-case信息错误,返回值是{}'.format(r.text)
                assert r.json()['status'] == 'PENDING', "获取kyc-case信息错误，返回值是{}".format(r.text)
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
        with allure.step("查询创建的cases"):
            params = {
                'caseSystemId': caseSystemId
            }
            r = session.request('GET', url='{}/operator/cases/{}'.format(get_json()['kyc'][get_json()['env']]['monitorUrl'], r.json()['caseSystemId']), params=params, headers=self.kyc_headers)
            print(r.url)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['externalCaseId'] is not None, '查询kyc-case信息错误,返回值是{}'.format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "ACCEPT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/operator/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            self.kyc_headers['ACCESS-SIGN'] = sign
            self.kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)

            r = session.request('POST', url='{}/operator/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=self.kyc_headers)
            print(r.url)
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

    @allure.testcase('test_monitor_002 创建直接pass 个人 Kyc case后查询cases,最后发送不接受结果信息')
    @pytest.mark.singleProcess
    def test_monitor_002(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("创建case"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "INDIVIDUAL",
                "fullName": "yuke zhang",
                "individualInfo": {
                    "gender": "MALE",
                    "dob": "1984-01-20",
                    "nationality": "USA",
                    "residentialCountry": "USA"
                },
                "organizationInfo": {
                    "registeredCountry": "USA"
                },
                "partnerId": get_json()['kyc'][get_json()['env']]['partnerId']
            }
            r = session.request('POST', url='{}/operator/cases'.format(get_json()['kyc'][get_json()['env']]['monitorUrl']), data=json.dumps(data),
                                headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['caseSystemId'] is not None, '获取kyc-case信息错误,返回值是{}'.format(r.text)
                assert r.json()['status'] == 'PENDING', "获取kyc-case信息错误，返回值是{}".format(r.text)
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
        with allure.step("查询创建的cases"):
            params = {
                'caseSystemId': caseSystemId
            }
            r = session.request('GET', url='{}/operator/cases/{}'.format(get_json()['kyc'][get_json()['env']]['monitorUrl'], r.json()['caseSystemId']),
                                params=params, headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['externalCaseId'] is not None, '查询kyc-case信息错误,返回值是{}'.format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "REJECT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/operator/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            self.kyc_headers['ACCESS-SIGN'] = sign
            self.kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/operator/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认不接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='REJECT',
                                               caseSystemId=caseSystemId)

    @allure.testcase('test_monitor_003 开启/关闭 ogs')
    @pytest.mark.singleProcess
    def test_monitor_003(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("创建case"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "INDIVIDUAL",
                "fullName": "yuke zhang",
                "individualInfo": {
                    "gender": "MALE",
                    "dob": "1984-01-20",
                    "nationality": "USA",
                    "residentialCountry": "USA"
                },
                "organizationInfo": {
                    "registeredCountry": "USA"
                },
                "partnerId": get_json()['kyc'][get_json()['env']]['partnerId']
            }
            r = session.request('POST', url='{}/operator/cases'.format(get_json()['kyc'][get_json()['env']]['monitorUrl']), data=json.dumps(data),
                                headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['caseSystemId'] is not None, '获取kyc-case信息错误,返回值是{}'.format(r.text)
                assert r.json()['status'] == 'PENDING', "获取kyc-case信息错误，返回值是{}".format(r.text)
            caseSystemId = r.json()['caseSystemId']
        with allure.step("开启ogs"):
            data = {
                'caseSystemId': caseSystemId
            }
            r = session.request('POST', url='{}/operator/cases/{}/ogs'.format(get_json()['kyc'][get_json()['env']]['monitorUrl'], caseSystemId),
                                params=json.dumps(data), headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, '开启ogs错误,返回值是{}'.format(r.text)
        with allure.step("关闭ogs"):
            data = {
                'caseSystemId': caseSystemId
            }
            r = session.request('DELETE', url='{}/operator/cases/{}/ogs'.format(get_json()['kyc'][get_json()['env']]['monitorUrl'], caseSystemId),
                                params=json.dumps(data), headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, '关闭ogs错误,返回值是{}'.format(r.text)

    @allure.testcase('test_monitor_004 创建直接pass 个人 Kyc case后查询cases,最后发送接受结果信息再reopen case')
    @pytest.mark.singleProcess
    def test_monitor_004(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("创建case"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "INDIVIDUAL",
                "fullName": "yuke zhang",
                "individualInfo": {
                    "gender": "MALE",
                    "dob": "1984-01-20",
                    "nationality": "USA",
                    "residentialCountry": "USA"
                },
                "organizationInfo": {
                    "registeredCountry": "USA"
                },
                "partnerId": get_json()['kyc'][get_json()['env']]['partnerId']
            }
            print(self.kyc_headers)
            r = session.request('POST', url='{}/operator/cases'.format(get_json()['kyc'][get_json()['env']]['monitorUrl']), data=json.dumps(data),
                                headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['caseSystemId'] is not None, '获取kyc-case信息错误,返回值是{}'.format(r.text)
                assert r.json()['status'] == 'PENDING', "获取kyc-case信息错误，返回值是{}".format(r.text)
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
        with allure.step("查询创建的cases"):
            params = {
                'caseSystemId': caseSystemId
            }
            r = session.request('GET', url='{}/operator/cases/{}'.format(get_json()['kyc'][get_json()['env']]['monitorUrl'], r.json()['caseSystemId']),
                                params=params, headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['externalCaseId'] is not None, '查询kyc-case信息错误,返回值是{}'.format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
        with allure.step("发送确认接受结果信息"):
            unix_time = int(time.time())
            data = {
                "decision": "REJECT",
                "comment": "决策备注"
            }
            sign = AccountFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                    url='/operator/cases/{}/decision'.format(caseSystemId),
                                                    body=json.dumps(data))
            self.kyc_headers['ACCESS-SIGN'] = sign
            self.kyc_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            r = session.request('POST', url='{}/operator/cases/{}/decision'.format(self.kyc_url, caseSystemId),
                                data=json.dumps(data), headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, "发送确认不接受结果信息错误，返回值是{}".format(r.text)
        with allure.step("获取新的wehbook"):
            AccountFunction.check_webhook_info(path='/webhook/compliance/operator', action='DecisionUpdated',
                                               caseSystemId=caseSystemId)
            AccountFunction.check_webhook_info(path='/webhook/screen/case/completed', decision='REJECT',
                                               caseSystemId=caseSystemId)
        with allure.step("重启case"):
            r = session.request('POST', url='{}/operator/cases/{}/reopen'.format(get_json()['kyc'][get_json()['env']]['monitorUrl'], caseSystemId),
                                headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, 'reopen case错误,返回值是{}'.format(r.text)

    @allure.testcase('test_monitor_006 completed manually')
    @pytest.mark.singleProcess
    def test_monitor_006(self):
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook()
        with allure.step("创建case"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "INDIVIDUAL",
                "fullName": "yuke zhang",
                "memo": "L++",
                "individualInfo": {
                    "gender": "MALE",
                    "dob": "1984-01-20",
                    "nationality": "USA",
                    "residentialCountry": "USA"
                },
                "organizationInfo": {
                    "registeredCountry": "USA"
                },
                "partnerId": get_json()['kyc'][get_json()['env']]['partnerId']
            }
            r = session.request('POST', url='{}/operator/cases'.format(get_json()['kyc'][get_json()['env']]['monitorUrl']), data=json.dumps(data),
                                headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['caseSystemId'] is not None, '获取kyc-case信息错误,返回值是{}'.format(r.text)
                assert r.json()['status'] == 'PENDING', "获取kyc-case信息错误，返回值是{}".format(r.text)
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
        with allure.step("人工改变case status=completed manually"):
            data = {
                '': ''
            }
            r = session.request('PUT', url='{}/operator/cases/{}/screen/manually-complete'.format(get_json()['kyc'][get_json()['env']]['monitorUrl'], caseSystemId), data=json.dumps(data), headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("查询创建的cases"):
            params = {
                'caseSystemId': caseSystemId
            }
            r = session.request('GET', url='{}/operator/cases/{}'.format(get_json()['kyc'][get_json()['env']]['monitorUrl'], caseSystemId),
                                params=params, headers=self.kyc_headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['externalCaseId'] is not None, '查询kyc-case信息错误,返回值是{}'.format(r.text)
                assert 'WAITING_APPROVAL' == r.json()['status'], "获取case信息错误，返回值是{}".format(r.text)
