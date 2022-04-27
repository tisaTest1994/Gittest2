from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("accounting 相关 testcases")
class TestAccountingPayOutOrderApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_payout_order_001')
    @allure.description('ETH Payout Order校验')
    def test_payout_order_001(self):
        with allure.step("生成一笔ETH payout订单"):
            transaction_id = ApiFunction.get_payout_transaction_id(amount='0.01', address='0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C', code_type='ETH')
            sleep(20)
        with allure.step("确认 PAYOUT_TXN_STATUS_CREATED 冻账"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_CREATED';".format(transaction_id)
            movement_id_create = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_create != (), 'PAYOUT_TXN_STATUS_CREATED冻账失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 内部户转出"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 1;".format(transaction_id)
            movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
            sql = "select * from internal_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_internal_balance != (), 'PAYOUT_TXN_STATUS_EXECUTING 内部户转出失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 外部户收到"):
            sql = "select * from client_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_client_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_client_balance != (), 'PAYOUT_TXN_STATUS_EXECUTING 外部户收到失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 手续费"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 2;".format(transaction_id)
            movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
            sql = "select * from internal_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_service_charge = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_service_charge != (), '确认 PAYOUT_TXN_STATUS_EXECUTING 手续费失败'
            assert len(movement_id_service_charge) == 2, '手续费一借一贷错误'

    @allure.title('test_payout_order_002')
    @allure.description('USDT Payout Order校验')
    def test_payout_order_002(self):
        with allure.step("生成一笔USDT payout订单"):
            transaction_id = ApiFunction.get_payout_transaction_id(amount='10.1', address='0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C', code_type='USDT')
            sleep(20)
        with allure.step("确认 PAYOUT_TXN_STATUS_CREATED 冻账"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_CREATED';".format(transaction_id)
            movement_id_create = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_create != (), 'PAYOUT_TXN_STATUS_CREATED冻账失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 内部户转出"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 1;".format(transaction_id)
            movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
            sql = "select * from internal_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_internal_balance != (), 'PAYOUT_TXN_STATUS_EXECUTING 内部户转出失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 外部户收到"):
            sql = "select * from client_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_client_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_client_balance != (), 'PAYOUT_TXN_STATUS_EXECUTING 外部户收到失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 手续费"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 2;".format(transaction_id)
            movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
            sql = "select * from internal_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_service_charge = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_service_charge != (), '确认 PAYOUT_TXN_STATUS_EXECUTING 手续费失败'
            assert len(movement_id_service_charge) == 2, '手续费一借一贷错误'

    @allure.title('test_payout_order_003')
    @allure.description('BTC Payout Order校验')
    def test_payout_order_003(self):
        with allure.step("生成一笔BTC payout订单"):
            transaction_id = ApiFunction.get_payout_transaction_id(amount='0.01', address='tb1q3fhjd9f0th907cuym9dtyzpy3zu9tn6205jhwm', code_type='BTC')
            sleep(20)
        with allure.step("确认 PAYOUT_TXN_STATUS_CREATED 冻账"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_CREATED';".format(transaction_id)
            movement_id_create = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_create != (), 'PAYOUT_TXN_STATUS_CREATED冻账失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 内部户转出"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 1;".format(transaction_id)
            movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
            sql = "select * from internal_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_internal_balance != (), 'PAYOUT_TXN_STATUS_EXECUTING 内部户转出失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 外部户收到"):
            sql = "select * from client_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_client_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_client_balance != (), 'PAYOUT_TXN_STATUS_EXECUTING 外部户收到失败'
        with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 手续费"):
            sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 2;".format(transaction_id)
            movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
            sql = "select * from internal_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
            movement_id_service_charge = sqlFunction().connect_mysql('wallet', sql=sql)
            assert movement_id_service_charge != (), '确认 PAYOUT_TXN_STATUS_EXECUTING 手续费失败'
            assert len(movement_id_service_charge) == 2, '手续费一借一贷错误'



