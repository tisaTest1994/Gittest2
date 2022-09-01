from Function.api_function import *
from Function.operate_sql import *


# Convert相关cases
class TestConvertApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()


