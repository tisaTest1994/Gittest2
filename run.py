import pytest
import os
from Function.CommonFunction import *

# 选择环境，得到环境url
global env_url
env_url = get_json()[get_json()['env']]


if __name__ == '__main__':
    pytest.main(['TestCase/TestApiCase/TestCase.py', '-v', '--alluredir', './Reports'])

