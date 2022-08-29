import pytest
import hmac
import base64
import http.client
import time
import allure
import pyotp
import uuid
import sys
import ssl
import uuid
from Function.slack import *
from Function.log import *
from decimal import *
from urllib.parse import urlencode
from time import sleep
from hashlib import sha256

ssl._create_default_https_context = ssl._create_unverified_context


# 初始化参数
# 通过修改配置文件中的env修改测试or生产环境
global env_url
env_url = get_json()[get_json()['env']]

# operate 环境
global operateUrl
operateUrl = get_json()['operateUrl']

global connect_url
connect_url = get_json()['url_list']['connect']

# headers
global headers
headers = get_json()['headers']

global package_name
package_name = get_json()['app_package'][get_json()['env']]

global connect_header
connect_header = get_json()['connect'][get_json()['env']]['bybit']['Headers']

global compliance_service_type
compliance_service_type = 'test'


class sessions(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', 10)
        return super(sessions, self).request(*args, **kwargs)


session = sessions()

if __name__ == '__main__':
    # 更新 mms
    get_language_map(type='app')
    get_language_map(type='web')
    get_language_map(type='email')
    if not os.path.exists('Reports'):
        os.makedirs('Reports')
    # 修改默认语言
    if sys.argv[2] is not None:
        if sys.argv[1] != 'kyc':
            write_json('language', sys.argv[2])
    # run
    if sys.argv[1] == 'api':
        pytest.main(['./TestCase/TestApiCase/', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == 'kyc':
        if sys.argv[1] != 'test':
            compliance_service_type = 'pro'
        pytest.main(['./TestCase/TestComplianceServiceCase', '-v', '--alluredir', './Reports', '--clean-alluredir', '--timeout=600'])
    elif sys.argv[1] == "app":
        pytest.main(['./TestCase/TestAndroidCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "cabinet":
        pytest.main(['./TestCase/TestCabinetCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "bybit":
        pytest.main(['./TestCase/TestBybitCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "web":
        pytest.main(['./TestCase/TestWebCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "accounting":
        pytest.main(['./TestCase/TestAccountingCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "infinni":
        pytest.main(['./TestCase/TestInfinniGamesCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "widget":
        pytest.main(['./TestCase/TestWidgetCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "pay":
        pytest.main(['./TestCase/TestCabitalPayCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "connect":
        pytest.main(['./TestCase/TestCabitalConnectCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    else:
        assert False, 'error 需要传入正确的参数'
    os.system("allure generate ./Reports  -o ./Reports/html --clean")
    slack_report(type=sys.argv[1], env=sys.argv[2])
