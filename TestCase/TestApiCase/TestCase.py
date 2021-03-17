import requests
import allure
from Function.ApiFunction import *
from run import *


# account相关cases
class TestAccountApi:

    @allure.feature('test_account_001 成功注册用户')
    def test_account_001(self):
        data = {
            "emailAddress": generate_email(),
            "verificationCode": "666666",
            "citizenCountryCode": "cn",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accessToken' in r.text, "成功注册用户错误，返回值是{}".format(r.text)

    @allure.feature('test_account_002 注册用户用户已经存在')
    def test_account_002(self):
        data = {
            "emailAddress": "yuk3e@cabital.com",
            "verificationCode": "666666",
            "citizenCountryCode": "cn",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'ACC_REGISTRY_000002' in r.text, "用户已经存在错误，返回值是{}".format(r.text)

    @allure.feature('test_account_003 注册用户验证码错误')
    def test_account_003(self):
        data = {
            "emailAddress": generate_email(),
            "verificationCode": "1666666",
            "citizenCountryCode": "cn",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'COMMON_000006' in r.text, "验证码错误错误，返回值是{}".format(r.text)

    @allure.feature('test_account_004 申请注册验证码')
    def test_account_004(self):
        data = {
            "emailAddress": generate_email(),
        }
        r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "申请注册验证码错误，返回值是{}".format(r.text)

    @allure.feature('test_account_005 申请注册验证码邮箱已注册')
    def test_account_005(self):
        data: dict[str, str] = {
            "emailAddress": "yuk3e@cabital.com",
        }
        r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert "ACC_REGISTRY_000002" in r.text, "申请注册验证码邮箱已注册错误，返回值是{}".format(r.text)

    @allure.feature('test_account_006 申请注册验证码邮箱在黑名单')
    def test_account_006(self):
        data = {
            "emailAddress": "yuk3e@cabital.com",
        }
        r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert "ACC_REGISTRY_000002" in r.text, "申请注册验证码邮箱在黑名单错误，返回值是{}".format(r.text)

    @allure.feature('test_account_007 登录已经注册账号')
    def test_account_007(self):
        data = {
            "username": "yuk3e@cabital.com",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accessToken' in r.text, "登录已经注册账号错误，返回值是{}".format(r.text)

    @allure.feature('test_account_008 登录已经注册账号密码错误')
    def test_account_008(self):
        data = {
            "username": "yuk3e@cabital.com",
            "password": "A!2123123"
        }
        r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'ACC_LOGIN_000001' in r.text, "登录已经注册账号密码错误错误，返回值是{}".format(r.text)

    @allure.feature('test_account_009 登录未注册账号')
    def test_account_009(self):
        data = {
            "username": "yuk3e@cabital23.com",
            "password": "A!2123123"
        }
        r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'ACC_LOGIN_000001' in r.text, "登录已经注册账号密码错误错误，返回值是{}".format(r.text)

    @allure.feature('test_account_010 登录黑名单账号')
    def test_account_010(self):
        data = {
            "username": "yuk3e@cabital23.com",
            "password": "A!2123123"
        }
        r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'ACC_LOGIN_000001' in r.text, "登录已经注册账号密码错误错误，返回值是{}".format(r.text)

    @allure.feature('test_account_011 刷新账户token')
    def test_account_011(self):
        """
        test_account_011 拿到原来的token
        """
        refreshToken = AccountFunction.get_account_token(account='yuk3e@cabital.com', password="A!234sdfg")['refreshToken']
        data = {
            "refreshToken": refreshToken
        }
        r = requests.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accessToken' in r.text, "刷新账户token错误，返回值是{}".format(r.text)

    @allure.feature('test_account_012 用错误的token刷新token')
    def test_account_012(self):
        """
        test_account_012 拿到原来的token
        """
        data = {
            "refreshToken": "123"
        }
        r = requests.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 401, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'ACC_LOGIN_000003' in r.text, "用错误的token刷新token错误，返回值是{}".format(r.text)

    @allure.feature('test_account_013 用空的token刷新token')
    def test_account_013(self):
        """
        test_account_013 拿到原来的token
        """
        data = {
            "refreshToken": ""
        }
        r = requests.request('POST', url='{}/account/user/refreshToken'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'COMMON_000006' in r.text, "用空的token刷新token错误，返回值是{}".format(r.text)

    @allure.feature('test_account_014 修改密码')
    def test_account_014(self):
        """
        test_account_014 拿到原来的access_token 放入header中
        """
        accessToken = AccountFunction.get_account_token(account='yuk3e@cabital.com', password="A!234sdfg")['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        data = {
            "original": "A!234sdfg",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "修改密码错误，返回值是{}".format(r.text)

    @allure.feature('test_account_015 修改密码使用错误token')
    def test_account_015(self):
        headers['Authorization'] = "Bearer " + "accessToken"
        data = {
            "original": "A!234sdfg",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 401, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.feature('test_account_016 使用错误原始密码修改密码')
    def test_account_016(self):
        """
        test_account_016 拿到原来的access_token 放入header中
        """
        accessToken = AccountFunction.get_account_token(account='yuk3e@cabital.com', password="A!234sdfg")['accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        data = {
            "original": "11111",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/resetPassword'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert "ACC_RESET_000001" in r.text, "使用错误原始密码修改密码错误，返回值是{}".format(r.text)

    @allure.feature('test_account_017 忘记密码验证码')
    def test_account_017(self):
        data = {
            "emailAddress": "yuke@cabital.com"
        }
        r = requests.request('POST', url='{}/account/user/forgetPassword/sendVerificationCode'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "忘记密码验证码错误，返回值是{}".format(r.text)

    @allure.feature('test_account_018 用户未注册忘记密码验证码')
    def test_account_018(self):
        data = {
            "emailAddress": "yuk32131e@cabital.com"
        }
        r = requests.request('POST', url='{}/account/user/forgetPassword/sendVerificationCode'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert "ACC_USER_000002" in r.text, "用户未注册忘记密码验证码错误，返回值是{}".format(r.text)

    @allure.feature('test_account_019 忘记密码')
    def test_account_019(self):
        data = {
            "code": "666666",
            "email": "yuk3e@cabital.com",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "忘记密码错误，返回值是{}".format(r.text)

    @allure.feature('test_account_020 未注册用户忘记密码')
    def test_account_020(self):
        data = {
            "code": "666666",
            "email": "yuk3e@cabita3123l.com",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert "ACC_USER_000002" in r.text, "未注册用户忘记密码错误，返回值是{}".format(r.text)

    @allure.feature('test_account_021 用户忘记密码验证码错误')
    def test_account_021(self):
        data = {
            "code": "166666",
            "email": "yuk3e@cabital.com",
            "password": "A!234sdfg"
        }
        r = requests.request('POST', url='{}/account/user/forgetPassword'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert "ACC_VERIFY_CODE_000001" in r.text, "用户忘记密码验证码错误错误，返回值是{}".format(r.text)

    @allure.feature('test_account_021 查询用户信息')
    def test_account_021(self):
        accessToken = AccountFunction.get_account_token(account='yuk3e@cabital.com', password="A!234sdfg")[
            'accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        r = requests.request('GET', url='{}/account/info'.format(env_url),  headers=headers)
        print(r.json())
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert "user" in r.text, "查询用户信息错误，返回值是{}".format(r.text)

    @allure.feature('test_account_022 修改个人信息')
    def test_account_022(self):
        accessToken = AccountFunction.get_account_token(account='yuk3e@cabital.com', password="A!234sdfg")[
            'accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        data = {
            "firstName": "yuke",
            "lastName": "zhang",
            "dateOfBirth": "1997-12-12",
            "gender": "MALE"
        }
        r = requests.request('POST', url='{}/account/info/personal'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "修改个人信息错误，返回值是{}".format(r.text)

    @allure.feature('test_account_023 修改个人爱好')
    def test_account_023(self):
        accessToken = AccountFunction.get_account_token(account='yuk3e@cabital.com', password="A!234sdfg")[
            'accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        data = {
            "language": "EN",
            "currency": "USD",
            "timeZone": "W11"
        }
        r = requests.request('POST', url='{}/account/setting/preference'.format(env_url),
                             data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "用户忘记密码验证码错误错误，返回值是{}".format(r.text)