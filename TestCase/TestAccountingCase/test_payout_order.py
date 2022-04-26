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
        with allure.step("确认 PAYOUT_TXN_STATUS_CREATED 交易"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN1_STATUS_CREATED'".format(transaction_id)
            movement_id_create = sqlFunction().connect_mysql('wallet', sql=sql)
            print(movement_id_create)
            print(type(movement_id_create))
            assert movement_id_create == (), 'PAYOUT_TXN_STATUS_CREATED冻账失败'

            #movement_id_list = [{'movement_id': '8e8a3336-bc9a-44a8-9445-e86ab9a5b96b'}, {'movement_id': 'fb547e8a-7f67-41a2-892f-d219d2cb1665'}, {'movement_id': '156db7aa-b244-4f39-a2fa-4e20e297fc23'}]
        # with allure.step("确认有三个movement id"):'
        #     assert len(movement_id_list) == 3, "确认有三个movement id"
        #     for i in movement_id_list:
        #         print(i)




