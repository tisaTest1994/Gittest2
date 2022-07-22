from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("Quote 相关 testcases")
class TestQuoteApi:

    # 初始化class
    def setup_method(self):
        pass

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
                with allure.step("获取需要增加的汇率"):
                    for y in (get_json()['cfx_service_charge']).keys():
                        if y in i:
                            service_charge = get_json()['cfx_service_charge'][y]
                            assert (Decimal(quote['original_bid']) * Decimal(1 - service_charge).quantize(Decimal('0.00000'), ROUND_FLOOR)).quantize(Decimal('0.00'), ROUND_FLOOR) == Decimal(quote['bid']).quantize(Decimal('0.00'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(quote['original_bid'], quote['bid'], i)
                        else:
                            service_charge = get_json()['cfx_service_charge']['Other']
                            print(Decimal(1 - service_charge).quantize(Decimal('0.00000'), ROUND_FLOOR))
                            print((Decimal(quote['original_bid']) * Decimal(1 - service_charge).quantize(Decimal('0.00000'), ROUND_FLOOR)).quantize(Decimal('0.00'), ROUND_FLOOR))
                            assert (Decimal(quote['original_bid']) * Decimal(1 - service_charge).quantize(Decimal('0.00000'), ROUND_FLOOR)).quantize(Decimal('0.00'), ROUND_FLOOR) == Decimal(quote['bid']).quantize(Decimal('0.00'), ROUND_FLOOR), '校验cfx汇率增加的浮点错误，original_bid是{}, bid是{}, pair是{}'.format(quote['original_bid'], quote['bid'], i)


