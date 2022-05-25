from Function.api_function import *
from Function.operate_sql import *


# Account相关cases
class TestAccountApi:

    url = get_json()['connect'][get_json()['env']]['url']
