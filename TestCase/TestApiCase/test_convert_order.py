from Function.api_function import *
import allure
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        time_list = get_zero_time(day_time='2021-05-14')
        cfx_info = []
        for i in time_list:
            info = sqlFunction().get_cfx_detail(end_time=i)
            if info is not None:
                cfx_info.append(info)
        print(cfx_info)