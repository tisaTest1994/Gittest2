import allure

from Function.api_function import *
from Function.operate_sql import *


@allure.feature("account 相关 testcases")
class TestAccountApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_account_001 成功注册新用户')
    def test_account_001(self):
        with allure.step("注册新用户"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "666666",
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "注册新用户失败，返回值是{}".format(r.text)
            assert r.json()['refreshExpiresTn'] == 86400, "token过期时间不是24小时，返回值是{}".format(r.text)

    @allure.title('test_account_002 注册用户时，用户已经存在（正常流程不会存在此问题）')
    def test_account_002(self):
        account = generate_email()
        with allure.step("提前先注册好"):
            ApiFunction.sign_up(account)
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
        with allure.step("注册"):
            data = {
                "emailAddress": account,
                "verificationCode": "666666",
                "citizenCountryCode": citizenCountryCode,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Registration failed. Please contact our customer service if the problem persists.' in r.text, "用户已经存在错误，返回值是{}".format(r.text)

    @allure.title('test_account_003 注册时，输入错误验证码导致注册失败')
    def test_account_003(self):
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "166666",
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'The verification code was wrong' in r.text, "注册时，输入错误验证码导致注册失败，返回值是{}".format(r.text)

    @allure.title('test_account_007 登录已经注册账号')
    def test_account_007(self):
        account = get_json()['email']['email']
        with allure.step("登录已经注册账号"):
            data = {
                "username": account,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "登录已经注册账号错误，返回值是{}".format(r.text)

    @allure.title('test_account_009 登录未注册账号')
    def test_account_009(self):
        with allure.step("登录未注册账号"):
            data = {
                "username": generate_email(),
                "password": "A!2123123"
            }
            r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 404, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Incorrect account or password.' in r.text, "登录已经注册账号输入错误密码错误，返回值是{}".format(r.text)

    @allure.title('test_account_010 登录已经注册的黑名单账号')
    def test_account_010(self):
        with allure.step("登录已经注册的黑名单账号"):
            blacklist = get_json()['blacklist']
            data = {
                "username": blacklist['email'],
                "password": blacklist['password']
            }
            r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "登录已经注册的黑名单账号错误，返回值是{}".format(r.text)

    @allure.title('test_account_011 刷新账户token')
    def test_account_011(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token()
        with allure.step("获取refreshToken"):
            data = {
                "username": get_json()['email']['email'],
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data), headers=headers)
            refreshToken = r.json()['refreshToken']
            print(headers['Authorization'])
        with allure.step("刷新tokne"):
            data = {
                "refreshToken": refreshToken
            }
            r = session.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "刷新账户token错误，返回值是{}".format(r.text)

    @allure.title('test_account_012 用错误的token刷新token')
    def test_account_012(self):
        with allure.step("用错误的token刷新token"):
            data = {
                "refreshToken": "123"
            }
            r = session.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 401, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Refresh token error' in r.text, "用错误的token刷新token错误，返回值是{}".format(r.text)

    @allure.title('test_account_013 用空的token刷新token')
    def test_account_013(self):
        with allure.step("用空的token刷新token"):
            data = {
                "refreshToken": ""
            }
            r = session.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid refresh token' in r.text, "用空的token刷新token错误，返回值是{}".format(r.text)

    @allure.title('test_account_018 忘记密码')
    def test_account_018(self):
        with allure.step("忘记密码"):
            account = generate_email()
            password = get_json()['email']['password']
            with allure.step("提前先注册好"):
                ApiFunction.sign_up(account, password)
            data = {
                "code": "666666",
                "email": account,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/forgetPassword'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "忘记密码错误，返回值是{}".format(r.text)

    @allure.title('test_account_019 未注册用户忘记密码失败')
    def test_account_019(self):
        with allure.step("未注册用户忘记密码失败"):
            data = {
                "code": "666666",
                "email": generate_email(),
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/forgetPassword'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "The verification code was wrong." in r.text, "未注册用户忘记密码失败错误，返回值是{}".format(r.text)

    @allure.title('test_account_020 用户忘记密码验证码错误')
    def test_account_020(self):
        with allure.step("用户忘记密码验证码错误"):
            account = generate_email()
            password = get_json()['email']['password']
            with allure.step("提前先注册好"):
                ApiFunction.sign_up(account, password)
        with allure.step("用户忘记密码验证码错误"):
            data = {
                "code": "166666",
                "email": account,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/forgetPassword'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "The verification code was wrong." in r.text, "用户忘记密码验证码错误错误，返回值是{}".format(r.text)

    @allure.title('test_account_021 查询用户信息')
    def test_account_021(self):
        with allure.step("查询用户信息"):
            r = session.request('GET', url='{}/account/info'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['user']['userId'] is not None, "查询用户信息错误，返回值是{}".format(r.text)

    @allure.title('test_account_023 用户使用特殊符号注册')
    def test_account_023(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
        with allure.step("注册"):
            data = {
                "emailAddress": '%$#{}@dsadda.com'.format(generate_number(8)),
                "verificationCode": "666666",
                "citizenCountryCode": citizenCountryCode,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "用户使用特殊符号注册错误，返回值是{}".format(r.text)

    @allure.title('test_account_024 注册用户验证码缺少位数输入')
    def test_account_024(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "16666",
                "citizenCountryCode": citizenCountryCode,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid verification code' in r.text, "注册用户验证码缺少位数输入错误，返回值是{}".format(r.text)

    @allure.title('test_account_025 注册用户验证码输入字符')
    def test_account_025(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "dqwdqwd",
                "citizenCountryCode": citizenCountryCode,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid verification code' in r.text, "注册用户验证码输入字符错误，返回值是{}".format(r.text)

    @allure.title('test_account_028 获取opt二维码')
    def test_account_028(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yilei1@163.com')
        r = session.request('GET', url='{}/account/security/mfa/otp/qrcode'.format(env_url), headers=headers)
        ApiFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['totpSecret'] is not None, "获取opt二维码不对，目前返回值是{}".format(r.text)

    @allure.title('test_account_029 创建opt验证，并且删除。')
    def test_account_029(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yilei3@163.com')
        # 获得opt secretKey
        r = session.request('GET', url='{}/account/security/mfa/otp/qrcode'.format(env_url), headers=headers)
        print(r.text)
        if '001018' in r.text:
            # 删除opt
            secretKey = get_json()['secretKeyForTest']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            data = {
                "mfaVerificationCode": str(mfaVerificationCode),
                "emailVerificationCode": "666666"
            }
            session.request('POST', url='{}/account/security/mfa/otp/disable'.format(env_url), data=json.dumps(data), headers=headers)
            write_json('secretKeyForTest', ' ')
        else:
            r = session.request('GET', url='{}/account/security/mfa/otp/qrcode'.format(env_url), headers=headers)
        if r.status_code == 200:
            secretData = r.json()['totpSecret']
            secretKey = r.json()['uriParams']['secret']
            # 写入secretKey
            logger.info('secretKey是{}'.format(secretKey))
            write_json('secretKeyForTest', secretKey)
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            data = {
                "secretData": str(secretData),
                "mfaVerificationCode": str(mfaVerificationCode),
                "userLabel": "account",
                "emailVerificationCode": "666666"
            }
            r = session.request('POST', url='{}/account/security/mfa/otp/enable'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert {} == r.json(), "创建opt验证不对，目前返回值是{}".format(r.text)
        with allure.step("删除opt"):
            secretKey = get_json()['secretKeyForTest']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            data = {
                "mfaVerificationCode": str(mfaVerificationCode),
                "emailVerificationCode": "666666"
            }
            session.request('POST', url='{}/account/security/mfa/otp/disable'.format(env_url), data=json.dumps(data), headers=headers)
            write_json('secretKeyForTest', ' ')

    @allure.title('test_account_030 验证opt code')
    def test_account_030(self):
        # 验证opt code
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='external.qa@cabital.com')
        secretKey = get_json()['secretKey']
        totp = pyotp.TOTP(secretKey)
        mfaVerificationCode = totp.now()
        data = {
            "totp": str(mfaVerificationCode)
        }
        r = session.request('POST', url='{}/account/security/mfa/otp/verify'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), " 验证opt code不对，目前返回值是{}".format(r.text)

    @allure.title('test_account_031 接受隐私政策版本')
    def test_account_031(self):
        data = {
            "privacyPolicyVersion": 20210528,
            "termOfServiceVersion": 20210528
        }
        r = session.request('POST', url='{}/account/setting/privacy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "接受隐私政策版本不对，目前返回值是{}".format(r.text)

    @allure.title('test_account_032 查询最新隐私政策版本')
    def test_account_032(self):
        r = session.request('GET', url='{}/account/privacy/latest'.format(env_url), headers=headers)
        data = {
            "privacyPolicyVersion": r.json()['privacyPolicyVersion'],
            "termOfServiceVersion": r.json()['termOfServiceVersion']
        }
        session.request('POST', url='{}/account/setting/privacy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'privacyPolicyVersion' in r.text, "查询最新隐私政策版本不对，目前返回值是{}".format(r.text)
            # 查询用户信息
            r1 = session.request('GET', url='{}/account/info'.format(env_url), headers=headers)
            assert r.json()['privacyPolicyVersion'] == r1.json()['user']['userPrivacyPolicy']['privacyPolicyVersion'], 'privacyPolicyVersion最新版本和个人接受版本不匹配'
            assert r.json()['termOfServiceVersion'] == r1.json()['user']['userPrivacyPolicy']['termOfServiceVersion'], 'termOfServiceVersion最新版本和个人接受版本不匹配'

    @allure.title('test_account_034 注册时，多输入几位验证码导致注册失败')
    def test_account_034(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "1366666",
                "citizenCountryCode": citizenCountryCode,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid verification code' in r.text, "注册时，输入错误验证码导致注册失败，返回值是{}".format(r.text)

    @allure.title('test_account_035 获得邀请人数和奖励')
    def test_account_035(self):
        with allure.step("获得邀请人数和奖励"):
            r = session.request('GET', url='{}/recruit/referal/referees'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'count' in r.json().keys(), "获得邀请人数和奖励失败，返回值是{}".format(r.text)

    @allure.title('test_account_036 获得邀请码和链接')
    def test_account_036(self):
        with allure.step("获得邀请人数和奖励"):
            r = session.request('GET', url='{}/recruit/referal/code'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] is not None, "获得邀请人数和奖励失败，返回值是{}".format(r.text)

    @allure.title('test_account_037 referal注册用户')
    def test_account_037(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(get_json()['citizenCountryCodeList'])
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "666666",
                "citizenCountryCode": citizenCountryCode,
                "password": get_json()['email']['password'],
                "metadata": {
                    "referral": {
                    "code": "6EM7LK"
                    }
                }
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
            sleep(2)
            logger.info('邮箱是{}'.format(data['emailAddress']))
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'accessToken' in r.text, "注册新用户失败，返回值是{}".format(r.text)
        with allure.step("数据库检查"):
            sql = "select relation from relation where referer_id='96f29441-feb4-495a-a531-96c833e8261a' and referee_id=(select account_id from account.user_account_map where user_id = (select user_id from account.user where email='{}'));".format(data['emailAddress'])
            relation = sqlFunction.connect_mysql('referral', sql)
            assert relation[0]['relation'] == 1, '数据库查询值是{}'.format(relation)

    @allure.title('test_account_038 查询指定版本的隐私政策')
    def test_account_038(self):
        with allure.step("获取最新隐私版本号"):
            r = session.request('GET', url='{}/account/privacy/latest'.format(env_url), headers=headers)
        with allure.step("查询指定版本的隐私政策"):
            params = {
                'version': r.json()['privacyPolicyVersion']
            }
            r = session.request('GET', url='{}/account/privacy'.format(env_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '"version":' in r.text, "查询指定版本的隐私政策失败，返回值是{}".format(r.text)

    @allure.title('test_account_039 查询指定版本的服务条款')
    def test_account_039(self):
        with allure.step("获取最新隐私版本号"):
            r = session.request('GET', url='{}/account/privacy/latest'.format(env_url), headers=headers)
        with allure.step("查询指定版本的服务条款"):
            params = {
                'version': r.json()['termOfServiceVersion']
            }
            r = session.request('GET', url='{}/account/tos'.format(env_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert '"version":' in r.text, "查询指定版本的服务条款失败，返回值是{}".format(r.text)

    @allure.title('test_account_040 忘记密码并且验证code')
    def test_account_040(self):
        account = get_json()['email']['payout_email']
        with allure.step("发忘记密码邮件"):
            code = ApiFunction.get_verification_code('FORGET_PASSWORD', account)
        with allure.step("验证忘记密码邮件"):
            ApiFunction.verify_verification_code('FORGET_PASSWORD', account, code)
        ApiFunction.add_headers()

    @allure.title('test_account_041 开启MFA且验证code')
    def test_account_041(self):
        account = get_json()['email']['payout_email']
        with allure.step("开启MFA且验证code"):
            code = ApiFunction.get_verification_code('ENABLE_MFA', account)
        with allure.step("开启MFA且验证code"):
            ApiFunction.verify_verification_code('ENABLE_MFA', account, code)
        ApiFunction.add_headers()

    @allure.title('test_account_042 关闭MFA且验证code')
    def test_account_042(self):
        account = get_json()['email']['payout_email']
        with allure.step("关闭MFA且验证code"):
            code = ApiFunction.get_verification_code('DISABLE_MFA', account)
        with allure.step("关闭MFA且验证code"):
            ApiFunction.verify_verification_code('DISABLE_MFA', account, code)
        ApiFunction.add_headers()

    @allure.title('test_account_043 MFA且验证code')
    def test_account_043(self):
        account = get_json()['email']['payout_email']
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account)
        with allure.step("MFA且验证code"):
            code = ApiFunction.get_verification_code('MFA_EMAIL', account)
        with allure.step("MFA且验证code"):
            ApiFunction.verify_verification_code('MFA_EMAIL', account, code)
        ApiFunction.add_headers()

    @allure.title('test_account_044 多次referal注册用户')
    def test_account_044(self):
        for i in range(5):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "666666",
                "password": get_json()['email']['password'],
                "metadata": {
                    "referral": {
                        "code": "CLC4BS"
                    }
                }
            }
            session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
            logger.info('邮箱是{}'.format(data['emailAddress']))
            sleep(5)
            with allure.step("数据库检查"):
                sql = "select relation from relation where referer_id='daf99d80-fcf4-4f10-8bb8-ab88dcf23cb8' and referee_id=(select account_id from account.user_account_map where user_id = (select user_id from account.user where email='{}'));".format(data['emailAddress'])
                relation = sqlFunction.connect_mysql('referral', sql)
                print(relation)
                print(type(relation[0]['relation']))
                assert relation[0]['relation'] == 2, '数据库查询值是{}'.format(relation)

    @allure.title('test_account_045 获取用户偏好信息')
    def test_account_045(self):
        with allure.step("获取用户偏好信息"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'language' in r.text, "获取用户偏好信息失败，返回值是{}".format(r.text)

    @allure.title('test_account_046 修改用户偏好信息')
    def test_account_046(self):
        with allure.step("获取用户偏好信息"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            data = r.json()
        with allure.step("修改用户偏好信息"):
            data1 = {
                "language": "zh_CN",
                "currency": "EUR",
                "timeZone": "Asia/shanghai"
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data1), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "获取用户偏好信息失败，返回值是{}".format(r.text)
        with allure.step("恢复之前的用户偏好信息"):
            session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)

    @allure.title('test_account_047 上传push相关token信息')
    def test_account_047(self):
        with allure.step("上传push相关token信息更新headers"):
            headers['User-Agent'] = 'iOS;1.0.0;1;14.4;14.4;iPhone;iPhone 12 Pro Max;'
            headers['X-Device'] = 'iOS'
            headers['X-locale'] = 'en_US'
            headers['Accept-Language'] = 'en_US'
            headers['X-Browser-Key'] = str(uuid.uuid4())
            headers['X-TimeZone'] = 'Asia/Shanghai'
        with allure.step("上传push相关token信息"):
            data = {
                "tokenType": 1,
                "token": "test_tokem2"
            }
            r = session.request('PUT', url='{}/preference/push/token'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "获取用户偏好信息失败，返回值是{}".format(r.text)

    @allure.title('test_account_048 登录后记录手机版本')
    def test_account_048(self):
        with allure.step("上传登录信息更新headers"):
            headers['User-Agent'] = 'iOS;1.0.0;1;14.4;14.4;iPhone;iPhone 12 Pro Max;'
            headers['X-Browser-Key'] = 'yilei_test'
        account = get_json()['email']['email']
        with allure.step("登录已经注册账号"):
            data = {
                "username": account,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "登录已经注册账号错误，返回值是{}".format(r.text)

    @allure.title('test_account_049 登出后refreshToken无法刷新')
    def test_account_049(self):
        with allure.step("上传登录信息更新headers"):
            headers['User-Agent'] = 'iOS;1.0.0;1;14.4;14.4;iPhone;iPhone 12 Pro Max;'
            headers['X-Browser-Key'] = 'yilei_test'
        account = get_json()['email']['email']
        with allure.step("登录已经注册账号"):
            data = {
                "username": account,
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "登录已经注册账号错误，返回值是{}".format(r.text)
            refreshToken = r.json()['refreshToken']
        with allure.step("登出"):
            headers['Authorization'] = 'Bearer {}'.format(r.json()['accessToken'])
            data = {
                'refreshToken': refreshToken
            }
            r = session.request('POST', url='{}/account/user/logout'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "登录已经注册账号错误，返回值是{}".format(r.text)
        with allure.step("刷新refreshToken"):
            data = {
                "refreshToken": refreshToken
            }
            r = session.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 401, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Refresh token error' in r.text, "用空的token刷新token错误，返回值是{}".format(r.text)

    @allure.title('test_account_050 修改nickname')
    def test_account_050(self):
        with allure.step("修改nickname"):
            data = {
                "nickname": "ad!@d😄我940!2342"
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "修改nickname错误，返回值是{}".format(r.text)
        with allure.step("获取用户偏好信息"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['nickname'] == "ad!@d😄我940!2342", "获取nickname失败，返回值是{}".format(r.text)

    @allure.title('test_account_051 修改nickname长度超过20')
    def test_account_051(self):
        with allure.step("修改nickname"):
            data = {
                "nickname": "ads157!934！#！@*#**#！2940我2342"
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['message'] == 'invalid nickname', "修改nickname错误，返回值是{}".format(r.text)

    @allure.title('test_account_052 打开/关闭notification推送')
    def test_account_052(self):
        with allure.step("打开notification推送"):
            data = {
                "notification_setting": {
                    "push_switch": 1
                }
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "打开/关闭notification推送错误，返回值是{}".format(r.text)

    @allure.title('test_account_052 打开/关闭notification推送')
    def test_account_052(self):
        with allure.step("打开notification推送"):
            data = {
                "notification_setting": {
                    "push_switch": 1
                }
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "打开/关闭notification推送错误，返回值是{}".format(r.text)

    @allure.title('test_account_053 注册时metadata随意传入信息')
    def test_account_053(self):
        with allure.step("打开notification推送"):
            account = generate_email()
            password = get_json()['email']['password']
            data = {
                "emailAddress": account,
                "password": password,
                "verificationCode": "666666",
                "citizenCountryCode": random.choice(get_json()['citizenCountryCodeList']),
                "metadata": {
                    "referral": {
                        "code": "metadata_test"
                    }
                }
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['accessToken'] is not None, "注册时metadata随意传入信息错误，返回值是{}".format(r.text)
        with allure.step("查询邮箱的account id"):
            sql = "select account_id from account.user_account_map where user_id=(select user_id from account.user where email='{}');".format(account)
            account_id = sqlFunction.connect_mysql(db='account', sql=sql, type=1)
            sql = "select metadata from account.account_metadata where account_id='{}';".format(account_id['account_id'])
            metadata = sqlFunction.connect_mysql(db='account', sql=sql, type=1)
            assert 'metadata_test' in metadata['metadata'], "注册时metadata随意传入信息数据库校验错误，返回值是{}".format(metadata)
            sql = "select metadata_type from account.account_metadata where account_id='{}';".format(account_id['account_id'])
            metadata_type = sqlFunction.connect_mysql(db='account', sql=sql)
            assert 'REFERRAL' in str(metadata_type), "注册时metadata随意传入信息数据库校验错误，返回值是{}".format(metadata)
            assert 'REGISTRY' in str(metadata_type), "注册时metadata随意传入信息数据库校验错误，返回值是{}".format(metadata)

    @allure.title('test_account_054 注册时无referral code并且metadata随意传入信息')
    def test_account_054(self):
        with allure.step("打开notification推送"):
            account = generate_email()
            password = get_json()['email']['password']
            data = {
                "emailAddress": account,
                "password": password,
                "verificationCode": "666666",
                "citizenCountryCode": random.choice(get_json()['citizenCountryCodeList']),
                "metadata": {
                    "dada": "213"
                }
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['accessToken'] is not None, "注册时metadata随意传入信息错误，返回值是{}".format(r.text)
        with allure.step("查询邮箱的account id"):
            sql = "select account_id from account.user_account_map where user_id=(select user_id from account.user where email='{}');".format(account)
            account_id = sqlFunction.connect_mysql(db='account', sql=sql, type=1)
            sql = "select metadata from account.account_metadata where account_id='{}';".format(account_id['account_id'])
            metadata = sqlFunction.connect_mysql(db='account', sql=sql, type=1)
            assert '213' in metadata['metadata'], "注册时metadata随意传入信息数据库校验错误，返回值是{}".format(metadata)
            sql = "select metadata_type from account.account_metadata where account_id='{}';".format(account_id['account_id'])
            metadata_type = sqlFunction.connect_mysql(db='account', sql=sql)
            assert 'REFERRAL' not in str(metadata_type), "注册时metadata随意传入信息数据库校验错误，返回值是{}".format(metadata)
            assert 'REGISTRY' in str(metadata_type), "注册时metadata随意传入信息数据库校验错误，返回值是{}".format(metadata)

    @allure.title('test_account_055 注册时传入internal用户类型')
    def test_account_055(self):
        with allure.step("打开notification推送"):
            account = generate_email()
            password = get_json()['email']['password']
            data = {
                "emailAddress": account,
                "password": password,
                "verificationCode": "666666",
                "citizenCountryCode": random.choice(get_json()['citizenCountryCodeList']),
                "metadata": {
                    "userType": "INTERNAL"
                }
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['accessToken'] is not None, "注册时metadata随意传入信息错误，返回值是{}".format(r.text)
        with allure.step("查询数据库的用户类型"):
            sql = "select user_type from account.user where email='{}';".format(account)
            user_type = sqlFunction.connect_mysql(db='account', sql=sql, type=1)
            assert 'INTERNAL' == user_type['user_type'], "注册时metadata随意传入信息数据库校验错误，返回值是{}".format(user_type)

    @allure.title('test_account_056 成功注册新用户不传国家地区码')
    def test_account_056(self):
        with allure.step("注册新用户"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "666666",
                "password": get_json()['email']['password']
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "成功注册新用户不传国家地区码失败，返回值是{}".format(r.text)
            assert r.json()['refreshExpiresTn'] == 86400, "token过期时间不是24小时，返回值是{}".format(r.text)

    @allure.title('test_account_057 获取已经设置密码用户的必填系统级数据')
    def test_account_057(self):
        with allure.step("获取已经设置密码用户的必填系统级数据"):
            r = session.request('GET', url='{}/account/info/system/required'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '"missing":[]' in r.text, "获取已经设置密码用户的必填系统级数据失败，返回值是{}".format(r.text)

    @allure.title('test_account_058 补充用户必填的系统级数据，密码已存在')
    def test_account_058(self):
        with allure.step("补充用户必填的系统级数据，密码已存在"):
            data = {
                "password": "Zcdsw123"
            }
            r = session.request('POST', url='{}/account/info/system/required'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '001024' in r.text, "补充用户必填的系统级数据，密码已存在失败，返回值是{}".format(r.text)

    @allure.title('test_account_059 获取用户必填的KYC数据，获取数据为空')
    def test_account_059(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yilei33@163.com')
        with allure.step("获取用户必填的KYC数据，获取数据为空"):
            r = session.request('GET', url='{}/account/info/kyc/required'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '"registryPurpose":null,' in r.text, "获取用户必填的KYC数据，获取数据为空失败，返回值是{}".format(r.text)

    @allure.title('test_account_060 获取用户必填的KYC数据，获取全部信息')
    def test_account_060(self):
        with allure.step("获取用户必填的KYC数据，获取全部信息"):
            r = session.request('GET', url='{}/account/info/kyc/required'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '"missing":[]' in r.text, "获取用户必填的KYC数据，获取全部信息失败，返回值是{}".format(r.text)

    @allure.title('test_account_061 补充用户必填的kyc数据')
    def test_account_061(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yilei33@163.com')
        with allure.step("获取用户必填的KYC数据，获取全部信息"):
            r = session.request('GET', url='{}/account/info/kyc/required'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert set(r.json()['missing']) == set(["RESIDENT", "REGISTRY_PURPOSE"]), "获取用户必填的KYC数据，获取全部信息失败，返回值是{}".format(r.text)
