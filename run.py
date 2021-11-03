import pytest
import hmac
import base64
import http.client
import time
import allure
import pyotp
import uuid
import sys
from Function.slack import *
from Function.log import *
from decimal import *
from urllib.parse import urlencode
from time import sleep
from hashlib import sha256
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# 初始化参数

# 通过修改配置文件中的env修改测试or生产环境
global env_url
env_url = get_json()[get_json()['env']]

# operate 环境
global operateUrl
operateUrl = get_json()['operateUrl']

# headers
global headers
headers = get_json()['headers']

global package_name
package_name = get_json()['app_package'][get_json()['env']]


class sessions(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', 5)
        return super(sessions, self).request(*args, **kwargs)


session = sessions()

if __name__ == '__main__':
    if not os.path.exists('Reports'):
        os.makedirs('Reports')
    if sys.argv[1] == 'api':
        pytest.main(['./TestCase/TestApiCase/test_convert.py', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == 'kyc':
        pytest.main(['./TestCase/TestComplianceServiceCase', '--alluredir', './Reports', '--clean-alluredir', '--timeout=600'])
    elif sys.argv[1] == "ui":
        pytest.main(['./TestCase/TestAndroidCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    elif sys.argv[1] == "cabinet":
        pytest.main(['./TestCase/TestCabinetCase', '-v', '--alluredir', './Reports', '--clean-alluredir'])
    else:
        assert False, 'error 需要传入正确的参数'
    os.system("allure generate ./Reports  -o ./Reports/html --clean")
    slack_report(type=sys.argv[1])
