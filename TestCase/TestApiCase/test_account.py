from Function.api_function import *
from run import *
from Function.log import *
import allure
import pyotp


# account相关cases
class TestAccountApi:

    # 初始化class
    def setup_class(self):
        AccountFunction.add_headers()

    @allure.testcase('test_account_001 成功注册新用户')
    def test_account_001(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "666666",
                "citizenCountryCode": citizenCountryCode,
                "password": "Zcdsw123"
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "注册新用户失败，返回值是{}".format(r.text)

    @allure.testcase('test_account_002 注册用户时，用户已经存在（正常流程不会存在此问题）')
    def test_account_002(self):
        account = generate_email()
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account)
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": account,
                "verificationCode": "666666",
                "citizenCountryCode": citizenCountryCode,
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Registration failed. Please contact our customer service if the problem persists.' in r.text, "用户已经存在错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_003 注册时，输入错误验证码导致注册失败')
    def test_account_003(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "166666",
                "citizenCountryCode": citizenCountryCode,
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'The verification code was wrong' in r.text, "注册时，输入错误验证码导致注册失败，返回值是{}".format(r.text)

    @allure.testcase('test_account_004 选择的国家代码可以成功申请注册验证码')
    def test_account_004(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
            data = {
                "emailAddress": "zcdsw159@163.com",
                "citizenCountryCode": citizenCountryCode
            }
            r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
                logger.info('国家代码是{}'.format(citizenCountryCode))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, "选择的国家代码可以成功申请注册验证码失败，返回值是{}".format(r.text)

    @allure.testcase('test_account_005 申请注册验证码的邮箱已注册')
    def test_account_005(self):
        account = generate_email()
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account)
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        data = {
            "emailAddress": account,
            "citizenCountryCode": citizenCountryCode
        }
        r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                             data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '{}' == r.text, "申请注册验证码的邮箱已注册错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_006 申请注册验证码邮箱在黑名单')
    def test_account_006(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("用黑名单邮箱申请注册验证码"):
            data = {
                "emailAddress": "yilei100@163.com",
                "citizenCountryCode": citizenCountryCode
            }
            r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '{}' == r.text, "申请注册验证码邮箱在黑名单错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_007 登录已经注册账号')
    def test_account_007(self):
        account = generate_email()
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account)
        with allure.step("登录已经注册账号"):
            data = {
                "username": account,
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "登录已经注册账号错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_008 登录已经注册账号输入错误密码')
    def test_account_008(self):
        account = generate_email()
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account)
        with allure.step("登录已经注册账号使用错误密码"):
            data = {
                "username": "yuk3e@cabital.com",
                "password": "A!2123123"
            }
            r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 404, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Incorrect account or password.' in r.text, "登录已经注册账号输入错误密码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_009 登录未注册账号')
    def test_account_009(self):
        with allure.step("登录未注册账号"):
            data = {
                "username": generate_email(),
                "password": "A!2123123"
            }
            r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 404, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Incorrect account or password.' in r.text, "登录已经注册账号输入错误密码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_010 登录已经注册的黑名单账号')
    def test_account_010(self):
        with allure.step("登录已经注册的黑名单账号"):
            blacklist = get_json()['blacklist']
            data = {
                "username": blacklist['email'],
                "password": blacklist['password']
            }
            r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "登录已经注册的黑名单账号错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_011 刷新账户token')
    def test_account_011(self):
        with allure.step("获取refreshToken"):
            data = {
                "username": email['email'],
                "password": email['password']
            }
            r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                                headers=headers)
            refreshToken = r.json()['refreshToken']
        with allure.step("刷新tokne"):
            data = {
                "refreshToken": refreshToken
            }
            r = requests.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "刷新账户token错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_012 用错误的token刷新token')
    def test_account_012(self):
        with allure.step("用错误的token刷新token"):
            data = {
                "refreshToken": "123"
            }
            r = requests.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 401, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Refresh token error' in r.text, "用错误的token刷新token错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_013 用空的token刷新token')
    def test_account_013(self):
        with allure.step("用空的token刷新token"):
            data = {
                "refreshToken": ""
            }
            r = requests.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid refresh token' in r.text, "用空的token刷新token错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_014 修改密码')
    def test_account_014(self):
        account = generate_email()
        password = 'Zcdsw123'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("修改密码"):
            data = {
                "original": password,
                "password": "87654321"
            }
            r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "修改密码错误，返回值是{}".format(r.text)
        with allure.step("用新密码重新登录"):
            AccountFunction.get_account_token(account=account, password='87654321')

    @allure.testcase('test_account_015 修改密码使用错误token')
    def test_account_015(self):
        with allure.step("把错误token写入headers"):
            headers['Authorization'] = "Bearer " + "accessToken1234"
        with allure.step("修改密码使用错误token"):
            data = {
                "original": "Zcdsw123",
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 401, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.testcase('test_account_016 使用错误原始密码修改密码')
    def test_account_016(self):
        account = generate_email()
        password = 'Zcdsw123'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("使用错误原始密码修改密码"):
            data = {
                "original": "11111",
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "Invalid original password." in r.text, "使用错误原始密码修改密码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_017 忘记密码验证码')
    def test_account_017(self):
        account = generate_email()
        password = 'Zcdsw123'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("忘记密码验证码"):
            data = {
                "emailAddress": account,
            }
            r = requests.request('POST', url='{}/account/user/forgetPassword/sendVerificationCode'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "忘记密码验证码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_018 用户未注册忘记密码验证码')
    def test_account_018(self):
        with allure.step("用户未注册忘记密码验证码"):
            data = {
                "emailAddress": generate_email()
            }
            r = requests.request('POST', url='{}/account/user/forgetPassword/sendVerificationCode'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "用户未注册忘记密码验证码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_019 忘记密码')
    def test_account_019(self):
        with allure.step("忘记密码"):
            account = generate_email()
            password = 'Zcdsw123'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
            data = {
                "code": "666666",
                "email": account,
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "忘记密码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_020 未注册用户忘记密码失败')
    def test_account_020(self):
        with allure.step("未注册用户忘记密码失败"):
            data = {
                "code": "666666",
                "email": generate_email(),
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "The verification code was wrong." in r.text, "未注册用户忘记密码失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_021 用户忘记密码验证码错误')
    def test_account_021(self):
        with allure.step("用户忘记密码验证码错误"):
            account = generate_email()
            password = 'Zcdsw123'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
        with allure.step("用户忘记密码验证码错误"):
            data = {
                "code": "166666",
                "email": account,
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "The verification code was wrong." in r.text, "用户忘记密码验证码错误错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_022 查询用户信息')
    def test_account_022(self):
        with allure.step("查询用户信息"):
            r = requests.request('GET', url='{}/account/info'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "user" in r.text, "查询用户信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_023 修改个人信息')
    def test_account_023(self):
        with allure.step("修改个人信息"):
            account = generate_email()
            password = 'Zcdsw123'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("修改个人信息"):
            data = {
                "firstName": "yuke",
                "lastName": "zhang",
                "dateOfBirth": "1997-12-12",
                "gender": "MALE"
            }
            r = requests.request('POST', url='{}/account/info/personal'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "修改个人信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_024 修改个人爱好')
    def test_account_024(self):
        with allure.step("修改个人爱好"):
            account = generate_email()
            password = 'Zcdsw123'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("修改个人爱好"):
            data = {
                "language": "EN",
                "currency": "USD",
                "timeZone": "W11"
            }
            r = requests.request('POST', url='{}/account/setting/preference'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "修改个人爱好错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_025 申请注册验证码,使用白名单外国家代码被拒绝')
    def test_account_025(self):
        with allure.step("申请注册验证码,使用白名单外国家代码被拒绝"):
            data = {
                "emailAddress": generate_email(),
                "citizenCountryCode": "WYL"
            }
            r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "Sorry, this country is temporarily not supported. Your email will be notified when we launch in your country." in r.text, "申请注册验证码,使用白名单外国家代码被拒绝错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_026 用户使用特殊符号注册')
    def test_account_026(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": '%$#{}@dsadda.com'.format(generate_number(8)),
                "verificationCode": "666666",
                "citizenCountryCode": citizenCountryCode,
                "password": "123456"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "用户使用特殊符号注册错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_027 注册用户验证码缺少位数输入')
    def test_account_027(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "16666",
                "citizenCountryCode": citizenCountryCode,
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid verification code' in r.text, "注册用户验证码缺少位数输入错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_028 注册用户验证码输入字符')
    def test_account_028(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "dqwdqwd",
                "citizenCountryCode": citizenCountryCode,
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid verification code' in r.text, "注册用户验证码输入字符错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_029 登录已经注册账号密码使用特殊字符')
    def test_account_029(self):
        account = generate_email()
        password = "Zcdsw1!@#$%^"
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("登录已经注册账号使用错误密码"):
            data = {
                "username": account,
                "password": password
            }
            r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, " 登录已经注册账号密码使用特殊字符错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_030 使用相同的密码修改密码')
    def test_account_030(self):
        account = generate_email()
        password = 'Zcdsw123'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("修改密码"):
            data = {
                "original": password,
                "password": password
            }
            r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "使用相同的密码修改密码错误，返回值是{}".format(r.text)
        with allure.step("用新密码重新登录"):
            AccountFunction.get_account_token(account=account, password=password)

    @allure.testcase('test_account_031 mfa验证码')
    def test_account_031(self):
        data = {
            "type": "OTP",
            "enable": True
        }
        r = requests.request('POST', url='{}/account/security/mfa/sendEmailVerificationCode'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "mfa验证码错误，目前返回值是{}".format(r.text)

    @allure.testcase('test_account_032 获取mfa邮箱验证码')
    def test_account_032(self):
        r = requests.request('GET', url='{}/account/security/mfa/email/sendVerificationCode'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "获取mfa邮箱验证码不对，目前返回值是{}".format(r.text)

    @allure.testcase('test_account_033 获取opt二维码')
    def test_account_033(self):
        run.accountToken = AccountFunction.get_account_token(account='yilei1@163.com')
        headers['Authorization'] = "Bearer " + run.accountToken
        r = requests.request('GET', url='{}/account/security/mfa/otp/qrcode'.format(env_url), headers=headers)
        AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'SUCCESS' == r.json()['result'], "获取opt二维码不对，目前返回值是{}".format(r.text)

    @allure.testcase('test_account_034 创建opt验证，并且删除。')
    def test_account_034(self):
        run.accountToken = AccountFunction.get_account_token(account='yilei3@163.com')
        headers['Authorization'] = "Bearer " + run.accountToken
        # 获得opt secretKey
        r = requests.request('GET', url='{}/account/security/mfa/otp/qrcode'.format(env_url), headers=headers)
        if 'ACC_SECURITY_MFA_000001' in r.text:
            # 删除opt
            secretKey = get_json()['secretKeyForTest']
            totp = pyotp.TOTP(secretKey)
            mfaVerificationCode = totp.now()
            data = {
                "mfaVerificationCode": str(mfaVerificationCode),
                "emailVerificationCode": "666666"
            }
            requests.request('POST', url='{}/account/security/mfa/otp/disable'.format(env_url), data=json.dumps(data), headers=headers)
            write_json('secretKeyForTest', ' ')
        else:
            r = requests.request('GET', url='{}/account/security/mfa/otp/qrcode'.format(env_url), headers=headers)
        if "SUCCESS" in r.text:
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
            r = requests.request('POST', url='{}/account/security/mfa/otp/enable'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert {} == r.json(), "创建opt验证不对，目前返回值是{}".format(r.text)
        # 删除opt
        secretKey = get_json()['secretKeyForTest']
        totp = pyotp.TOTP(secretKey)
        mfaVerificationCode = totp.now()
        data = {
            "mfaVerificationCode": str(mfaVerificationCode),
            "emailVerificationCode": "666666"
        }
        requests.request('POST', url='{}/account/security/mfa/otp/disable'.format(env_url), data=json.dumps(data),
                         headers=headers)
        write_json('secretKeyForTest', ' ')
        AccountFunction.add_headers()

    @allure.testcase('test_account_035 验证opt code')
    def test_account_035(self):
        # 验证opt code
        run.accountToken = AccountFunction.get_account_token(account='external.qa@cabital.com')
        headers['Authorization'] = "Bearer " + run.accountToken
        secretKey = get_json()['secretKey']
        totp = pyotp.TOTP(secretKey)
        mfaVerificationCode = totp.now()
        data = {
            "totp": str(mfaVerificationCode)
        }
        r = requests.request('POST', url='{}/account/security/mfa/otp/verify'.format(env_url), data=json.dumps(data), headers=headers)
        AccountFunction.add_headers()
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), " 验证opt code不对，目前返回值是{}".format(r.text)

    @allure.testcase('test_account_036 接受隐私政策版本')
    def test_account_036(self):
        data = {
            "privacyPolicyVersion": 20210528,
            "termOfServiceVersion": 20210528
        }
        r = requests.request('POST', url='{}/account/setting/privacy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "接受隐私政策版本不对，目前返回值是{}".format(r.text)

    @allure.testcase('test_account_037 查询最新隐私政策版本')
    def test_account_037(self):
        r = requests.request('GET', url='{}/account/privacy/latest'.format(env_url), headers=headers)
        data = {
            "privacyPolicyVersion": r.json()['privacyPolicyVersion'],
            "termOfServiceVersion": r.json()['termOfServiceVersion']
        }
        requests.request('POST', url='{}/account/setting/privacy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'privacyPolicyVersion' in r.text, "查询最新隐私政策版本不对，目前返回值是{}".format(r.text)
            # 查询用户信息
            r1 = requests.request('GET', url='{}/account/info'.format(env_url), headers=headers)
            assert r.json()['privacyPolicyVersion'] == r1.json()['user']['userPrivacyPolicy']['privacyPolicyVersion'], 'privacyPolicyVersion最新版本和个人接受版本不匹配'
            assert r.json()['termOfServiceVersion'] == r1.json()['user']['userPrivacyPolicy']['termOfServiceVersion'], 'termOfServiceVersion最新版本和个人接受版本不匹配'

    @allure.testcase('test_account_038 修改投资目的')
    def test_account_038(self):
        data = {
            "purposes": [
                "SAVING_OR_INVESTMENT"
            ]
        }
        r = requests.request('POST', url='{}/account/setting/purpose'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert '' in r.text, "修改投资目的不对，目前返回值是{}".format(r.text)
            # useId = get_json()['email']['userId']
            # sql = "SELECT purposes FROM user_registry_purpose where user_id = '{}';".format(useId)
            # purposes = sqlFunction.connect_mysql('account', sql)

    @allure.testcase('test_account_039 注册时，多输入几位验证码导致注册失败')
    def test_account_039(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "1366666",
                "citizenCountryCode": citizenCountryCode,
                "password": "Zcdsw123"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Invalid verification code' in r.text, "注册时，输入错误验证码导致注册失败，返回值是{}".format(r.text)

    @allure.testcase('test_account_040 获得邀请人数和奖励')
    def test_account_040(self):
        with allure.step("获得邀请人数和奖励"):
            r = requests.request('GET', url='{}/recruit/referal/referees'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'count' in r.json().keys(), "获得邀请人数和奖励失败，返回值是{}".format(r.text)

    @allure.testcase('test_account_041 获得邀请码和链接')
    def test_account_041(self):
        with allure.step("获得邀请人数和奖励"):
            r = requests.request('GET', url='{}/recruit/referal/code'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['code'] is not None, "获得邀请人数和奖励失败，返回值是{}".format(r.text)

    @allure.testcase('test_account_042 referal注册用户')
    def test_account_042(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "666666",
                "citizenCountryCode": citizenCountryCode,
                "password": "Zcdsw123",
                "metadata": {
                    "referral": {
                    "code": "6EM7LK"
                    }
                }
            }
            r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
            logger.info('邮箱是{}'.format(data['emailAddress']))
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'accessToken' in r.text, "注册新用户失败，返回值是{}".format(r.text)
        with allure.step("数据库检查"):
            sql = "select * from relation where referee_id=(select account_id from account.user_account_map where user_id = (select user_id from account.user where email='{}'));".format(data['emailAddress'])
            relation = sqlFunction.connect_mysql('referral', sql)
            print(relation)


    @allure.testcase('test_account_043 查询指定版本的隐私政策')
    def test_account_043(self):
        with allure.step("获取最新隐私版本号"):
            r = requests.request('GET', url='{}/account/privacy/latest'.format(env_url), headers=headers)
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

    @allure.testcase('test_account_044 查询指定版本的服务条款')
    def test_account_044(self):
        with allure.step("获取最新隐私版本号"):
            r = requests.request('GET', url='{}/account/privacy/latest'.format(env_url), headers=headers)
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

    @allure.testcase('test_account_045 忘记密码并且验证code')
    def test_account_045(self):
        account = get_json()['email']['payout_email']
        run.accountToken = AccountFunction.get_account_token(account=account)
        headers['Authorization'] = "Bearer " + run.accountToken
        with allure.step("发忘记密码邮件"):
            code = AccountFunction.get_verification_code('FORGET_PASSWORD', account)
        with allure.step("验证忘记密码邮件"):
            AccountFunction.verify_verification_code('FORGET_PASSWORD', account, code)
        AccountFunction.add_headers()

    @allure.testcase('test_account_045 开启MFA且验证code')
    def test_account_045(self):
        account = get_json()['email']['payout_email']
        run.accountToken = AccountFunction.get_account_token(account=account)
        headers['Authorization'] = "Bearer " + run.accountToken
        with allure.step("发忘记密码邮件"):
            code = AccountFunction.get_verification_code('ENABLE_MFA', account)
        with allure.step("验证忘记密码邮件"):
            AccountFunction.verify_verification_code('ENABLE_MFA', account, code)
        AccountFunction.add_headers()

    @allure.testcase('test_account_045 关闭MFA且验证code')
    def test_account_045(self):
        account = get_json()['email']['payout_email']
        run.accountToken = AccountFunction.get_account_token(account=account)
        headers['Authorization'] = "Bearer " + run.accountToken
        with allure.step("发忘记密码邮件"):
            code = AccountFunction.get_verification_code('DISABLE_MFA', account)
        with allure.step("验证忘记密码邮件"):
            AccountFunction.verify_verification_code('DISABLE_MFA', account, code)
        AccountFunction.add_headers()

    @allure.testcase('test_account_045 MFA且验证code')
    def test_account_045(self):
        account = get_json()['email']['payout_email']
        run.accountToken = AccountFunction.get_account_token(account=account)
        headers['Authorization'] = "Bearer " + run.accountToken
        with allure.step("发忘记密码邮件"):
            code = AccountFunction.get_verification_code('MFA_EMAIL', account)
        with allure.step("验证忘记密码邮件"):
            AccountFunction.verify_verification_code('MFA_EMAIL', account, code)
        AccountFunction.add_headers()
