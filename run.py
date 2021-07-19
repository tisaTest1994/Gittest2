import os

import pytest
from Function.slack import *
from Function.operate_sql import *


# 选择环境，得到环境url
global env_url
env_url = get_json()[get_json()['env']]

global operateUrl
operateUrl = get_json()['operateUrl']

global headers
headers = get_json()['headers']

global email
email = get_json()['email']

global citizenCountryCodeList
citizenCountryCodeList = get_json()['citizenCountryCodeList']

global accountToken
accountToken = ''

global kyc_type
kyc_type = 'test'


class sessions(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', 5)
        return super(sessions, self).request(*args, **kwargs)


session = sessions()

if __name__ == '__main__':
    os.system('yum install net-tools -y')
    os.system('ifconfig -a')
    # if not os.path.exists('Reports'):
    #     os.makedirs('Reports')
    # pytest.main(['./TestCase/TestApiCase', '-v', '--alluredir', './Reports'])
    # os.system("allure generate ./Reports  -o ./Reports/html --clean")
    # slack_report()
