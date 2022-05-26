from Function.api_function import *
from Function.operate_sql import *


# Account相关cases
class TestAccountApi:

    @allure.title('test_account_001')
    @allure.description('注册新用户,用户未被注册')
    def test_account_001(self):
        with allure.step("注册账户"):
            headers['X-Device'] = ''
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

