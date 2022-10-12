from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api pay in crypto相关 testcases")
class TestPayInCryptoApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()