import pytest
from Function.slack import *
from Function.operate_sql import *
from time import sleep


# 选择环境，得到环境url
global env_url
env_url = get_json()[get_json()['env']]

global headers
headers = get_json()['headers']

global email
email = get_json()['email']

global citizenCountryCodeList
citizenCountryCodeList = get_json()['citizenCountryCodeList']

global accountToken
accountToken = ''


class sessions(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', 5)
        return super(sessions, self).request(*args, **kwargs)


session = sessions()

if __name__ == '__main__':
    if not os.path.exists('Reports'):
        os.makedirs('Reports')
    pytest.main(['TestCase/TestApiCase/test_payout.py', '-v', '--alluredir', './Reports'])
    os.system("allure generate ./Reports  -o ./Reports/html --clean")
    slack_report()

