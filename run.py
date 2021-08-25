import pytest
from Function.slack import *
from Function.operate_sql import *

# 初始化参数

# 通过修改配置文件中的env修改测试or生产环境
global env_url
env_url = get_json()[get_json()['env']]

# operate 环境
global operateUrl
operateUrl = get_json()['operateUrl']

# 提供给monitor
global monitorUrl
monitorUrl = get_json()['monitorUrl']

# headers
global headers
headers = get_json()['headers']

global email
email = get_json()['email']

global citizenCountryCodeList
citizenCountryCodeList = get_json()['citizenCountryCodeList']

global accountToken
accountToken = ''

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
    pytest.main(['./TestCase/TestApiCase', '-v', '--alluredir', './Reports'])
    # pytest.main(['./TestCase/TestAndroidCase', '-v', '--alluredir', './Reports'])
    os.system("allure generate ./Reports  -o ./Reports/html --clean")
    slack_report()
