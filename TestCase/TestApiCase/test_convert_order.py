from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        time_list = get_zero_time(day_time='2021-05-19')
        cfx_info = []
        for i in time_list:
            info = sqlFunction().get_cfx_detail(end_time=i)
            if info is not None:
                 cfx_info.append(info)
        print(cfx_info)
        cfx_list = []
        # for y in cfx_info:
        #     cfx_dict = {}
        #     if y['book_id'] == 1:
        #         profit = Decimal(y['trading_amount']) * (Decimal(y['rate']) - Decimal(y['cost']))
        #         profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #         assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #     elif y['book_id'] == 2:
        #         profit = Decimal(y['trading_amount']) * (Decimal(y['rate']) - Decimal(y['cost']))
        #         profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
        #         assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #         print(profit)
        #         print(y)
        #     elif y['book_id'] == 3:
        #         profit = Decimal(y['trading_amount']) * (Decimal(y['rate']) - Decimal(y['cost']))
        #         profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #         assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #         print(profit)
        #         print(y)
