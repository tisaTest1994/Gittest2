import pytest
import os
from Function.CommonFunction import *

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
    pytest.main(['TestCase/TestApiCase/TestCase.py', '-v', '--alluredir', './Reports'])
    split = "/usr/share/allure generate ./Reports  -o ./Reports/html --clean"
    print(os.system('pwd'))
    print(os.system('type allure'))
    print(os.system('ls -l /usr/bin/allure'))
    print(os.system('ls -l /usr/local/bin/allure'))
    print(os.system('ls -l //usr/share/allure'))
    os.system(split)



