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

    split = "/usr/bin/allure generate ./Reports  -o ./Reports/html --clean"
    print(os.system('pwd'))
    os.system(split)



