from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        cfx_info = AccountFunction.get_cfx_info()
        time_info = []
        for i in cfx_info:
            time_info.append(i['order_time'])
        time_info = list(set(time_info))
        for y in time_info:
            sql = "select book_id from book_aggregation where aggregation_no = '{}';".format(y)
            book_id = sqlFunction().connect_mysql('hedging', sql=sql)[0]['book_id']
            biz_id = '{}:{}'.format(y, book_id)
            sql = "select rate from order where biz_id='{}';".format(biz_id)
            print(sql)
            rate = sqlFunction().connect_mysql('cfxorder', sql=sql)
            print(rate)
            BTC_number = 0
            ETH_number = 0
            BTC_number_two_profit = 0
            ETH_number_two_profit = 0
            for z in cfx_info:
                if y == z['order_time']:
                    if z['buy_us'] == 'BTC' and z['sell_us'] == 'ETH':
                        BTC_number = Decimal(BTC_number) - Decimal(z['buy_us_amount'])
                        ETH_number_two_profit = Decimal(z['cost'])
                    elif z['buy_us'] == 'ETH' and z['sell_us'] == 'BTC':
                        BTC_number = Decimal(BTC_number) + Decimal(z['sell_us_amount'])
                    elif z['buy_us'] == 'BTC' and z['sell_us'] == 'USDT':
                        BTC_number = Decimal(BTC_number) - Decimal(z['buy_us_amount'])
                    elif z['buy_us'] == 'USDT' and z['sell_us'] == 'BTC':
                        BTC_number = Decimal(BTC_number) + Decimal(z['sell_us_amount'])
                    elif z['buy_us'] == 'ETH' and z['sell_us'] == 'USDT':
                        ETH_number = Decimal(ETH_number) - Decimal(z['buy_us_amount'])
                    elif z['buy_us'] == 'USDT' and z['sell_us'] == 'ETH':
                        ETH_number = Decimal(ETH_number) + Decimal(z['sell_us_amount'])
            logger.info('在{}时间断内需要卖出{}的BTC'.format(y, BTC_number))
            logger.info('在{}时间断内需要卖出{}的ETH'.format(y, ETH_number))

    # @allure.testcase('test_convert_order_002 根据id编号查询单笔交易')
    # def test_convert_order_002(self):
    #     cfx_info = AccountFunction.get_cfx_info()
    #     time_info = []
    #     for i in cfx_info:
    #         time_info.append(i['order_time'])
    #     time_info = list(set(time_info))
    #     for y in time_info:
    #         BTC_number = 0
    #         ETH_number = 0
    #         for z in cfx_info:
    #             if y == z['order_time']:
    #                 if z['buy_us'] == 'BTC' and z['sell_us'] == 'ETH':
    #                     BTC_number = Decimal(BTC_number) - Decimal(z['buy_us_amount'])
    #                 elif z['buy_us'] == 'ETH' and z['sell_us'] == 'BTC':
    #                     BTC_number = Decimal(BTC_number) + Decimal(z['sell_us_amount'])
    #                 elif z['buy_us'] == 'BTC' and z['sell_us'] == 'USDT':
    #                     BTC_number = Decimal(BTC_number) - Decimal(z['buy_us_amount'])
    #                 elif z['buy_us'] == 'USDT' and z['sell_us'] == 'BTC':
    #                     BTC_number = Decimal(BTC_number) + Decimal(z['sell_us_amount'])
    #                 elif z['buy_us'] == 'ETH' and z['sell_us'] == 'USDT':
    #                     ETH_number = Decimal(ETH_number) - Decimal(z['buy_us_amount'])
    #                 elif z['buy_us'] == 'USDT' and z['sell_us'] == 'ETH':
    #                     ETH_number = Decimal(ETH_number) + Decimal(z['sell_us_amount'])
    #         logger.info('在{}时间断内需要卖出{}的BTC'.format(y, BTC_number))
    #         logger.info('在{}时间断内需要卖出{}的ETH'.format(y, ETH_number))
    #         sql = "select book_id from book_aggregation where aggregation_no = '{}'".format(y)
    #         book_id = sqlFunction().connect_mysql('hedging', sql=sql)
    #         biz_id = '{}:{}'.format(y, book_id)
    #         sql = "select rate from order where biz_id='{}'".format(biz_id)
    #         rate = book_id = sqlFunction().connect_mysql('cfxorder', sql=sql)
    #         if BTC_number >= 0:
    #             rate