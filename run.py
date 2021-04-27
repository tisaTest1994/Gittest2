import pytest
from Function.slack import *
from Function.common_function import *
from Function.connect_mysql import *

# 选择环境，得到环境url
global env_url
env_url = get_json()[get_json()['env']]

global headers
headers = get_json()['headers']

global email
email = get_json()['email']

global citizenCountryCodeList
citizenCountryCodeList = get_json()['citizenCountryCodeList']


if __name__ == '__main__':
    connect_mysql('account', 'select * from account.account where account_id = "6cdfb1da-7646-4806-9a6a-445101928dc6";')
    # pytest.main(['TestCase/TestApiCase', '-n 8', '-v', '--alluredir', './Reports'])
    # split = "allure generate ./Reports  -o ./Reports/html --clean"
    # os.system(split)
    # slack_report()


