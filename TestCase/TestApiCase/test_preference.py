from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api preference 相关 testcases")
class TestPreferenceApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_preference_001')
    @allure.description('获取用户偏好信息')
    def test_preference_001(self):
        with allure.step("获取用户偏好信息"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'language' in r.json().keys(), "获取用户偏好信息失败，返回值是{}".format(r.text)
            assert 'currency' in r.json().keys(), "获取用户偏好信息失败，返回值是{}".format(r.text)

    @allure.title('test_preference_002')
    @allure.description('修改用户偏好信息')
    def test_preference_002(self):
        with allure.step("获取用户偏好信息"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            data = r.json()
        with allure.step("修改用户偏好信息"):
            data1 = {
                "language": "zh_CN",
                "currency": "GBP",
                "timeZone": "Asia/shanghai"
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data1), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "获取用户偏好信息失败，返回值是{}".format(r.text)
        with allure.step("检查用户偏好信息已经被修改"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            assert r.json()['currency'] == 'GBP', "修改用户偏好信息失败，返回值是{}".format(r.text)
        with allure.step("恢复之前的用户偏好信息"):
            session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)

    @allure.title('test_preference_003')
    @allure.description('修改用户偏好信息使用缺失信息')
    def test_preference_003(self):
        with allure.step("获取用户偏好信息"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            data = r.json()
        with allure.step("修改用户偏好信息"):
            data1 = {
                "currency": "GBP",
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data1), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "获取用户偏好信息失败，返回值是{}".format(r.text)
        with allure.step("检查用户偏好信息已经被修改"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            assert r.json()['currency'] == 'GBP', "修改用户偏好信息失败，返回值是{}".format(r.text)
        with allure.step("恢复之前的用户偏好信息"):
            session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)

    @allure.title('test_preference_004')
    @allure.description('上传push相关token信息')
    def test_preference_004(self):
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
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "上传push相关token信息失败，返回值是{}".format(r.text)

    @allure.title('test_preference_005')
    @allure.description('修改nickname')
    def test_preference_005(self):
        with allure.step("修改nickname"):
            data = {
                "nickname": "ad!@d😄我940!2342"
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "修改nickname错误，返回值是{}".format(r.text)
        with allure.step("获取用户偏好信息"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['nickname'] == "ad!@d😄我940!2342", "获取nickname失败，返回值是{}".format(r.text)

    @allure.title('test_preference_006')
    @allure.description('修改nickname长度超过20')
    def test_preference_006(self):
        with allure.step("修改nickname"):
            data = {
                "nickname": "ads157!934！#！@*#**#！2940我2342"
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['message'] == 'invalid nickname', "修改nickname错误，返回值是{}".format(r.text)

    @allure.title('test_preference_007')
    @allure.description('打开/关闭notification推送')
    def test_preference_007(self):
        with allure.step("打开notification推送"):
            data = {
                "notification_setting": {
                    "push_switch": 1
                }
            }
            r = session.request('PUT', url='{}/preference/account/setting'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "打开/关闭notification推送错误，返回值是{}".format(r.text)