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
            sleep(10)
            transaction_id = 'f01f782f-b6ce-42be-b4bb-aa1f3504bf47'
        with allure.step("确认 PAYOUT_TXN_STATUS_CREATED 冻账"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_CREATED';".format(transaction_id)
            movement_id_create = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_create == (), 'PAYOUT_TXN_STATUS_CREATED冻账失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 内部户"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 1;".format(transaction_id)
            movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
            print(movement_id[0]['movement_id'])
            sql = "select * from internal_balance where movement_id = '{}';".format(movement_id)
            sda = sqlFunction().connect_mysql('wallet', sql=sql)
            print(sda)








