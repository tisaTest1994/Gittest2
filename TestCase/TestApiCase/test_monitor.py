from Function.api_function import *
from run import *
from Function.log import *
import allure


# saving相关cases
class TestMonitorApi:

    # 初始化class
    def setup_class(self):
        AccountFunction.add_headers()

    @allure.testcase('test_monitor_001 创建case 并且查询')
    def test_monitor_001(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account='kimi.gong@cabital.com', password='123456',
                                                            type='monitor')
            headers['Authorization'] = "Bearer " + accessToken
            headers['Content-Type'] = 'application/json'
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook('test')
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
                "partnerId": "800b482d-0a88-480a-aae7-741f77a572f4"
            }
            r = session.request('POST', url='{}/operator/cases'.format(monitorUrl), data=json.dumps(data),
                                headers=headers)
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
            sleep_time = 0
            while sleep_time < 300:
                sleep_time = sleep_time + 30
                sleep(30)
                webhook_info = AccountFunction.get_webhook('test')
                for y in json.loads(webhook_info)['data']:
                    if y['e']['path'] == '/webhook/screen/case/pending':
                        sleep_time = 501
                        with allure.step("wehbook验签"):
                            webhook_sign = AccountFunction.make_access_sign(
                                unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'],
                                url=y['e']['path'], body=y['e']['bodyRaw'])
                            assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
        while sleep_time < 300:
            sleep_time = sleep_time + 30
            sleep(30)
            webhook_info = AccountFunction.get_webhook('test')
            for y in json.loads(webhook_info)['data']:
                if y['e']['path'] == '/webhook/compliance/operator' and 'SUGGEST_TO_ACCEPT' == y['e']['body']['suggestion']:
                    sleep_time = 501
                    with allure.step("wehbook验签"):
                        webhook_sign = AccountFunction.make_access_sign(
                            unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'],
                            url=y['e']['path'], body=y['e']['bodyRaw'])
                        assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
        with allure.step("查询创建的cases"):
            params = {
                'caseSystemId': caseSystemId
            }
            r = session.request('GET', url='{}/operator/cases/{}'.format(monitorUrl, r.json()['caseSystemId']),
                                params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['externalCaseId'] is not None, '查询kyc-case信息错误,返回值是{}'.format(r.text)
        with allure.step("查询创建的cases的audit log"):
            params = {
                'caseSystemId': caseSystemId
            }
            r = session.request('GET', url='{}/operator/cases/{}/audit'.format(monitorUrl, caseSystemId), params=params,
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'id' in r.text, '查询创建的cases的audit log错误,返回值是{}'.format(r.text)

    @allure.testcase('test_monitor_002 开启/关闭 ogs')
    def test_monitor_002(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account='kimi.gong@cabital.com', password='123456',
                                                            type='monitor')
            headers['Authorization'] = "Bearer " + accessToken
            headers['Content-Type'] = 'application/json'
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook('test')
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
                "partnerId": "800b482d-0a88-480a-aae7-741f77a572f4"
            }
            r = session.request('POST', url='{}/operator/cases'.format(monitorUrl), data=json.dumps(data),
                                headers=headers)
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
            r = session.request('POST', url='{}/operator/cases/{}/ogs'.format(monitorUrl, caseSystemId),
                                params=json.dumps(data), headers=headers)
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
            r = session.request('DELETE', url='{}/operator/cases/{}/ogs'.format(monitorUrl, caseSystemId),
                                params=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '' in r.text, '关闭ogs错误,返回值是{}'.format(r.text)

    @allure.testcase('test_monitor_003 创建case 给出系统建议')
    def test_monitor_003(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account='kimi.gong@cabital.com', password='123456',
                                                            type='monitor')
            headers['Authorization'] = "Bearer " + accessToken
            headers['Content-Type'] = 'application/json'
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook('test')
        with allure.step("创建case"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
            data = {
                "externalCaseId": externalCaseId,
                "screenType": "INDIVIDUAL",
                "fullName": "James",
                "individualInfo": {
                    "nationality": "USA",
                    "residentialCountry": "USA"
                },
                "organizationInfo": {
                    "registeredCountry": "USA"
                },
                "partnerId": "800b482d-0a88-480a-aae7-741f77a572f4"
            }
            r = session.request('POST', url='{}/operator/cases'.format(monitorUrl), data=json.dumps(data),
                                headers=headers)
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
            sleep_time = 0
            while sleep_time < 300:
                sleep_time = sleep_time + 30
                sleep(30)
                webhook_info = AccountFunction.get_webhook('test')
                for y in json.loads(webhook_info)['data']:
                    if y['e']['path'] == '/webhook/screen/case/pending':
                        sleep_time = 501
                        with allure.step("wehbook验签"):
                            webhook_sign = AccountFunction.make_access_sign(
                                unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'],
                                url=y['e']['path'], body=y['e']['bodyRaw'])
                            assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
        with allure.step("给出建议"):
            data = {
                "suggestion": "SUGGEST_TO_ACCEPT",
                "comment": ""
            }
            r = session.request('POST',
                                url='{}/operator/cases/{}/suggestion'.format(monitorUrl, r.json()['caseSystemId']),
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert {} == r.json(), '给出建议错误,返回值是{}'.format(r.text)

    @allure.testcase('test_monitor_004 创建case 没给出用户决策就reopen case失败')
    def test_monitor_004(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account='kimi.gong@cabital.com', password='123456',
                                                            type='monitor')
            headers['Authorization'] = "Bearer " + accessToken
            headers['Content-Type'] = 'application/json'
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook('test')
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
                "partnerId": "800b482d-0a88-480a-aae7-741f77a572f4"
            }
            r = session.request('POST', url='{}/operator/cases'.format(monitorUrl), data=json.dumps(data),
                                headers=headers)
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
            sleep_time = 0
            while sleep_time < 300:
                sleep_time = sleep_time + 30
                sleep(30)
                webhook_info = AccountFunction.get_webhook('test')
                for y in json.loads(webhook_info)['data']:
                    if y['e']['path'] == '/webhook/screen/case/reviewed' and 'SUGGEST_TO_ACCEPT' == y['e']['body']['suggestion']:
                        sleep_time = 501
                        with allure.step("wehbook验签"):
                            webhook_sign = AccountFunction.make_access_sign(
                                unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'],
                                url=y['e']['path'], body=y['e']['bodyRaw'])
                            assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
        while sleep_time < 300:
            sleep_time = sleep_time + 30
            sleep(30)
            webhook_info = AccountFunction.get_webhook('test')
            for y in json.loads(webhook_info)['data']:
                if y['e']['path'] == '/webhook/compliance/operator' and 'SUGGEST_TO_ACCEPT' == y['e']['body']['suggestion']:
                    sleep_time = 501
                    with allure.step("wehbook验签"):
                        webhook_sign = AccountFunction.make_access_sign(
                            unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'],
                            url=y['e']['path'], body=y['e']['bodyRaw'])
                        assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
        with allure.step("重启case"):
            r = session.request('POST', url='{}/operator/cases/{}/reopen'.format(monitorUrl, caseSystemId),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == '001003', '没给出用户决策就reopen case失败错误,返回值是{}'.format(r.text)

    @allure.testcase('test_monitor_005 创建case 给出用户决策后再reopen case')
    def test_monitor_005(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account='kimi.gong@cabital.com', password='123456',
                                                            type='monitor')
            headers['Authorization'] = "Bearer " + accessToken
            headers['Content-Type'] = 'application/json'
        with allure.step("删除旧的webhook"):
            AccountFunction.delete_old_webhook('test')
        with allure.step("创建case"):
            externalCaseId = generate_string(30)
            logger.info('externalCaseId是{}'.format(externalCaseId))
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
                },
                "partnerId": "800b482d-0a88-480a-aae7-741f77a572f4"
            }
            r = session.request('POST', url='{}/operator/cases'.format(monitorUrl), data=json.dumps(data),
                                headers=headers)
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
            sleep_time = 0
            while sleep_time < 300:
                sleep_time = sleep_time + 30
                sleep(30)
                webhook_info = AccountFunction.get_webhook('test')
                for y in json.loads(webhook_info)['data']:
                    if y['e']['path'] == '/webhook/screen/case/pending':
                        sleep_time = 501
                        with allure.step("wehbook验签"):
                            webhook_sign = AccountFunction.make_access_sign(
                                unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'],
                                url=y['e']['path'], body=y['e']['bodyRaw'])
                            assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
        with allure.step("给出建议"):
            data = {
                "suggestion": "SUGGEST_TO_ACCEPT",
                "comment": ""
            }
            r = session.request('POST',
                                url='{}/operator/cases/{}/suggestion'.format(monitorUrl, r.json()['caseSystemId']),
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert {} == r.json(), '给出建议错误,返回值是{}'.format(r.text)
        with allure.step("给予客户case决策"):
            data = {
                "decision": "ACCEPT",
                "comment": ""
            }
            r = session.request('POST', url='{}/operator/cases/{}/decision'.format(monitorUrl, caseSystemId), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, '给出用户决策错误,返回值是{}'.format(r.text)
        while sleep_time < 300:
            sleep_time = sleep_time + 30
            sleep(30)
            webhook_info = AccountFunction.get_webhook('test')
            for y in json.loads(webhook_info)['data']:
                if y['e']['path'] == '/webhook/screen/case/reviewed' and 'SUGGEST_TO_ACCEPT' == y['e']['body']['suggestion']:
                    sleep_time = 501
                    with allure.step("wehbook验签"):
                        webhook_sign = AccountFunction.make_access_sign(
                            unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'],
                            url=y['e']['path'], body=y['e']['bodyRaw'])
                        assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
        with allure.step("重启case"):
            r = session.request('POST', url='{}/operator/cases/{}/reopen'.format(monitorUrl, caseSystemId),
                                headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, 'reopen case错误,返回值是{}'.format(r.text)

