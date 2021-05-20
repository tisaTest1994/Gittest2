from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        sl = "select * from book_detail where created_at >= '2021-05-20 06:16:00' and created_at < '2021-05-20 06:17:00';"
        info = sqlFunction().connect_mysql('hedging', sql=sl)
        print(info)
        # time_list = get_zero_time(day_time='2021-05-20')
        # cfx_info = []
        # for i in time_list:
        #     info = sqlFunction().get_cfx_detail(end_time=i)
        #     print(info)
        #     if info is not None:
        #          cfx_info.append(info)
        # print(cfx_info)
        # cfx_info = [{'id': 344, 'deal_no': '8e594e34-852e-4b58-9ee5-a9847c369fa4', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 20, 5, 26, 19), 'transaction_time': datetime.datetime(2021, 5, 20, 5, 26, 20), 'trading_amount': '0.01', 'pnl_amount': '392.002605', 'rate': '39200.2605', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621488420, 'gnl': '0.392395', 'cost': '39239.5'}, {'id': 345, 'deal_no': 'd0542635-89b2-46e9-98ff-cfeb5a017198', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 20, 6, 16, 19), 'transaction_time': datetime.datetime(2021, 5, 20, 6, 16, 19), 'trading_amount': '1', 'pnl_amount': '15.16727395', 'rate': '15.16727395', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621491420, 'gnl': '0.01518246', 'cost': '15.18245641'}, {'id': 347, 'deal_no': '206e5e50-f134-4c2e-83da-b643a6a12fe5', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 20, 6, 17, 39), 'transaction_time': datetime.datetime(2021, 5, 20, 6, 17, 40), 'trading_amount': '0.01149488', 'pnl_amount': '30', 'rate': '2609.85725', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621491480, 'gnl': '0.02997', 'cost': '2607.25'}]
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
        #         #assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #     elif y['book_id'] == 2:
        #         profit = Decimal(y['trading_amount']) * (Decimal(y['rate']) - Decimal(y['cost']))
        #         profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
        #         eth_number = eth_number + float(y['trading_amount'])
        #         #assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #         print(profit)
        #         print(y)
        #     elif y['book_id'] == 3:
        #         profit = Decimal(y['trading_amount']) * (Decimal(y['rate']) - Decimal(y['cost']))
        #         profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #         btc_number = btc_number + float(y['trading_amount'])
        #         #assert profit == y['gnl'], '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #         print(profit)
        #         print(y)
        # print(btc_number)
        # print(eth_number)