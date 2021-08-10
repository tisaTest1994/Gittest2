from Function.api_function import *
from run import *
from Function.log import *
import allure


# operate相关cases
class TestOperateApi:

    @allure.testcase('test_operate_001 管理员账户登录')
    def test_operate_001(self):
        account = get_json()['operate_admin_account']
        data = {
            "username": account['email'],
            "password": account['password']
        }
        r = session.request('POST', url='{}/operator/operator/login'.format(operateUrl), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "管理员账户登录错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_002 检索用户')
    def test_operate_002(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "accountId": email['accountId'],
            "status": "ACTIVE",
            "email": email['email'],
            "userId": email['userId'],
            "pagination": {
                "pageNo": 1,
                "pageSize": 10
            },
            "sort": {
                "field": "updatedAt",
                "order": "asc"
            }
        }
        r = session.request('POST', url='{}/operator/operator/users/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['accounts'] is not None, '检索用户失败，返回值是{}'.format(r.text)

    @allure.testcase('test_operate_003 管理员查询用户信息')
    def test_operate_003(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        r = session.request('GET', url='{}/operator/operator/user/info/{}'.format(operateUrl, email['userId']), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'user' in r.text, "管理员查询用户信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_004 管理员刷新token')
    def test_operate_004(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        r = session.request('GET', url='{}/operator/operator/user/info/{}'.format(operateUrl, email['userId']), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'user' in r.text, "管理员查询用户信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_005 检索cases')
    def test_operate_005(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "userId": email["userId"],
            "status": "COMPLETE",
            "caseId": "",
            "pagination": {
                "pageNo": 1,
                "pageSize": 5
            },
            "sort": {
                "field": "submittedTime",
                "order": "desc"
            }
        }
        r = session.request('POST', url='{}/operator/operator/cases/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'caseList' in r.text, "检索cases错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_006 获取cases详情')
    def test_operate_006(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获得cases id"):
            data = {
                "userId": email["userId"],
                "status": "COMPLETE",
                "caseId": "",
                "pagination": {
                    "pageNo": 1,
                    "pageSize": 5
                },
                "sort": {
                    "field": "submittedTime",
                    "order": "desc"
                }
            }
            r = session.request('POST', url='{}/operator/operator/cases/search'.format(operateUrl), data=json.dumps(data),
                                headers=headers)
            case_id = random.choice(r.json()['caseList'])['caseId']
            logger.info('case_id是{}'.format(case_id))
        r = session.request('GET', url='{}/operator/operator/case/{}/detail'.format(operateUrl, case_id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'individualInfo' in r.text, "检索cases错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_007 检索payin交易')
    def test_operate_007(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "amount",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/payin/search'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'pagination_response' in r.text, "检索payin交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_008 检索payin交易明细')
    def test_operate_008(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "amount",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/payin/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        logger.info('payin信息{}'.format(r.text))
        transaction_id = random.choice(r.json()['transactions'])['transaction_id']
        with allure.step("查询payin具体信息"):
            r = requests.request('GET', url='{}/operatorapi/txns/payin/{}'.format(operateUrl, transaction_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'order_id' in r.text, "检索payin交易明细错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_009 检索cfx交易')
    def test_operate_009(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/cfx/search'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'pagination_response' in r.text, "检索cfx交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_010 检索cfx交易明细')
    def test_operate_010(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/cfx/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        logger.info('payin信息{}'.format(r.text))
        transaction_id = random.choice(r.json()['transactions'])['transaction_id']
        with allure.step("检索cfx交易明细"):
            r = requests.request('GET', url='{}/operatorapi/txns/cfx/{}'.format(operateUrl, transaction_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'pair' in r.text, "检索cfx交易明细错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_011 检索payout交易')
    def test_operate_011(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "amount",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/payout/search'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'pagination_response' in r.text, "检索payout交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_012 检索payout交易明细')
    def test_operate_012(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "amount",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/payout/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        logger.info('payin信息{}'.format(r.text))
        transaction_id = random.choice(r.json()['transactions'])['transaction_id']
        with allure.step("查询payin具体信息"):
            r = requests.request('GET', url='{}/operatorapi/txns/payout/{}'.format(operateUrl, transaction_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'request_by' in r.text, "检索payout交易明细错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_013 检索earn交易')
    def test_operate_013(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/earn/search'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'record_count' in r.text, "检索earn交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_014 检索earn交易明细')
    def test_operate_014(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/payin/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        logger.info('payin信息{}'.format(r.text))
        transaction_id = random.choice(r.json()['transactions'])['transaction_id']
        with allure.step("检索earn交易明细"):
            r = requests.request('GET', url='{}/operatorapi/txns/payin/{}'.format(operateUrl, transaction_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'order_id' in r.text, "检索earn交易明细错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_015 检索interest交易')
    def test_operate_015(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/interest/search'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'record_count' in r.text, "检索interest交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_016 检索interest交易明细')
    def test_operate_016(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/interest/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        logger.info('interest信息{}'.format(r.text))
        interests_id = random.choice(r.json()['interests'])['interest_id']
        with allure.step("检索earn交易明细"):
            r = requests.request('GET', url='{}/operatorapi/txns/interest/{}'.format(operateUrl, interests_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'interest_id' in r.text, "检索earn交易明细错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_017 检索yield')
    def test_operate_017(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/yield/search'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'record_count' in r.text, "检索yield交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_018 检索yield交易明细')
    def test_operate_018(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/yield/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        logger.info('yield信息{}'.format(r.text))
        yield_id = random.choice(r.json()['yields'])['yield_id']
        with allure.step("检索yield交易明细"):
            r = requests.request('GET', url='{}/operatorapi/txns/yield/{}'.format(operateUrl, yield_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'yield_id' in r.text, "检索yield交易明细错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_019 检索payout')
    def test_operate_019(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/payout/search'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'crypto_account' in r.text, "检索payout交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_020 检索payout交易明细')
    def test_operate_020(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/txns/payout/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        logger.info('payout信息{}'.format(r.text))
        transaction_id = random.choice(r.json()['transactions'])['transaction_id']
        with allure.step("检索yield交易明细"):
            r = requests.request('GET', url='{}/operatorapi/txns/payout/{}'.format(operateUrl, transaction_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'transaction_id' in r.text, "检索yield交易明细错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_021 检索payin order')
    def test_operate_021(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/orders/payin/search'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'crypto_account' in r.text, "检索payout交易错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_022 检索payin order交易明细')
    def test_operate_022(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 30
            },
            "sort_request": {
                "field": "created_at",
                "order": "desc"
            }
        }
        r = requests.request('POST', url='{}/operatorapi/orders/payin/search'.format(operateUrl), data=json.dumps(data), headers=headers)
        logger.info('payin order信息{}'.format(r.text))
        order_id = random.choice(r.json()['orders'])['order_id']
        with allure.step("检索yield交易明细"):
            r = requests.request('GET', url='{}/operatorapi/orders/payin/{}'.format(operateUrl, order_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'order_id' in r.text, "检索payin order交易明细错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_023 检索活期产品')
    def test_operate_023(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "productSubType": 2
        }
        r = requests.request('POST', url='{}/operatorapi/products'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'product_uuid' in r.text, "检索活期产品错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_024 检索定期产品')
    def test_operate_024(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
            "productSubType": 1
        }
        r = requests.request('POST', url='{}/operatorapi/products'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'product_uuid' in r.text, "检索定期产品错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_025 检索所有产品')
    def test_operate_025(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
        }
        r = requests.request('POST', url='{}/operatorapi/products'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'product_uuid' in r.text, "检索所有产品错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_026 获得wallet')
    def test_operate_026(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        params = {
            "account_id": '96f29441-feb4-495a-a531-96c833e8261a'
        }
        r = requests.request('GET', url='{}/operatorapi/wallets'.format(operateUrl), params=params, headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['Wallets'] is not None, "获得wallet错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_027 wallet调整余额内部户转到客户账户失败')
    def test_operate_027(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
                "debit_wallet_id": "e37e7c9e-95f6-11eb-84c0-067d526cf950",
                "credit_wallet_id": "bd6608b9-81be-4260-ae8a-6726f8eabddd",
                "amount": "100",
                "txn_type": "adjustment",
        }
        r = requests.request('POST', url='{}/operatorapi/wallets/balance/adjust'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['is_succeed'] is False, "wallet调整余额内部户转到客户账户失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_028 wallet调整余额客户转到内部户账户失败')
    def test_operate_028(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
                "debit_wallet_id": "bd6608b9-81be-4260-ae8a-6726f8eabddd",
                "credit_wallet_id": "e37e7c9e-95f6-11eb-84c0-067d526cf950",
                "amount": "100",
                "txn_type": "adjustment",
        }
        r = requests.request('POST', url='{}/operatorapi/wallets/balance/adjust'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['is_succeed'] is False, "wallet调整余额客户转到内部户账户失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_029 wallet调整余额内部户账户到内部户账户')
    def test_operate_029(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
                "debit_wallet_id": "77c65bcc-d40b-11eb-8e66-0a3898443cb8",
                "credit_wallet_id": "e37e7c9e-95f6-11eb-84c0-067d526cf950",
                "amount": "0.5",
                "txn_type": "adjustment",
        }
        with allure.step("从数据库获得转账前的balance"):
            sql_payout = "select amount from balance where type='1' and wallet_id=(select id from wallet.wallet where wallet_id='{}');".format(data['debit_wallet_id'])
            sql_payin = "select amount from balance where type='1' and wallet_id=(select id from wallet.wallet where wallet_id='{}');".format(data['credit_wallet_id'])
            payout_amount_old = sqlFunction.connect_mysql('wallet', sql_payout)[0]['amount']
            payin_amount_old = sqlFunction.connect_mysql('wallet', sql_payin)[0]['amount']
        r = requests.request('POST', url='{}/operatorapi/wallets/balance/adjust'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['is_succeed'] is True, "wallet调整余额内部户账户到内部户账户错误，返回值是{}".format(r.text)
        with allure.step("从数据库获得转账后的balance"):
            payout_amount_new = sqlFunction.connect_mysql('wallet', sql_payout)[0]['amount']
            payin_amount_new = sqlFunction.connect_mysql('wallet', sql_payin)[0]['amount']
        assert float(payout_amount_old) - 0.5 == float(payout_amount_new), 'wallet调整余额内部户账户到内部户账户错误，payout_amount_old是{}, payout_amount_new是{}'.format(payout_amount_old, payout_amount_new)
        assert float(payin_amount_old) - 0.5 == float(
            payin_amount_old), 'wallet调整余额内部户账户到内部户账户错误，payout_amount_old是{}, payout_amount_new是{}'.format(
            payout_amount_old, payin_amount_new)

    @allure.testcase('test_operate_030 wallet调整余额内部户CA账户到内部户账户需要传入counterparty_txn_id失败')
    def test_operate_030(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
                "debit_wallet_id": "77c0b45d-d40b-11eb-8e66-0a3898443cb8",
                "credit_wallet_id": "77bf824e-d40b-11eb-8e66-0a3898443cb8",
                "amount": "0.5",
                "txn_type": "adjustment",
        }
        r = requests.request('POST', url='{}/operatorapi/wallets/balance/adjust'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['is_succeed'] is False, "wallet调整余额内部户CA账户到内部户账户需要传入counterparty_txn_id失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_031 wallet调整余额内部户eth转btc失败')
    def test_operate_031(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
                "debit_wallet_id": "77b5c78e-d40b-11eb-8e66-0a3898443cb8",
                "credit_wallet_id": "77b9f6b9-d40b-11eb-8e66-0a3898443cb8",
                "amount": "0.5",
                "txn_type": "adjustment",
        }
        r = requests.request('POST', url='{}/operatorapi/wallets/balance/adjust'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['is_succeed'] is False, "wallet调整余额内部户eth转btc失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_operate_032 wallet调整余额内部户CA账户到内部户账户需要传入counterparty_txn_id')
    def test_operate_032(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=get_json()['operate_admin_account']['email'], password=get_json()['operate_admin_account']['password'], type='operate')
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        data = {
                "debit_wallet_id": "77c0b45d-d40b-11eb-8e66-0a3898443cb8",
                "credit_wallet_id": "77bf824e-d40b-11eb-8e66-0a3898443cb8",
                "amount": "0.5",
                "txn_type": "adjustment",
                "value_date": "2021/08/05 19:21:59",
                "counterparty_txn_id": "7698c69e-a8bc-4429-ae07-a08312264118fd"
        }
        r = requests.request('POST', url='{}/operatorapi/wallets/balance/adjust'.format(operateUrl), data=json.dumps(data), headers=headers, timeout=100)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['is_succeed'] is True, "wallet调整余额内部户CA账户到内部户账户需要传入counterparty_txn_id错误，返回值是{}".format(r.text)