from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        cfx_info = AccountFunction.get_cfx_info()
        print(cfx_info)
