from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        # 获得 cfx_book
        cfx_book = get_json()['cfx_book']
        # 从数据库拿到某日数据
        #cfx_info = AccountFunction.get_cfx_info()
        cfx_info = [{'buy_us': 'BTC', 'sell_us': 'ETH', 'buy_us_amount': '0.1486675', 'sell_us_amount': '2.05985186', 'profit': '0.00205779', 'order_time': 1621996380, 'cost': '13.84158659'}, {'buy_us': 'ETH', 'sell_us': 'BTC', 'buy_us_amount': '0.01246212', 'sell_us_amount': '0.00090126', 'profit': '0.00001247', 'order_time': 1621996380, 'cost': '13.84116779'}, {'buy_us': 'BTC', 'sell_us': 'ETH', 'buy_us_amount': '0.00698478', 'sell_us_amount': '0.09730376', 'profit': '0.0000972', 'order_time': 1621996380, 'cost': '13.91689662'}, {'buy_us': 'ETH', 'sell_us': 'BTC', 'buy_us_amount': '0.54615875', 'sell_us_amount': '0.03928477', 'profit': '0.0005467', 'order_time': 1621996380, 'cost': '13.91647356'}, {'buy_us': 'BTC', 'sell_us': 'USDT', 'buy_us_amount': '0.09164082', 'sell_us_amount': '3605.727837', 'profit': '3.602125', 'order_time': 1621996380, 'cost': '39307'}, {'buy_us': 'USDT', 'sell_us': 'BTC', 'buy_us_amount': '23.385875', 'sell_us_amount': '0.00059555', 'profit': '0.023408', 'order_time': 1621996380, 'cost': '39306.5'}, {'buy_us': 'BTC', 'sell_us': 'USDT', 'buy_us_amount': '0.00085489', 'sell_us_amount': '33.636899', 'profit': '0.033603', 'order_time': 1621996440, 'cost': '39307'}, {'buy_us': 'USDT', 'sell_us': 'BTC', 'buy_us_amount': '5929.547387', 'sell_us_amount': '0.15103202', 'profit': '5.935482', 'order_time': 1621996440, 'cost': '39299.5'}, {'buy_us': 'BTC', 'sell_us': 'EUR', 'buy_us_amount': '0.1456557', 'sell_us_amount': '4684.03', 'profit': '4.67', 'order_time': 1621996440, 'cost': '32126.126466'}, {'buy_us': 'EUR', 'sell_us': 'BTC', 'buy_us_amount': '27.64', 'sell_us_amount': '0.00086123', 'profit': '0.02', 'order_time': 1621996440, 'cost': '32125.71811'}, {'buy_us': 'BTC', 'sell_us': 'EUR', 'buy_us_amount': '0.00081098', 'sell_us_amount': '26.08', 'profit': '0.02', 'order_time': 1621996440, 'cost': '32126.126466'}, {'buy_us': 'EUR', 'sell_us': 'BTC', 'buy_us_amount': '1392.01', 'sell_us_amount': '0.04337347', 'profit': '1.39', 'order_time': 1621996440, 'cost': '32125.71811'}, {'buy_us': 'ETH', 'sell_us': 'USDT', 'buy_us_amount': '0.05319855', 'sell_us_amount': '150.500091', 'profit': '0.150349', 'order_time': 1621996440, 'cost': '2826.2'}, {'buy_us': 'USDT', 'sell_us': 'ETH', 'buy_us_amount': '24.130362', 'sell_us_amount': '0.00856771', 'profit': '0.024154', 'order_time': 1621996500, 'cost': '2819.25'}, {'buy_us': 'ETH', 'sell_us': 'USDT', 'buy_us_amount': '0.0106915', 'sell_us_amount': '30.172708', 'profit': '0.030142', 'order_time': 1621996500, 'cost': '2819.3'}, {'buy_us': 'USDT', 'sell_us': 'ETH', 'buy_us_amount': '286.282665', 'sell_us_amount': '0.10164733', 'profit': '0.286569', 'order_time': 1621996500, 'cost': '2819.25'}, {'buy_us': 'ETH', 'sell_us': 'EUR', 'buy_us_amount': '0.16303195', 'sell_us_amount': '376.03', 'profit': '0.37', 'order_time': 1621996500, 'cost': '2304.185494'}, {'buy_us': 'EUR', 'sell_us': 'ETH', 'buy_us_amount': '20.45', 'sell_us_amount': '0.00888419', 'profit': '0.02', 'order_time': 1621996500, 'cost': '2304.144658'}, {'buy_us': 'ETH', 'sell_us': 'EUR', 'buy_us_amount': '0.014386', 'sell_us_amount': '33.16', 'profit': '0.03', 'order_time': 1621996500, 'cost': '2302.715415'}, {'buy_us': 'EUR', 'sell_us': 'ETH', 'buy_us_amount': '246.83', 'sell_us_amount': '0.10730386', 'profit': '0.24', 'order_time': 1621996560, 'cost': '2302.674579'}, {'buy_us': 'USDT', 'sell_us': 'EUR', 'buy_us_amount': '23.805924', 'sell_us_amount': '19.5', 'profit': '0.01', 'order_time': 1621996560, 'cost': '0.818338'}, {'buy_us': 'EUR', 'sell_us': 'USDT', 'buy_us_amount': '32.83', 'sell_us_amount': '40.158038', 'profit': '0.03', 'order_time': 1621996560, 'cost': '0.818338'}, {'buy_us': 'USDT', 'sell_us': 'EUR', 'buy_us_amount': '34.230354', 'sell_us_amount': '28.04', 'profit': '0.02', 'order_time': 1621996560, 'cost': '0.818338'}, {'buy_us': 'EUR', 'sell_us': 'USDT', 'buy_us_amount': '22.99', 'sell_us_amount': '28.130509', 'profit': '0.02', 'order_time': 1621996560, 'cost': '0.818338'}]
        # 拆分每一天
        time_info = []
        for i in cfx_info:
            time_info.append(i['order_time'])
        time_info = list(set(time_info))
        for y in time_info:
            # 基准货币数量
            book_profit_dict = {'BTC-ETH_number': 0, 'BTC-USDT_number': 0, 'BTC-EUR_number': 0, 'ETH-USDT_number': 0, 'ETH-EUR_number': 0, 'USDT-EUR_number': 0}
            # 中间
            amount_dict = {'BTC-ETH_amount': 0, 'BTC-USDT_amount': 0, 'BTC-EUR_amount': 0, 'ETH-USDT_amount': 0, 'ETH-EUR_amount': 0, 'USDT-EUR_amount': 0}
            for z in cfx_info:
                if y == z['order_time']:
                    for d in cfx_book.values():
                        if z['buy_us'] == str(d).split('-')[0] and z['sell_us'] == str(d).split('-')[1]:
                            book_profit_dict['{}_number'.format(d)] = Decimal(book_profit_dict['{}_number'.format(d)]) - Decimal(z['buy_us_amount'])
                            amount_dict['{}_amount'.format(d)] = Decimal(amount_dict['{}_amount'.format(d)]) - Decimal(z['buy_us_amount']) * Decimal(z['cost'])
                        elif z['buy_us'] == str(d).split('-')[1] and z['sell_us'] == str(d).split('-')[0]:
                            book_profit_dict['{}_number'.format(d)] = Decimal(book_profit_dict['{}_number'.format(d)]) + Decimal(z['sell_us_amount'])
                            amount_dict['{}_amount'.format(d)] = Decimal(amount_dict['{}_amount'.format(d)]) + Decimal(z['sell_us_amount']) * Decimal(z['cost'])
                        if '.' in str(amount_dict['{}_amount'.format(d)]):
                            if str(d).split('-')[1] == 'ETH' or str(d).split('-')[1] == 'BTC':
                                amount_dict['{}_amount'.format(d)] = '{}.{}'.format(str(amount_dict['{}_amount'.format(d)]).split('.')[0], str(amount_dict['{}_amount'.format(d)]).split('.')[1][:8])
                            elif str(d).split('-')[1] == 'USDT':
                                amount_dict['{}_amount'.format(d)] = '{}.{}'.format(str(amount_dict['{}_amount'.format(d)]).split('.')[0], str(amount_dict['{}_amount'.format(d)]).split('.')[1][:6])
                            else:
                                amount_dict['{}_amount'.format(d)] = '{}.{}'.format(str(amount_dict['{}_amount'.format(d)]).split('.')[0], str(amount_dict['{}_amount'.format(d)]).split('.')[1][:2])

            # 按照货币对算第1层损益
            for x in cfx_book.keys():
                # 获得数据库中的损益记录
                info = sqlFunction.get_one_floor(aggregation_no=y, book_id=x)
                if info is not None:
                    info = info[0]
                    if info['exposure_direction'] == 1:
                        logger.info('交易对{}在{}时间中要买入{}数量的{}货币'.format(cfx_book[x], y, book_profit_dict['{}_number'.format(cfx_book[x])],str(cfx_book[x]).split('-')[0]))
                        assert Decimal(info['trading_amount']) == book_profit_dict['{}_number'.format(cfx_book[x])], '在{}时间中，{}第一层损益不对'.format(y, book_profit_dict['{}_number'.format(cfx_book[x])])
                    if info['exposure_direction'] == 2:
                        logger.info('交易对{}在{}时间中要卖出{}数量的{}货币'.format(cfx_book[x], y, -book_profit_dict['{}_number'.format(cfx_book[x])], str(cfx_book[x]).split('-')[0]))
                        assert Decimal(info['trading_amount']) == -book_profit_dict['{}_number'.format(cfx_book[x])], '在{}时间中，{}第一层损益不对'.format(y, book_profit_dict['{}_number'.format(cfx_book[x])])
                # 获得bybit利率
                parity = AccountFunction.get_bybit_parities(aggregation_no=y, book_id=x)
                print(parity)
                # 第2层损益
                amount = Decimal(parity) * Decimal(book_profit_dict['{}_number'.format(cfx_book[x])]) - Decimal(amount_dict['{}_amount'.format(cfx_book[x])])
                print('第2层损益{}'.format(amount))