from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("Quote 相关 testcases")
class TestQuoteApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_quote_001')
    @allure.description('校验cfx汇率增加的浮点')
    def test_quote_001(self):
        with allure.step("获取当前UTC时间"):
            day_time = (datetime.now(tz=pytz.timezone('UTC'))).strftime("%Y%m%d")
        with allure.step("获取全部换汇币种对"):
            cfx_list = ApiFunction.get_cfx_list()
            for i in cfx_list:
                sql = "select bid, ask, original_bid, original_ask from quote_{} where pair = '{}' and purpose = 'Customer' limit 1;".format(day_time, i)
                logger.info('sql命令是{}'.format(sql))
                quote = (sqlFunction().connect_mysql('pricing', sql=sql))[0]
                logger.info('汇率list是{}'.format(quote))
                service_charge_type = 0
                with allure.step("获取需要增加的汇率"):
                    for y in (get_json()['cfx_service_charge']).keys():
                        if y in i:
                            service_charge = get_json()['cfx_service_charge'][y]
                            assert (Decimal(quote['original_bid']) * Decimal(str(1 - service_charge))).quantize(Decimal('0.00'), ROUND_FLOOR) == Decimal(quote['bid']).quantize(Decimal('0.00'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(quote['original_bid'], quote['bid'], i)
                            assert (Decimal(quote['original_ask']) * Decimal(str(1 + service_charge))).quantize(
                                Decimal('0.00'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.00'),
                                                                                                ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(
                                quote['original_ask'], quote['ask'], i)
                            service_charge_type = 1
                    if service_charge_type == 0:
                        service_charge = get_json()['cfx_service_charge']['Other']
                        assert (Decimal(quote['original_bid']) * Decimal(str(1 - service_charge))).quantize(
                            Decimal('0.00'),
                            ROUND_FLOOR) == Decimal(
                            quote['bid']).quantize(Decimal('0.00'),
                                                   ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(
                            quote['original_bid'], quote['bid'], i)
                        assert (Decimal(quote['original_ask']) * Decimal(str(1 + service_charge))).quantize(
                            Decimal('0.00'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.00'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(
                            quote['original_ask'], quote['ask'], i)

    @allure.title('test_quote_002')
    @allure.description('校验check out汇率增加的浮点')
    def test_quote_002(self):
        with allure.step("获取当前UTC时间"):
            day_time = (datetime.now(tz=pytz.timezone('UTC'))).strftime("%Y%m%d")
        with allure.step("获取全部换汇币种对"):
            cfx_list = ApiFunction.get_buy_crypto_currency(type='all')
            for i in cfx_list:
                sql = "select bid, ask, original_bid, original_ask from quote_{} where pair = '{}' and purpose = 'BuyTxn' limit 1;".format(day_time, i)
                logger.info('sql命令是{}'.format(sql))
                quote = (sqlFunction().connect_mysql('pricing', sql=sql))[0]
                logger.info('汇率list是{}'.format(quote))
                service_charge_type = 0
                with allure.step("获取需要增加的汇率"):
                    for y in (get_json()['check_out_cfx_service_charge']).keys():
                        if y in i:
                            service_charge = get_json()['check_out_cfx_service_charge'][y]
                            assert (Decimal(quote['original_bid']) * Decimal(str(1 - service_charge))).quantize(Decimal('0.00'), ROUND_FLOOR) == Decimal(quote['bid']).quantize(Decimal('0.00'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(quote['original_bid'], quote['bid'], i)
                            assert (Decimal(quote['original_ask']) * Decimal(str(1 + service_charge))).quantize(
                                Decimal('0.00'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.00'),
                                                                                                ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(
                                quote['original_ask'], quote['ask'], i)
                            service_charge_type = 1
                    if service_charge_type == 0:
                        service_charge = get_json()['check_out_cfx_service_charge']['Other']
                        assert (Decimal(quote['original_bid']) * Decimal(str(1 - service_charge))).quantize(
                            Decimal('0.00'),
                            ROUND_FLOOR) == Decimal(
                            quote['bid']).quantize(Decimal('0.00'),
                                                   ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(
                            quote['original_bid'], quote['bid'], i)
                        assert (Decimal(quote['original_ask']) * Decimal(str(1 + service_charge))).quantize(
                            Decimal('0.00'), ROUND_FLOOR) == Decimal(quote['ask']).quantize(Decimal('0.00'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_ask是{}, ask是{}, pair是{}'.format(
                            quote['original_ask'], quote['ask'], i)
