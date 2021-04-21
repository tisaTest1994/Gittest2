import pytest
from Function.slack import *
from Function.common_function import *

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
    pytest.main(['TestCase/TestApiCase', '-n 8', '-v', '--alluredir', './Reports'])
    split = "allure generate ./Reports  -o ./Reports/html --clean"
    os.system(split)
    slack_report()


