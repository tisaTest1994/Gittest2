import allure

from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api account deletion相关 testcases")
class TestAccountDeletionApi:

    # 初始化class
    @staticmethod
    def setup_method():
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_account_deletion_001')
    @allure.description('注册新账户，并查看销户申请状态为NOT_INIT')
    def test_account_deletion_001(self):
        account = generate_email()
        with allure.step("注册一个新账户"):
            ApiFunction.sign_up(account)
            logger.info('Email是：{}'.format(account))
        with allure.step("查看该账户的销户申请状态为NOT_INIT"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account,
                                                                                 password=get_json()['email'][
                                                                                     'password'], )
            r = session.request('GET', url='{}/account/writeoff/status'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['status'] == 'NOT_INIT', "销户状态错误，返回值是{}".format(r.text)

    @allure.title('test_account_deletion_002')
    @allure.description('提交注销申请，并查看销户申请状态为PENDING，用户状态为SUSPEND')
    def test_account_deletion_002(self):
        account = generate_email()
        with allure.step("注册一个新账户"):
            ApiFunction.sign_up(account)
            logger.info('Email是：{}'.format(account))
        with allure.step("查看该账户的销户申请状态为NOT_INIT"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account)
            r = session.request('GET', url='{}/account/writeoff/status'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['status'] == 'NOT_INIT', "销户状态错误，返回值是{}".format(r.text)

        with allure.step("提交销户申请，并查看销户申请状态为PENDING"):
            r = session.request('POST', url='{}/account/writeoff/applicant/submit'.format(env_url),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['status'] == 'PENDING', "销户状态错误，返回值是{}".format(r.text)
        with allure.step("查看用户状态为SUSPEND"):
            ApiFunction.get_account_status(email=account) == 'SUSPEND', "用户状态不对，目前状态是{}".format(
                r.status_code)

    @allure.title('test_account_deletion_003')
    @allure.description('重复提交注销申请报错，并查看销户申请状态为PENDING，用户状态为SUSPEND')
    def test_account_deletion_003(self):
        with allure.step("提交销户申请"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account="winnie.wang+121@cabital.com",
                                                                                 password="A!234sdfg")
            r = session.request('POST', url='{}/account/writeoff/applicant/submit'.format(env_url),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] == '001036', "销户申请状态错误，返回值是{}".format(r.text)
        with allure.step("查看用户状态为SUSPEND"):
            ApiFunction.get_account_status(email="winnie.wang+121@cabital.com") == 'SUSPEND', "用户状态不对，目前状态是{}".format(
                r.status_code)

    @allure.title('test_account_deletion_004')
    @allure.description('提交销户申请后审批通过，查看用户状态为CLOSED')
    def test_account_deletion_004(self):
        account = generate_email()
        with allure.step("注册一个新账户"):
            ApiFunction.sign_up(account)
            logger.info('Email是：{}'.format(account))
        with allure.step("提交销户申请，并查看销户申请状态为PENDING"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account)
            r = session.request('POST', url='{}/account/writeoff/applicant/submit'.format(env_url),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['status'] == 'PENDING', "销户状态错误，返回值是{}".format(r.text)
        with allure.step("修改用户状态为CLOSED"):
            user_id = ApiFunction.get_user_id(email=account)
            logger.info('user_id是：{}'.format(user_id))
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['operate_admin_account']['email'],
                password=get_json()['operate_admin_account']['password'], type='operate')
            data = {
                "toModifyList": [
                    {
                        "type": "ACCOUNT_STATUS",
                        "value": "CLOSED"
                    }
                ]
            }
            r = session.request('PUT', url='{}/operator/operator/users/update/{}'.format(operateUrl, user_id),
                                data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("销户申请审批通过"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['operate_admin_account']['email'],
                password=get_json()['operate_admin_account']['password'], type='operate')
            data = {
                "status": "APPROVED"
            }
            r = session.request('POST', url='{}/operator/operator/writeoff/{}/callback'.format(operateUrl, user_id),
                                data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("查看用户状态为CLOSED"):
            status = ApiFunction.get_account_status(user_id=user_id)
        with allure.step("校验用户状态"):
            assert status == 'CLOSED', "用户状态不对，目前状态是{}".format(r.status_code)

    @allure.title('test_account_deletion_005')
    @allure.description('新用户提交销户申请后审批拒绝，查看用户状态为NEW')
    def test_account_deletion_005(self):
        account = generate_email()
        with allure.step("注册一个新账户"):
            ApiFunction.sign_up(account)
            logger.info('Email是：{}'.format(account))
        with allure.step("提交销户申请，并查看销户申请状态为PENDING"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account)
            r = session.request('POST', url='{}/account/writeoff/applicant/submit'.format(env_url),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['status'] == 'PENDING', "销户状态错误，返回值是{}".format(r.text)
        with allure.step("销户申请审批拒绝"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['operate_admin_account']['email'],
                password=get_json()['operate_admin_account']['password'], type='operate')
            data = {
                "status": "REJECTED"
            }
            user_id = ApiFunction.get_user_id(email=account)
            logger.info('user_id是：{}'.format(user_id))
            r = session.request('POST', url='{}/operator/operator/writeoff/{}/callback'.format(operateUrl, user_id),
                                data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("查看用户状态为NEW"):
            status = ApiFunction.get_account_status(user_id=user_id)
        with allure.step("校验用户状态"):
            assert status == 'NEW', "用户状态不对，目前状态是{}".format(r.status_code)

    @allure.title('test_account_deletion_006')
    @allure.description('ACTIVE用户提交销户申请后审批拒绝，查看用户状态为ACTIVE')
    def test_account_deletion_006(self):
        with allure.step("提交销户申请，并查看销户申请状态为PENDING"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account="winnie.wang+125@cabital.comm",
                                                                                 password="A!234sdfg")
            r = session.request('POST', url='{}/account/writeoff/applicant/submit'.format(env_url),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['status'] == 'PENDING', "销户状态错误，返回值是{}".format(r.text)
        with allure.step("销户申请审批拒绝"):
            user_id = "20f336f6-7dbd-48b5-953b-2d805593448f"
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['operate_admin_account']['email'],
                password=get_json()['operate_admin_account']['password'], type='operate')
            data = {
                "status": "REJECTED"
            }
            r = session.request('POST', url='{}/operator/operator/writeoff/{}/callback'.format(operateUrl, user_id),
                                data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("查看用户状态为ACTIVE"):
                status = ApiFunction.get_account_status(user_id=user_id)
            with allure.step("校验用户状态"):
                assert status == 'ACTIVE', "用户状态不对，目前状态是{}".format(r.status_code)
