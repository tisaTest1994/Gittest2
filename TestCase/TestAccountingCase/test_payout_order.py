from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("accounting PayOutOrder 相关 testcases")
class TestAccountingPayOutOrderApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_payout_order_001')
    @allure.description('ETH Payout Order校验')
    def test_payout_order_001(self):
        with allure.step("生成一笔ETH payout订单"):
            transaction_id = ApiFunction.get_payout_transaction_id(amount='0.02', address='0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C', code_type='ETH')
        with allure.step("等待交易成功"):
            sql = "select * from transaction where transaction_id = '{}';".format(transaction_id)
            payout_txn = (sqlFunction().connect_mysql('payouttxn', sql=sql))[0]
            # payout_txn = [{'id': 9785, 'transaction_id': '9fce7911-6d5e-4cc3-89ea-dbd6247b0682', 'account_id': '700dca34-1e6f-408b-903d-e37d0fcfd615', 'legal_entity': 'LEGAL_ENTITY_LITHUANIA_DGT', 'status': 'PAYOUT_TXN_STATUS_SUCCEEDED', 'status_idx': 2, 'ccy': 'ETH', 'amount': '0.02', 'payer': 'null', 'beneficiary': '{"crypto_account": {"address": "0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C"}}', 'payment_method': '{}', 'fee': '{"ccy": {"code": {"role": 2, "symbol": "ETH"}, "amount": {"amount": "0.004"}}}', 'counterparty_response': '{}', 'memo': '', 'request_by': 'pay.api', 'failed_reason': '', 'cancel_reason': '', 'return_fee': 0, 'cfx_transaction_id': '', 'original_transaction_id': '', 'settlement_at': None, 'daily_frozen_amount': 'EUR:26.67', 'created_at': 'datetime.datetime(2022, 9, 28, 9, 55, 12, 949811)', 'updated_at': 'datetime.datetime(2022, 9, 28, 9, 55, 13, 828659)', 'extra': '{"partner_id": "800b482d-0a88-480a-aae7-741f77a572f4", "user_ref_id": "988518746672869376"}', 'chain': 'ETH', 'previous_txn_type': 0, 'previous_txn_id': None, 'real_ccy': 'ETH'}][0]
            status = payout_txn['status']
            ccy = payout_txn['ccy']
            amount = payout_txn['amount']
            fee = json.loads(payout_txn['fee'])
            fee_amount = fee['ccy']['amount']['amount']
            for i in range(0, 10):
                if status == 'PAYOUT_TXN_STATUS_SUCCEEDED':
                    pass
                else:
                    sleep(60)
        with allure.step("查transaction的动账"):
            sql = "select * from wallet.internal_balance where transaction_id = '{}';".format(transaction_id)
            internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            line1 = internal_balance[0]
            line2 = internal_balance[1]
            line3 = internal_balance[2]
        print(line1)
        print(line2)
        print(line3)
        # with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 内部户转出"):
        #     sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 1;".format(transaction_id)
        #     movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
        #     sql = "select * from internal_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
        #     movement_id_internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
        #     assert movement_id_internal_balance != (), 'PAYOUT_TXN_STATUS_EXECUTING 内部户转出失败'
        # with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 外部户收到"):
        #     sql = "select * from client_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
        #     movement_id_client_balance = sqlFunction().connect_mysql('wallet', sql=sql)
        #     assert movement_id_client_balance != (), 'PAYOUT_TXN_STATUS_EXECUTING 外部户收到失败'
        # with allure.step("确认 PAYOUT_TXN_STATUS_EXECUTING 手续费"):
        #     sql = "select movement_id from movement where transaction_id = '{}' and memo = 'PAYOUT_TXN_STATUS_EXECUTING' and offset = 2;".format(transaction_id)
        #     movement_id = sqlFunction().connect_mysql('wallet', sql=sql)
        #     sql = "select * from internal_balance where movement_id = '{}';".format(movement_id[0]['movement_id'])
        #     movement_id_service_charge = sqlFunction().connect_mysql('wallet', sql=sql)
        #     assert movement_id_service_charge != (), '确认 PAYOUT_TXN_STATUS_EXECUTING 手续费失败'
        #     assert len(movement_id_service_charge) == 2, '手续费一借一贷错误'
        #
