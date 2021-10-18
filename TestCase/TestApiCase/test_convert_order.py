from Function.api_function import *
from Function.operate_sql import *


# convert order相关cases
class TestConvertOrderApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    @pytest.mark.multiprocess
    def test_convert_order_001(self):
        # 获得 cfx_book
        cfx_book = get_json()['cfx_book']
        # 从数据库拿到某日数据
        cfx_info = ApiFunction.get_cfx_info(day_time='2021-05-31')
        # 拆分每一天
        time_info = []
        for i in cfx_info:
            time_info.append(i['order_time'])
        time_info = list(set(time_info))
        for y in time_info:
            # 基准货币数量
            book_profit_dict = {}
            amount_dict = {}
            for x in cfx_book:
                book_profit_dict[x + '_number'] == 0
                amount_dict[x + '_number'] == 0
            for z in cfx_info:
                if y == z['order_time']:
                    for d in cfx_book.values():
                        if z['buy_us'] == str(d).split('-')[0] and z['sell_us'] == str(d).split('-')[1]:
                            book_profit_dict['{}_number'.format(d)] = Decimal(book_profit_dict['{}_number'.format(d)]) - Decimal(z['buy_us_amount'])
                            cost_amount = Decimal(z['buy_us_amount']) * Decimal(z['cost'])
                            if '.' in str(cost_amount):
                                if z['sell_us'] == 'ETH' or z['sell_us'] == 'BTC':
                                    cost_amount = '{}.{}'.format(str(cost_amount).split('.')[0], str(cost_amount).split('.')[1][:8])
                                elif z['sell_us'] == 'USDT':
                                    cost_amount = '{}.{}'.format(str(cost_amount).split('.')[0], str(cost_amount).split('.')[1][:6])
                                else:
                                    cost_amount = '{}.{}'.format(str(cost_amount).split('.')[0], str(cost_amount).split('.')[1][:2])
                            amount_dict['{}_amount'.format(d)] = Decimal(amount_dict['{}_amount'.format(d)]) - Decimal(cost_amount)
                        elif z['buy_us'] == str(d).split('-')[1] and z['sell_us'] == str(d).split('-')[0]:
                            book_profit_dict['{}_number'.format(d)] = Decimal(book_profit_dict['{}_number'.format(d)]) + Decimal(z['sell_us_amount'])
                            cost_amount = Decimal(z['sell_us_amount']) * Decimal(z['cost'])
                            if '.' in str(cost_amount):
                                if z['buy_us'] == 'ETH' or z['buy_us'] == 'BTC':
                                    cost_amount = '{}.{}'.format(str(cost_amount).split('.')[0], str(cost_amount).split('.')[1][:8])
                                elif z['buy_us'] == 'USDT':
                                    cost_amount = '{}.{}'.format(str(cost_amount).split('.')[0], str(cost_amount).split('.')[1][:6])
                                else:
                                    cost_amount = '{}.{}'.format(str(cost_amount).split('.')[0], str(cost_amount).split('.')[1][:2])
                            amount_dict['{}_amount'.format(d)] = Decimal(amount_dict['{}_amount'.format(d)]) + Decimal(cost_amount)
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
                    cfx_order_info = sqlFunction.get_order_info(aggregation_no=y, book_id=x)
                    bybit_rate = cfx_order_info['rate']
                    quote_amount = cfx_order_info['quote_amount']
                    # 第2层损益
                    if str(book_profit_dict['{}_number'.format(cfx_book[x])]) != '0':
                        amount = Decimal(bybit_rate) * Decimal(book_profit_dict['{}_number'.format(cfx_book[x])])
                        if '.' in str(amount):
                            if str(cfx_book[x]).split('-')[1] == 'ETH' or str(cfx_book[x]).split('-')[1] == 'BTC':
                                amount = '{}.{}'.format(str(amount).split('.')[0], str(amount).split('.')[1][:8])
                            elif str(cfx_book[x]).split('-')[1] == 'USDT':
                                amount = '{}.{}'.format(str(amount).split('.')[0], str(amount).split('.')[1][:6])
                            else:
                                amount = '{}.{}'.format(str(amount).split('.')[0], str(amount).split('.')[1][:2])
                        assert Decimal(quote_amount) == - Decimal(amount_dict['{}_amount'.format(cfx_book[x])]), '货币总量数据库反馈是{},计算是{}'.format(quote_amount, Decimal(amount_dict['{}_amount'.format(cfx_book[x])]))
                        logger.info(
                            '第2层损益{}'.format(Decimal(amount) - Decimal(amount_dict['{}_amount'.format(cfx_book[x])])))
                        wallet_info = sqlFunction.get_two_floor('{}:{}'.format(y, x))
                        print(wallet_info)

