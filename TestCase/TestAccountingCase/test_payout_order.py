from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("accounting 相关 testcases")
class TestAccountingPayOutOrderApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_payout_order_001')
    @allure.description('wallet 验证')
    def test_payout_order_001(self):
        with allure.step("生成一笔ETH payout订单"):
            # transaction_id = ApiFunction.get_payout_transaction_id(amount='0.01', address='0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C', code_type='ETH')
            transaction_id = 'f01f782f-b6ce-42be-b4bb-aa1f3504bf47'
        with allure.step("通过sql查询movement id"):
            sql = "select movement_id from movement where transaction_id = '{}'".format(transaction_id)
            info = sqlFunction().connect_mysql('wallet', sql=sql)
            print(info)
            print(type(info))




