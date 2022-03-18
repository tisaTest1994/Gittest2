from Function.api_function import *
from Function.operate_sql import *


# operate相关cases
class TestCabinetAccountApi:

    # 初始化class
    def setup_method(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')

    @allure.title('test_cabinet_account_001 用户修改邮箱')
    def test_cabinet_account_001(self):
        with allure.step("用户修改邮箱"):
            user_id = "a4d5006b-c036-42dc-8f77-b8d7baedd442"
            account = generate_email()
            logger.info('新的email是{}'.format(account))
            data = {
                "email": account
            }
            r = session.request('PUT', url='{}/operator/operator/users/{}/email'.format(operateUrl, user_id),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "用户修改邮箱错误，返回值是{}".format(r.text)

    @allure.title('test_cabinet_account_002 用户使用已经注册的邮箱修改邮箱')
    def test_cabinet_account_002(self):
        with allure.step("用户修改邮箱"):
            user_id = "a4d5006b-c036-42dc-8f77-b8d7baedd442"
            data = {
                "email": 'yilei4@163.com'
            }
            r = session.request('PUT', url='{}/operator/operator/users/{}/email'.format(operateUrl, user_id),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BAD_REQUEST' == r.json()['code'], "用户使用已经注册的邮箱修改邮箱错误，返回值是{}".format(r.text)
            assert 'The email address has been registered.' == r.json()['message'], "用户使用已经注册的邮箱修改邮箱错误，返回值是{}".format(r.text)

    @allure.title('test_cabinet_account_003 用户使用未找到的user_id修改绑定邮箱')
    def test_cabinet_account_003(self):
        with allure.step("用户修改邮箱"):
            user_id = "a4d5006b-c036-42dc-8f77-b8d7baedd44212"
            data = {
                "email": generate_email()
            }
            r = session.request('PUT', url='{}/operator/operator/users/{}/email'.format(operateUrl, user_id),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BAD_REQUEST' == r.json()['code'], "用户使用未找到的user_id修改绑定邮箱错误，返回值是{}".format(r.text)
            assert 'User not exist.' == r.json()['message'], "用户使用未找到的user_id修改绑定邮箱错误，返回值是{}".format(r.text)

    @allure.title('test_cabinet_account_004 未找到关闭用户otp')
    def test_cabinet_account_004(self):
        with allure.step("未找到关闭用户otp"):
            user_id = "a4d5006b-c036-42dc-8f77-b8d7baedd44212"
            data = {
                "type": "OTP"
            }
            r = session.request('POST', url='{}/operator/operator/users/{}/mfa/reset'.format(operateUrl, user_id),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BAD_REQUEST' == r.json()['code'], "未找到关闭用户otp错误，返回值是{}".format(r.text)
            assert 'To protect your account, you have to enable Two-Factor Authentication(2FA).' == r.json()['message'], "未找到关闭用户otp错误，返回值是{}".format(r.text)

    @allure.title('test_cabinet_account_005 关闭用户otp')
    def test_cabinet_account_005(self):
        with allure.step("用户修改邮箱"):
            user_id = "a4d5006b-c036-42dc-8f77-b8d7baedd442"
            account = generate_email()
            logger.info('新的email是{}'.format(account))
            data = {
                "email": account
            }
            session.request('PUT', url='{}/operator/operator/users/{}/email'.format(operateUrl, user_id),
                            data=json.dumps(data), headers=headers)
        with allure.step("绑定otp"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account)
            r = session.request('GET', url='{}/account/security/mfa/otp/qrcode'.format(env_url), headers=headers)
            if "SUCCESS" in r.text:
                secretData = r.json()['totpSecret']
                secretKey = r.json()['uriParams']['secret']
                # 写入secretKey
                logger.info('secretKey是{}'.format(secretKey))
                totp = pyotp.TOTP(secretKey)
                mfaVerificationCode = totp.now()
                data = {
                    "secretData": str(secretData),
                    "mfaVerificationCode": str(mfaVerificationCode),
                    "userLabel": "account",
                    "emailVerificationCode": "666666"
                }
                session.request('POST', url='{}/account/security/mfa/otp/enable'.format(env_url),
                                data=json.dumps(data), headers=headers)
        with allure.step("关闭otp"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['operate_admin_account']['email'],
                password=get_json()['operate_admin_account']['password'], type='operate')
            user_id = "a4d5006b-c036-42dc-8f77-b8d7baedd442"
            data = {
                "type": "OTP"
            }
            r = session.request('POST', url='{}/operator/operator/users/{}/mfa/reset'.format(operateUrl, user_id),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "关闭用户otp错误，返回值是{}".format(r.text)
