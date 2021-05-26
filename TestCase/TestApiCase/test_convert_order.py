from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        # cfx_info = AccountFunction.get_cfx_info()
        cfx_info = [{'buy_us': 'BTC', 'sell_us': 'ETH', 'buy_us_amount': '0.1486675', 'sell_us_amount': '2.05985186', 'profit': '0.00205779', 'order_time': 1621996380, 'cost': '13.84158659'}, {'buy_us': 'ETH', 'sell_us': 'BTC', 'buy_us_amount': '0.01246212', 'sell_us_amount': '0.00090126', 'profit': '0.00001247', 'order_time': 1621996380, 'cost': '13.84116779'}, {'buy_us': 'BTC', 'sell_us': 'ETH', 'buy_us_amount': '0.00698478', 'sell_us_amount': '0.09730376', 'profit': '0.0000972', 'order_time': 1621996380, 'cost': '13.91689662'}, {'buy_us': 'ETH', 'sell_us': 'BTC', 'buy_us_amount': '0.54615875', 'sell_us_amount': '0.03928477', 'profit': '0.0005467', 'order_time': 1621996380, 'cost': '13.91647356'}, {'buy_us': 'BTC', 'sell_us': 'USDT', 'buy_us_amount': '0.09164082', 'sell_us_amount': '3605.727837', 'profit': '3.602125', 'order_time': 1621996380, 'cost': '39307'}, {'buy_us': 'USDT', 'sell_us': 'BTC', 'buy_us_amount': '23.385875', 'sell_us_amount': '0.00059555', 'profit': '0.023408', 'order_time': 1621996380, 'cost': '39306.5'}, {'buy_us': 'BTC', 'sell_us': 'USDT', 'buy_us_amount': '0.00085489', 'sell_us_amount': '33.636899', 'profit': '0.033603', 'order_time': 1621996440, 'cost': '39307'}, {'buy_us': 'USDT', 'sell_us': 'BTC', 'buy_us_amount': '5929.547387', 'sell_us_amount': '0.15103202', 'profit': '5.935482', 'order_time': 1621996440, 'cost': '39299.5'}, {'buy_us': 'BTC', 'sell_us': 'EUR', 'buy_us_amount': '0.1456557', 'sell_us_amount': '4684.03', 'profit': '4.67', 'order_time': 1621996440, 'cost': '32126.126466'}, {'buy_us': 'EUR', 'sell_us': 'BTC', 'buy_us_amount': '27.64', 'sell_us_amount': '0.00086123', 'profit': '0.02', 'order_time': 1621996440, 'cost': '32125.71811'}, {'buy_us': 'BTC', 'sell_us': 'EUR', 'buy_us_amount': '0.00081098', 'sell_us_amount': '26.08', 'profit': '0.02', 'order_time': 1621996440, 'cost': '32126.126466'}, {'buy_us': 'EUR', 'sell_us': 'BTC', 'buy_us_amount': '1392.01', 'sell_us_amount': '0.04337347', 'profit': '1.39', 'order_time': 1621996440, 'cost': '32125.71811'}, {'buy_us': 'ETH', 'sell_us': 'USDT', 'buy_us_amount': '0.05319855', 'sell_us_amount': '150.500091', 'profit': '0.150349', 'order_time': 1621996440, 'cost': '2826.2'}, {'buy_us': 'USDT', 'sell_us': 'ETH', 'buy_us_amount': '24.130362', 'sell_us_amount': '0.00856771', 'profit': '0.024154', 'order_time': 1621996500, 'cost': '2819.25'}, {'buy_us': 'ETH', 'sell_us': 'USDT', 'buy_us_amount': '0.0106915', 'sell_us_amount': '30.172708', 'profit': '0.030142', 'order_time': 1621996500, 'cost': '2819.3'}, {'buy_us': 'USDT', 'sell_us': 'ETH', 'buy_us_amount': '286.282665', 'sell_us_amount': '0.10164733', 'profit': '0.286569', 'order_time': 1621996500, 'cost': '2819.25'}, {'buy_us': 'ETH', 'sell_us': 'EUR', 'buy_us_amount': '0.16303195', 'sell_us_amount': '376.03', 'profit': '0.37', 'order_time': 1621996500, 'cost': '2304.185494'}, {'buy_us': 'EUR', 'sell_us': 'ETH', 'buy_us_amount': '20.45', 'sell_us_amount': '0.00888419', 'profit': '0.02', 'order_time': 1621996500, 'cost': '2304.144658'}, {'buy_us': 'ETH', 'sell_us': 'EUR', 'buy_us_amount': '0.014386', 'sell_us_amount': '33.16', 'profit': '0.03', 'order_time': 1621996500, 'cost': '2302.715415'}, {'buy_us': 'EUR', 'sell_us': 'ETH', 'buy_us_amount': '246.83', 'sell_us_amount': '0.10730386', 'profit': '0.24', 'order_time': 1621996560, 'cost': '2302.674579'}, {'buy_us': 'USDT', 'sell_us': 'EUR', 'buy_us_amount': '23.805924', 'sell_us_amount': '19.5', 'profit': '0.01', 'order_time': 1621996560, 'cost': '0.818338'}, {'buy_us': 'EUR', 'sell_us': 'USDT', 'buy_us_amount': '32.83', 'sell_us_amount': '40.158038', 'profit': '0.03', 'order_time': 1621996560, 'cost': '0.818338'}, {'buy_us': 'USDT', 'sell_us': 'EUR', 'buy_us_amount': '34.230354', 'sell_us_amount': '28.04', 'profit': '0.02', 'order_time': 1621996560, 'cost': '0.818338'}, {'buy_us': 'EUR', 'sell_us': 'USDT', 'buy_us_amount': '22.99', 'sell_us_amount': '28.130509', 'profit': '0.02', 'order_time': 1621996560, 'cost': '0.818338'}]
        time_info = []
        for i in cfx_info:
            time_info.append(i['order_time'])
        time_info = list(set(time_info))
        for y in time_info:
            # sql = "select book_id from book_aggregation where aggregation_no = '{}';".format(y)
            # book_id = sqlFunction().connect_mysql('hedging', sql=sql)[0]['book_id']
            # biz_id = '{}:{}'.format(y, book_id)
            # sql = "select rate from cfxorder.order where biz_id='{}';".format(biz_id)
            # rate = sqlFunction().connect_mysql('cfxorder', sql=sql)[0]['rate']
            # print(rate)
            BTC_ETH_number = 0
            BTC_USDT_number = 0
            BTC_EUR_number = 0
            ETH_USDT_number = 0
            ETH_EUR_number = 0
            USDT_EUR_number = 0
            for z in cfx_info:
                if y == z['order_time']:
                    if z['buy_us'] == 'BTC' and z['sell_us'] == 'ETH':
                        BTC_ETH_number = Decimal(BTC_ETH_number) - Decimal(z['buy_us_amount'])
                    elif z['buy_us'] == 'ETH' and z['sell_us'] == 'BTC':
                        BTC_ETH_number = Decimal(BTC_ETH_number) + Decimal(z['sell_us_amount'])
                    elif z['buy_us'] == 'BTC' and z['sell_us'] == 'USDT':
                        BTC_USDT_number = Decimal(BTC_USDT_number) - Decimal(z['buy_us_amount'])
                    elif z['buy_us'] == 'USDT' and z['sell_us'] == 'BTC':
                        BTC_USDT_number = Decimal(BTC_USDT_number) + Decimal(z['sell_us_amount'])
                    elif z['buy_us'] == 'ETH' and z['sell_us'] == 'USDT':
                        ETH_USDT_number = Decimal(ETH_USDT_number) - Decimal(z['buy_us_amount'])
                    elif z['buy_us'] == 'USDT' and z['sell_us'] == 'ETH':
                        ETH_USDT_number = Decimal(ETH_USDT_number) + Decimal(z['sell_us_amount'])
                    elif z['buy_us'] == 'BTC' and z['sell_us'] == 'EUR':
                        BTC_EUR_number = Decimal(BTC_EUR_number) - Decimal(z['buy_us_amount'])
                    elif z['buy_us'] == 'EUR' and z['sell_us'] == 'BTC':
                        BTC_EUR_number = Decimal(BTC_EUR_number) + Decimal(z['sell_us_amount'])
                    elif z['buy_us'] == 'ETH' and z['sell_us'] == 'EUR':
                        ETH_EUR_number = Decimal(ETH_EUR_number) - Decimal(z['buy_us_amount'])
                    elif z['buy_us'] == 'EUR' and z['sell_us'] == 'ETH':
                        ETH_EUR_number = Decimal(ETH_EUR_number) + Decimal(z['sell_us_amount'])
                    elif z['buy_us'] == 'USDT' and z['sell_us'] == 'EUR':
                        USDT_EUR_number = Decimal(USDT_EUR_number) - Decimal(z['buy_us_amount'])
                    elif z['buy_us'] == 'EUR' and z['sell_us'] == 'USDT':
                        USDT_EUR_number = Decimal(USDT_EUR_number) + Decimal(z['sell_us_amount'])
            info = sqlFunction.get_one_floor(aggregation_no=y, book_id=1)
            if info['exposure_direction'] == 1:
                logger.info('BTC-USDT在{}时间断内需要卖出{}的BTC'.format(y, BTC_USDT_number))
                assert Decimal(info['trading_amount']) == BTC_USDT_number, 'BTC_ETH_number error'
            elif info['exposure_direction'] == 2:
                logger.info('BTC-USDT在{}时间断内需要买入{}的BTC'.format(y, -BTC_USDT_number))
                assert -Decimal(info['trading_amount']) == BTC_USDT_number, 'BTC_ETH_number error'

            # logger.info('BTC-ETH在{}时间断内需要卖出{}的BTC'.format(y, BTC_ETH_number))
            # logger.info('BTC-USDT在{}时间断内需要卖出{}的BTC'.format(y, BTC_USDT_number))
            # logger.info('BTC-EUR在{}时间断内需要卖出{}的BTC'.format(y, BTC_EUR_number))
            # logger.info('ETH-USDT在{}时间断内需要卖出{}的BTC'.format(y, ETH_USDT_number))
            # logger.info('ETH-EUR在{}时间断内需要卖出{}的ETH'.format(y, ETH_EUR_number))
            # logger.info('USDT-EUR在{}时间断内需要卖出{}的USDT'.format(y, USDT_EUR_number))