from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        time_list = get_zero_time(day_time='2021-05-20')
        cfx_info = {}
        for i in time_list:
            info = sqlFunction().get_cfx_detail(end_time=i)
            if info is not None and '()' not in str(info):
                 cfx_info[i] = info
        print(cfx_info)
        # cfx_info = [[{'id': 344, 'deal_no': '8e594e34-852e-4b58-9ee5-a9847c369fa4', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 20, 5, 26, 19), 'transaction_time': datetime.datetime(2021, 5, 20, 5, 26, 20), 'trading_amount': '0.01', 'pnl_amount': '392.002605', 'rate': '39200.2605', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621488420, 'gnl': '0.392395', 'cost': '39239.5'}], [{'id': 345, 'deal_no': 'd0542635-89b2-46e9-98ff-cfeb5a017198', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 20, 6, 16, 19), 'transaction_time': datetime.datetime(2021, 5, 20, 6, 16, 19), 'trading_amount': '1', 'pnl_amount': '15.16727395', 'rate': '15.16727395', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621491420, 'gnl': '0.01518246', 'cost': '15.18245641'}, {'id': 346, 'deal_no': 'ea4e6f5a-db99-4f3a-8653-aa44abb7a89a', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 20, 6, 16, 36), 'transaction_time': datetime.datetime(2021, 5, 20, 6, 16, 37), 'trading_amount': '0.19759244', 'pnl_amount': '3', 'rate': '15.18276697', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621491420, 'gnl': '0.002997', 'cost': '15.16759937'}], [{'id': 347, 'deal_no': '206e5e50-f134-4c2e-83da-b643a6a12fe5', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 20, 6, 17, 39), 'transaction_time': datetime.datetime(2021, 5, 20, 6, 17, 40), 'trading_amount': '0.01149488', 'pnl_amount': '30', 'rate': '2609.85725', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621491480, 'gnl': '0.02997', 'cost': '2607.25'}, {'id': 348, 'deal_no': '3041fa13-9087-4bb6-87d7-ddc7bf16a417', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 20, 6, 17, 56), 'transaction_time': datetime.datetime(2021, 5, 20, 6, 17, 57), 'trading_amount': '0.01775746', 'pnl_amount': '700', 'rate': '39420.0405', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621491480, 'gnl': '0.7007', 'cost': '39459.5'}]]
        # cfx_list = []
        # for y in cfx_info:
        #     for z in y:
        #         cfx_dict = {}
        #         if z['book_id'] == 1:
        #             if z['trading_direction'] == 1:
        #                 cfx_dict['buy_us'] = 'USDT'
        #                 cfx_dict['sell_us'] = 'BTC'
        #                 cfx_dict['buy_us_amount'] = z['pnl_amount']
        #                 cfx_dict['sell_us_amount'] = z['trading_amount']
        #                 cfx_dict['profit'] = z['gnl']
        #                 profit = Decimal(z['trading_amount']) * (Decimal(z['cost']) - Decimal(z['rate']))
        #                 profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #                 assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #             elif z['trading_direction'] == 2:
        #                 cfx_dict['buy_us'] = 'BTC'
        #                 cfx_dict['sell_us'] = 'USDT'
        #                 cfx_dict['buy_us_amount'] = z['trading_amount']
        #                 cfx_dict['sell_us_amount'] = z['pnl_amount']
        #                 cfx_dict['profit'] = z['gnl']
        #                 profit = Decimal(z['trading_amount']) * (Decimal(z['rate']) - Decimal(z['cost']))
        #                 profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #                 btc_number = btc_number + float(z['trading_amount'])
        #                 assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #         elif z['book_id'] == 2:
        #             if z['trading_direction'] == 1:
        #                 cfx_dict['buy_us'] = 'ETH'
        #                 cfx_dict['sell_us'] = 'BTC'
        #                 cfx_dict['buy_us_amount'] = z['pnl_amount']
        #                 cfx_dict['sell_us_amount'] = z['trading_amount']
        #                 cfx_dict['profit'] = z['gnl']
        #                 profit = Decimal(z['trading_amount']) * (Decimal(z['cost']) - Decimal(z['rate']))
        #                 profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
        #                 assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, z['gnl'])
        #             elif z['trading_direction'] == 2:
        #                 cfx_dict['buy_us'] = 'BTC'
        #                 cfx_dict['sell_us'] = 'ETH'
        #                 cfx_dict['buy_us_amount'] = z['trading_amount']
        #                 cfx_dict['sell_us_amount'] = z['pnl_amount']
        #                 cfx_dict['profit'] = z['gnl']
        #                 profit = Decimal(z['trading_amount']) * (Decimal(z['rate']) - Decimal(z['cost']))
        #                 profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
        #                 assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, z['gnl'])
        #         elif z['book_id'] == 3:
        #             if z['trading_direction'] == 1:
        #                 cfx_dict['buy_us'] = 'USDT'
        #                 cfx_dict['sell_us'] = 'ETH'
        #                 cfx_dict['buy_us_amount'] = z['pnl_amount']
        #                 cfx_dict['sell_us_amount'] = z['trading_amount']
        #                 cfx_dict['profit'] = z['gnl']
        #                 profit = Decimal(z['trading_amount']) * (Decimal(z['cost']) - Decimal(z['rate']))
        #                 profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #                 assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, z['gnl'])
        #             elif z['trading_direction'] == 2:
        #                 cfx_dict['buy_us'] = 'ETH'
        #                 cfx_dict['sell_us'] = 'USDT'
        #                 cfx_dict['buy_us_amount'] = z['trading_amount']
        #                 cfx_dict['sell_us_amount'] = z['pnl_amount']
        #                 cfx_dict['profit'] = z['gnl']
        #                 profit = Decimal(z['trading_amount']) * (Decimal(z['rate']) - Decimal(z['cost']))
        #                 profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
        #                 assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, y['gnl'])
        #         cfx_list.append(cfx_dict)
        #
        # print(cfx_list)