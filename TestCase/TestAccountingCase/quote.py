from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("Quote 相关 testcases")
class TestQuoteApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
    #
    # @allure.title('test_quote_001')
    # @allure.description('校验cfx汇率增加的浮点')
    # def test_quote_001(self):
    #     cfx1_list = []
    #     with allure.step("获取当前UTC时间"):
    #         day_time = (datetime.now(tz=pytz.timezone('UTC'))).strftime("%Y%m%d")
    #     with allure.step("获取全部换汇币种对"):
    #         # cfx_list = ApiFunction.get_cfx_list()
    #         # for i in cfx_list:
    #         #     sql = "select bid, ask, original_bid, original_ask, extra from quote_{} where pair = '{}' and purpose = 'Customer' limit 1;".format(
    #         #         day_time, i)
    #         #     logger.info('sql命令是{}'.format(sql))
    #         #     quote = (sqlFunction().connect_mysql('pricing', sql=sql))[0]
    #         #     logger.info('汇率list是{}'.format(quote))
    #             quote = {'bid': '12.456988652518', 'ask': '12.658495579796', 'original_bid': '12.557448238426', 'original_ask': '12.558031329163', 'extra': '{"origins":[{"formalized_data_id":69449,"bid":"24290.5","ask":"24291","middle":"24290.75","provider":1,"origin_create_time":1660521567,"weight":100,"pair":"BTC-USDT"},{"formalized_data_id":69450,"bid":"1934.3","ask":"1934.35","middle":"1934.325","provider":1,"origin_create_time":1660521567,"weight":100,"pair":"ETH-USDT"}]}'}
    #             with allure.step("获取具体汇率"):
    #                 extra = json.loads(quote['extra'])
    #                 if len(extra['origins']) == 1:
    #                     original_bid = extra['origins'][0]['bid']
    #                     original_ask = extra['origins'][0]['ask']
    #                 else:
    #                     original_info = extra['origins']
    #                     pair1 = extra['origins'][0]['pair']
    #                     pair2 = extra['origins'][1]['pair']
    #                     if str(pair1).split('-')[0] == str(pair2).split('-')[0]:
    #                         pass
    #                     elif str(pair1).split('-')[0] == str(pair2).split('-')[1]:
    #                         original_bid = Decimal(original_info[0]['bid']) * Decimal(original_info[1]['bid'])
    #                         original_ask = Decimal(original_info[0]['ask']) * Decimal(original_info[1]['ask'])
    #                     elif str(pair1).split('-')[1] == str(pair2).split('-')[0]:
    #                         original_bid = Decimal(original_info[0]['bid']) * Decimal(original_info[1]['bid'])
    #                         original_ask = Decimal(original_info[0]['ask']) * Decimal(original_info[1]['ask'])
    #                     elif str(pair1).split('-')[1] == str(pair2).split('-')[1]:
    #                         original_bid = Decimal(original_info[0]['bid']) / Decimal(original_info[1]['bid'])
    #                         original_ask = Decimal(original_info[0]['ask']) / Decimal(original_info[1]['ask'])
    #                     print(original_bid, original_ask)
    #             # service_charge_type = 0
    #             # with allure.step("获取需要增加的汇率"):
    #             #     for y in (get_json()['cfx_service_charge']).keys():
    #             #         if y in i:
    #             #             service_charge = get_json()['cfx_service_charge'][y]
    #             #             assert (Decimal(original_bid) * Decimal(str(1 - service_charge))).quantize(Decimal('0.0000'), ROUND_FLOOR) == Decimal(quote['bid']).quantize(Decimal('0.0000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(original_bid, quote['bid'], i)
    #             #             assert (Decimal(original_ask) * Decimal(str(1 + service_charge))).quantize(Decimal('0.0000'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.0000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(original_ask, quote['ask'], i)
    #             #             service_charge_type = 1
    #             #     if service_charge_type == 0:
    #             #         service_charge = get_json()['cfx_service_charge']['Other']
    #             #         assert (Decimal(original_bid) * Decimal(str(1 - service_charge))).quantize(Decimal('0.0000'), ROUND_FLOOR) == Decimal(quote['bid']).quantize(Decimal('0.0000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(original_bid, quote['bid'], i)
    #             #         assert (Decimal(original_ask) * Decimal(str(1 + service_charge))).quantize(Decimal('0.0000'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.0000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(original_ask, quote['ask'], i)

    @allure.title('test_quote_001')
    @allure.description('校验cfx汇率增加的浮点')
    def test_quote_001(self):
        with allure.step("获取当前UTC时间"):
            day_time = (datetime.now(tz=pytz.timezone('UTC'))).strftime("%Y%m%d")
        with allure.step("获取全部换汇币种对"):
            cfx_list = ApiFunction.get_cfx_list()
            for i in cfx_list:
                sql = "select bid, ask, original_bid, original_ask, extra from quote_{} where pair = '{}' and purpose = 'Customer' limit 1;".format(day_time, i)
                logger.info('sql命令是{}'.format(sql))
                quote = (sqlFunction().connect_mysql('pricing', sql=sql))[0]
                logger.info('汇率list是{}'.format(quote))
                service_charge_type = 0
                with allure.step("获取需要增加的汇率"):
                    for y in (get_json()['cfx_service_charge']).keys():
                        if y in i:
                            service_charge = get_json()['cfx_service_charge'][y]
                            assert (Decimal(quote['original_bid']) * Decimal(str(1 - service_charge))).quantize(Decimal('0.000'), ROUND_FLOOR) == Decimal(quote['bid']).quantize(Decimal('0.000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(quote['original_bid'], quote['bid'], i)
                            assert (Decimal(quote['original_ask']) * Decimal(str(1 + service_charge))).quantize(
                                Decimal('0.000'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.000'),
                                                                                                ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(
                                quote['original_ask'], quote['ask'], i)
                            service_charge_type = 1
                    if service_charge_type == 0:
                        service_charge = get_json()['cfx_service_charge']['Other']
                        assert (Decimal(quote['original_bid']) * Decimal(str(1 - service_charge))).quantize(
                            Decimal('0.000'),
                            ROUND_FLOOR) == Decimal(
                            quote['bid']).quantize(Decimal('0.000'),
                                                   ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(
                            quote['original_bid'], quote['bid'], i)
                        assert (Decimal(quote['original_ask']) * Decimal(str(1 + service_charge))).quantize(
                            Decimal('0.000'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(
                            quote['original_ask'], quote['ask'], i)

    @allure.title('test_quote_002')
    @allure.description('校验check out汇率增加的浮点')
    def test_quote_002(self):
        with allure.step("获取当前UTC时间"):
            day_time = (datetime.now(tz=pytz.timezone('UTC'))).strftime("%Y%m%d")
        with allure.step("获取全部换汇币种对"):
            cfx_list = ApiFunction.get_buy_crypto_currency(partner=partner, type='all')
            for i in cfx_list:
                sql = "select bid, ask, original_bid, original_ask, extra from quote_{} where pair = '{}' and purpose = 'BuyTxn' limit 1;".format(day_time, i)
                logger.info('sql命令是{}'.format(sql))
                quote = (sqlFunction().connect_mysql('pricing', sql=sql))[0]
                logger.info('汇率list是{}'.format(quote))
                service_charge_type = 0
                with allure.step("获取需要增加的汇率"):
                    for y in (get_json()['check_out_cfx_service_charge']).keys():
                        if y == i.split('-')[1]:
                            service_charge = get_json()['check_out_cfx_service_charge'][y]
                            assert (Decimal(quote['original_bid']) * Decimal(str(1 - service_charge))).quantize(Decimal('0.000'), ROUND_FLOOR) == Decimal(quote['bid']).quantize(Decimal('0.000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(quote['original_bid'], quote['bid'], i)
                            assert (Decimal(quote['original_ask']) * Decimal(str(1 + service_charge))).quantize(
                                Decimal('0.000'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(
                                quote['original_ask'], quote['ask'], i)
                            service_charge_type = 1
                    if service_charge_type == 0:
                        service_charge = get_json()['check_out_cfx_service_charge']['Other']
                        assert (Decimal(quote['original_bid']) * Decimal(str(1 - service_charge))).quantize(
                            Decimal('0.000'),
                            ROUND_FLOOR) == Decimal(
                            quote['bid']).quantize(Decimal('0.000'),
                                                   ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(
                            quote['original_bid'], quote['bid'], i)
                        assert (Decimal(quote['original_ask']) * Decimal(str(1 + service_charge))).quantize(
                            Decimal('0.000'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.000'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(
                            quote['original_ask'], quote['ask'], i)
