from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        time_list = get_zero_time(day_time='2021-05-20')
        cfx_info = []
        for i in time_list:
            info = sqlFunction().get_cfx_detail(end_time=i)
            print(info)
            if info is not None:
                 cfx_info.append(info)
        print(cfx_info)
        # cfx_info = [{'id': 343, 'deal_no': 'cbe6e290-11e9-45d2-ad2b-200836c222b5', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 19, 8, 42, 25), 'transaction_time': datetime.datetime(2021, 5, 19, 8, 42, 25), 'trading_amount': '0.00671033', 'pnl_amount': '20', 'rate': '2980.4775', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621413780, 'gnl': '0.006559', 'cost': '2979.5'}]
        # cfx_list = []
        # btc_number = 0
        # eth_number = 0
        # for y in cfx_info:
        #     cfx_dict = {}
        #     if y['book_id'] == 1:
        #         profit = Decimal(y['trading_amount']) * (Decimal(y['rate']) - Decimal(y['cost']))
        #         profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #         btc_number = btc_number + float(y['trading_amount'])
        #         print(profit)
        #         print(y)
        #         assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #     elif y['book_id'] == 2:
        #         profit = Decimal(y['trading_amount']) * (Decimal(y['rate']) - Decimal(y['cost']))
        #         profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
        #         eth_number = eth_number + float(y['trading_amount'])
        #         assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #         print(profit)
        #         print(y)
        #     elif y['book_id'] == 3:
        #         profit = Decimal(y['trading_amount']) * (Decimal(y['rate']) - Decimal(y['cost']))
        #         profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #         btc_number = btc_number + float(y['trading_amount'])
        #         assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #         print(profit)
        #         print(y)
        # print(btc_number)
        # print(eth_number)