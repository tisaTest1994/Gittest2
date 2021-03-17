import requests
import allure
import pytest
from run import *

global headers
headers = {
    'Content-Type': 'application/json',
    'Content-Encoding': 'deflate'
}


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
        assert 'accessToken' in r.text, "成功注册用户错误，返回值是{}".format(r.json())

    @allure.feature('test_account_002 用户已经存在')
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
        assert 'ACC_REGISTRY_000002' in r.text, "成功注册用户错误，返回值是{}".format(r.json())

    @allure.feature('test_account_003 验证码错误')
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
        assert 'COMMON_000006' in r.text, "成功注册用户错误，返回值是{}".format(r.json())

    @allure.feature('test_account_004 申请注册验证码')
    def test_account_004(self):
        data = {
            "emailAddress": generate_email(),
        }
        r = requests.request('POST', url='{}/account/user/signUp/sendVerificationCode'.format(env_url),
                             data=json.dumps(data), headers=headers)
        print(r.json())
        #assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        #assert 'COMMON_000006' in r.text, "成功注册用户错误，返回值是{}".format(r.json())
