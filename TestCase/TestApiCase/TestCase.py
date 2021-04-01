from Function.ApiFunction import *
from run import *
from Function.log import *
import allure


# account相关cases
class TestAccountApi:

    @allure.testcase('test_account_001 成功注册用户')
    def test_account_001(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "666666",
                "citizenCountryCode": citizenCountryCode,
                "password": "12345678"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "成功注册用户错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_002 注册用户用户已经存在')
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
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_REGISTRY_000002' in r.text, "用户已经存在错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_003 注册用户验证码错误输入')
    def test_account_003(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "1666666",
                "citizenCountryCode": citizenCountryCode,
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'COMMON_000006' in r.text, "验证码错误错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_004 申请注册验证码,全可过国家')
    def test_account_004(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
            data = {
                "emailAddress": generate_email(),
                "citizenCountryCode": citizenCountryCode
            }
            r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                                 data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
                logger.info('国家代码是{}'.format(citizenCountryCode))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, "申请注册验证码,全可过国家错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_005 申请注册验证码邮箱已注册')
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
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "ACC_REGISTRY_000002" in r.text, "申请注册验证码邮箱已注册错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_006 申请注册验证码邮箱在黑名单')
    def test_account_006(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("用黑名单邮箱申请注册验证码"):
            data = {
                "emailAddress": "heimingdan@test.com",
                "citizenCountryCode": citizenCountryCode
            }
            r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "ACC_REGISTRY_000001" in r.text, "申请注册验证码邮箱在黑名单错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_007 登录已经注册账号')
    def test_account_007(self):
        account = generate_email()
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account)
        with allure.step("登录已经注册账号"):
            data = {
                "username": account,
                "password": "12345678"
            }
            r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "登录已经注册账号错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_008 登录已经注册账号密码错误')
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
            assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_LOGIN_000001' in r.text, "登录已经注册账号密码错误错误，返回值是{}".format(r.text)

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
            assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_LOGIN_000001' in r.text, "登录已经注册账号密码错误错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_010 登录黑名单账号')
    def test_account_010(self):
        with allure.step("登录黑名单账号"):
            data = {
                "username": "b3Gv@gmail.com",
                "password": "123456"
            }
            r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        # with allure.step("校验返回值"):
        #     assert 'ACC_LOGIN_000001' in r.text, "登录已经注册账号密码错误错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_011 刷新账户token')
    def test_account_011(self):
        with allure.step("获取refreshToken"):
            refreshToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'refreshToken']
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
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
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
            assert r.status_code == 401, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_LOGIN_000003' in r.text, "用错误的token刷新token错误，返回值是{}".format(r.text)

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
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'COMMON_000006' in r.text, "用空的token刷新token错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_014 修改密码')
    def test_account_014(self):
        account = generate_email()
        password = '12345678'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
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
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
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
                "original": "A!234sdfg",
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 401, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.testcase('test_account_016 使用错误原始密码修改密码')
    def test_account_016(self):
        account = generate_email()
        password = '12345678'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("使用错误原始密码修改密码"):
            data = {
                "original": "11111",
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "ACC_RESET_000001" in r.text, "使用错误原始密码修改密码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_017 忘记密码验证码')
    def test_account_017(self):
        account = generate_email()
        password = '12345678'
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
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
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
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "ACC_USER_000002" in r.text, "用户未注册忘记密码验证码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_019 忘记密码')
    def test_account_019(self):
        with allure.step("忘记密码"):
            account = generate_email()
            password = '12345678'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
            data = {
                "code": "666666",
                "email": account,
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "忘记密码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_020 未注册用户忘记密码')
    def test_account_020(self):
        with allure.step("忘记密码"):
            data = {
                "code": "666666",
                "email": generate_email(),
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "ACC_USER_000002" in r.text, "未注册用户忘记密码错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_021 用户忘记密码验证码错误')
    def test_account_021(self):
        with allure.step("忘记密码"):
            account = generate_email()
            password = '12345678'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
        with allure.step("用户忘记密码验证码错误"):
            data = {
                "code": "166666",
                "email": account,
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                                 data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "ACC_VERIFY_CODE_000001" in r.text, "用户忘记密码验证码错误错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_021 查询用户信息')
    def test_account_021(self):
        with allure.step("忘记密码"):
            account = generate_email()
            password = '12345678'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询用户信息"):
            r = requests.request('GET', url='{}/account/info'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "user" in r.text, "查询用户信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_022 修改个人信息')
    def test_account_022(self):
        with allure.step("忘记密码"):
            account = generate_email()
            password = '12345678'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
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
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "修改个人信息错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_023 修改个人爱好')
    def test_account_023(self):
        with allure.step("忘记密码"):
            account = generate_email()
            password = '12345678'
            with allure.step("提前先注册好"):
                AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
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
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "用户忘记密码验证码错误错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_024 申请注册验证码,使用白名单外国家代码被拒绝')
    def test_account_024(self):
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
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert "ACC_LEGAL_ENTITY_000001" in r.text, "申请注册验证码,使用白名单外国家代码被拒绝错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_025 用户使用特殊符号注册')
    def test_account_025(self):
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
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "用户使用特殊符号注册错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_026 注册用户验证码缺少位数输入')
    def test_account_026(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "16666",
                "citizenCountryCode": citizenCountryCode,
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'COMMON_000006' in r.text, "注册用户验证码缺少位数输入错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_027 注册用户验证码输入字符')
    def test_account_027(self):
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("注册"):
            data = {
                "emailAddress": generate_email(),
                "verificationCode": "dqwdqwd",
                "citizenCountryCode": citizenCountryCode,
                "password": "A!234sdfg"
            }
            r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'COMMON_000006' in r.text, "注册用户验证码输入字符错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_028 登录已经注册账号密码使用特殊字符')
    def test_account_028(self):
        account = generate_email()
        password = "@#$123456"
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
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, " 登录已经注册账号密码使用特殊字符错误，返回值是{}".format(r.text)

    @allure.testcase('test_account_029 使用相同的密码修改密码')
    def test_account_029(self):
        account = generate_email()
        password = '12345678'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
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
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "使用相同的密码修改密码错误，返回值是{}".format(r.text)
        with allure.step("用新密码重新登录"):
            AccountFunction.get_account_token(account=account, password=password)


# kyc相关cases
class TestKycApi:

    @allure.testcase('test_kyc_001 通过kyc的用户，获取kyc上传token失败')
    def test_kyc_001(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("随机获得国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
            data = {
                "citizenCountryCode": citizenCountryCode
            }
        with allure.step("通过kyc的用户，获取kyc上传token失败"):
            r = requests.request('POST', url='{}/kyc/case/start'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'KYC_CASE_000001' in r.text, "通过kyc的用户，获取kyc上传token失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_002 未通过kyc的用户，获取kyc上传token')
    def test_kyc_002(self):
        account = generate_email()
        password = '12345678'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取随机国家代码"):
            citizenCountryCode = random.choice(citizenCountryCodeList)
        with allure.step("未通过kyc的用户，获取kyc上传token"):
            data = {
                "citizenCountryCode": citizenCountryCode
            }
            r = requests.request('POST', url='{}/kyc/case/start'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'Cabital_LT_KYC_Mobile_Basic' in r.text, "通过kyc的用户，获取kyc上传token错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_003 未申请kyc获取kyc-case失败')
    def test_kyc_003(self):
        account = generate_email()
        password = '12345678'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        allure.dynamic.description("调用kyc")
        with allure.step("未申请kyc获取kyc-case失败"):
            data = {
            }
            r = requests.request('POST', url='{}/kyc/case/get'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'informations' in r.text, "未申请kyc获取kyc-case失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_kyc_004 获取kyc-case')
    def test_kyc_004(self):
        with allure.step("获取token"):
            accessToken = AccountFunction.get_account_token(account="james@test.com", password="A!234sdfg")[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("调用kyc"):
            data = {
            }
            r = requests.request('POST', url='{}/kyc/case/get'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'id' in r.text, "获取kyc-case错误，返回值是{}".format(r.text)


# core相关cases
class TestCoreApi:

    @allure.testcase('test_core_001 查询钱包所有地址')
    def test_core_001(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包所有地址"):
            r = requests.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'wallets' in r.text, "查询钱包所有地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_002 查询钱包所有币种')
    def test_core_002(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包所有币种"):
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'id' in r.text, "查询钱包所有币种错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_003 查询钱包某个币种')
    def test_core_003(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包所有币种"):
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
            id = r.json()[0]["id"]
        with allure.step("查询钱包某个币种"):

            r = requests.request('GET', url='{}/core/account/wallets/{}'.format(env_url, id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['id'] is not None, "查询钱包所有币种错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_004 查询货币兑换比例')
    def test_core_004(self):
        list = ['BTC-USD', 'USD-BTC', 'USD-EUR', 'EUR-USD', 'BTC-EUR', 'BTC-EUR']
        with allure.step("查询货币兑换比例"):
            for i in list:
                with allure.step("查询{}兑换比例".format(i)):
                    r = requests.request('GET', url='{}/core/quotes/{}'.format(env_url, i), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['quote'] != {}, " 查询货币兑换比例错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_005 查询钱包所有币种，使用SAVING模式')
    def test_core_005(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包所有币种，使用SAVING模式"):
            params = {
                'type': 'SAVING'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'SAVING' in r.text, "查询钱包所有币种，使用SAVING模式错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_006 查询钱包所有币种，使用BALANCE模式')
    def test_core_006(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包所有币种，使用BALANCE模式"):
            params = {
                'type': 'BALANCE'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BALANCE' in r.text, "查询钱包所有币种，使用BALANCE模式错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_007 查询钱包BTC地址')
    def test_core_007(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包BTC地址"):
            params = {
                'code': 'BTC'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'BTC' in r.text, "查询钱包BTC地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_008 查询钱包ETH地址')
    def test_core_008(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包ETH地址"):
            params = {
                'code': 'BTC'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ETH' in r.text, "查询钱包ETH地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_core_007 查询钱包USDT地址')
    def test_core_007(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询钱包USDT地址"):
            params = {
                'code': 'USDT'
            }
            r = requests.request('GET', url='{}/core/account/wallets'.format(env_url), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'USDT' in r.text, "查询钱包USDT地址错误，返回值是{}".format(r.text)


# market相关cases
class TestMarketApi:
    @allure.testcase('test_market_001 获得价格曲线')
    def test_market_001(self):
        with allure.step("循环货币循环时间"):
            pass
        for i in ['BTCEUR', 'BTCUSD', 'ETHEUR', 'ETHUSD', 'USDEUR']:
            for y in ['10', '60', 'D', 'W', 'M']:
                params = {
                    "pair": i,
                    "interval": y,
                    "from_time": "0",
                    "to_time": ""
                }
                r = requests.request('GET', url='{}/marketstat/public/quote-chart'.format(env_url), params=params,
                                     headers=headers)
                logger.info('货币{}的{}时间的曲线{}'.format(i, y, r.text))
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert 'items' in r.text, "获得价格曲线错误，返回值是{}".format(r.text)


# payout相关cases
class TestPayoutApi:

    @allure.testcase('test_payout_001 没有Kyc用户添加常用收款地址失败')
    def test_payout_001(self):
        account = generate_email()
        password = '12345678'
        with allure.step("提前先注册好"):
            AccountFunction.sign_up(account, password)
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=account, password=password)['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("没有Kyc用户添加常用收款地址失败"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "USDT",
                "method": "ERC20",
                "address": "test-address"
            }
            r = requests.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 403, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_FORBIDDEN' in r.text, "没有Kyc用户添加常用收款地址失败错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_002 有Kyc用户添加常用收款地址')
    def test_payout_002(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("有Kyc用户添加常用收款地址"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "USDT",
                "method": "ERC20",
                "address": "test-address"
            }
            r = requests.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "有Kyc用户添加常用收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_003 获取收款地址list')
    def test_payout_003(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取收款地址list"):
            r = requests.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'payeeList' in r.text, "获取收款地址list错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_004 获取常用收款地址')
    def test_payout_004(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取收款地址list"):
            r = requests.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
        with allure.step("获取单个收款地址id"):
            id = r.json()['payeeList'][0]['id']
        with allure.step("获取单个收款地址"):
            r = requests.request('GET', url='{}/account/myPayee/{}'.format(env_url, id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'payeeList' in r.text, "获取常用收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_005 使用不存在id获取常用收款地址')
    def test_payout_005(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])['accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("使用不存在id获取常用收款地址"):
            r = requests.request('GET', url='{}/account/myPayee/{}'.format(env_url, '300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_MY_PAYEE_000001' in r.text, "使用不存在id获取常用收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_006 更新收款地址')
    def test_payout_006(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("更新收款地址"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "EUR",
                "method": "ERC20",
                "address": "test-address-update",
                "isValid": True,
                "whitelisted": False
            }
            r = requests.request('PUT', url='{}/account/myPayee/{}'.format(env_url, '3'), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "更新收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_007 更新使用不存在id收款地址')
    def test_payout_007(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("更新使用不存在id收款地址"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "EUR",
                "method": "ERC20",
                "address": "test-address-update",
                "isValid": True,
                "whitelisted": False
            }
            r = requests.request('PUT', url='{}/account/myPayee/{}'.format(env_url, '300'), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_MY_PAYEE_000001' in r.text, "更新使用不存在id收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_008 删除收款地址')
    def test_payout_008(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("增加常用地址"):
            data = {
                "nickName": "alan EUR ERC20",
                "currency": "USDT",
                "method": "ERC20",
                "address": "test-address-delete"
            }
            requests.request('POST', url='{}/account/myPayee/create'.format(env_url), data=json.dumps(data),
                             headers=headers)
        with allure.step("寻找刚加的地址，获得id号"):
            r = requests.request('GET', url='{}/account/myPayee/list'.format(env_url), headers=headers)
            for i in r.json()['payeeList']:
                if i['address'] == "test-address-delete":
                    with allure.step("凭借id号删除地址"):
                        r = requests.request('DELETE', url='{}/account/myPayee/{}'.format(env_url, i['id']),
                                             headers=headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert {} == r.json(), "删除收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_009 根据不存在的删除收款地址')
    def test_payout_009(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("凭借空id号删除地址"):
            r = requests.request('DELETE', url='{}/account/myPayee/{}'.format(env_url, '300'), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'ACC_MY_PAYEE_000001' in r.text, "删除收款地址错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_010 获取提现费率和提现限制')
    def test_payout_010(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("获取提现费率和提现限制"):
            data = {
                "amount": "0.8",
                "code": "BTC",
                "address": "xxxxxxxxxxxx",
                "method": "ERC20",
                "receive_amount": "0.79995"
            }
            r = requests.request('POST', url='{}/pay/withdraw/verification'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'fee' in r.text, "获取提现费率和提现限制错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_011 使用错误地址提现')
    def test_payout_011(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("提现"):
            data = {
                "amount": "0.8",
                "code": "BTC",
                "address": "xxxxxxxxxxxx",
                "method": "ERC20"
            }
            r = requests.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'WALLET000003' in r.text, "使用错误地址提现错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_012 提现失败')
    def test_payout_012(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("提现"):
            data = {
                "amount": "0.8",
                "code": "BTC",
                "address": "b8915f70-3e28-480b-970a-d54ec8d8a284",
                "method": "ERC20"
            }
            r = requests.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'transaction_id' in r.text, "提现错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_013 查询提现详情')
    def test_payout_013(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询提现详情"):
            r = requests.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url,
                                                                                     '46842250-3fa0-4bd1-9d46-4467dfa9ce52'),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'transaction_time' in r.text, "查询提现详情错误，返回值是{}".format(r.text)

    @allure.testcase('test_payout_014 使用错误id查询提现详情')
    def test_payout_014(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询提现详情"):
            r = requests.request('GET', url='{}/pay/withdraw/transactions/{}'.format(env_url,
                                                                                     '468422531310-3fa0-4bd1-9d46-4467dfa9ce52'),
                                 headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'no rows in result set' in r.text, "使用错误id查询提现详情错误，返回值是{}".format(r.text)


# pay in相关cases
class TestPayInApi:

    @allure.testcase('test_pay_in_001 查询转入记录（不指定链）')
    def test_pay_in_001(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询转入记录"):
            currency = ['USDT', 'BTC', 'ETH']
            data = {}
            for i in currency:
                data['code'] = i
                r = requests.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data,
                                     headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == [] or 'code' in r.text, "查询转入记录（不指定链）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_002 查询转入记录（使用错误币种）')
    def test_pay_in_002(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询转入记录"):
            data = {
                'code': 'US345'
            }
            r = requests.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'method is not support message' in r.text, "查询转入记录（使用错误币种）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_003 查询转入记录（使用转币链查询）')
    def test_pay_in_003(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询转入记录"):
            data = {
                'code': 'ETH',
                'method': 'ERC20'
            }
            r = requests.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'ERC20' in r.text, "查询转入记录（使用转币链查询）错误，返回值是{}".format(r.text)

    @allure.testcase('test_pay_in_004 查询转入记录（使用错误转币链查询）')
    def test_pay_in_004(self):
        with allure.step("获得token"):
            accessToken = AccountFunction.get_account_token(account=email['email'],  password=email['password'])[
                'accessToken']
        with allure.step("把token写入headers"):
            headers['Authorization'] = "Bearer " + accessToken
        with allure.step("查询转入记录"):
            data = {
                'code': 'ETH',
                'method': 'ER124141'
            }
            r = requests.request('GET', url='{}/pay/deposit/addresses'.format(env_url), params=data, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'method is not support message' in r.text, "查询转入记录（使用错误转币链查询）错误，返回值是{}".format(r.text)
