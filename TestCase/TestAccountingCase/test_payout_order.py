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
                    break
                else:
                    sleep(60)
        with allure.step("查transaction的动账"):
            with allure.step("step1：查internal balance表"):
                sql = "select * from wallet.internal_balance where transaction_id = '{}';".format(transaction_id)
                internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
                # internal_balance = [{'id': 2982881, 'trace_id': 'bb59c17f-707a-46a2-b398-eaef7a7d25cc', 'movement_id': '2e912069-89f1-4a47-a5e3-69f27fe2a340', 'account_id': 'LT000001.0003.0001.0000.DGT_________', 'move_index': 1, 'wallet_id': '77ad0e81-d40b-11eb-8e66-0a3898443cb8', 'date': 'datetime.datetime(2022, 9, 29, 3, 39, 9)', 'transaction_id': '5950ae52-1c23-4a62-b70d-278275488b47', 'requested_by': 'payouttxn', 'transaction_sub_type': 'Payment', 'detail': '{"type": 1, "amount": {"amount": "0.02"}, "wallet": null, "balance": 1, "route_wallet": {"code": {"role": 2, "chain": "", "symbol": "ETH"}, "step": 0, "account_id": "LT000001.0003.0001.0000.DGT_________", "moneyhouse": "", "amount_type": 1, "legal_entity": 1, "requested_by": "payouttxn", "status_transitions": {"to": "Executing", "from": "Ready"}, "transaction_sub_type": "Payment"}, "transaction_sub_type": ""}', 'status': 0, 'movement_type': 1, 'code': 'ETH', 'amount': '0.02', 'created_at': 'datetime.datetime(2022, 9, 29, 3, 39, 10, 145286)', 'updated_at': 'datetime.datetime(2022, 9, 29, 3, 39, 10, 145286)', 'legal_entity': 'LEGAL_ENTITY_LITHUANIA_DGT', 'moneyhouse': ''},
                #             {'id': 2982882, 'trace_id': '839d0c4c-09a3-4371-8c47-e53f38d9c138', 'movement_id': 'e5347702-76b2-49da-a849-19cb8f43738c', 'account_id': 'LT000001.0003.0001.0000.DGT_________', 'move_index': 2, 'wallet_id': '77ad0e81-d40b-11eb-8e66-0a3898443cb8', 'date': 'datetime.datetime(2022, 9, 29, 3, 39, 10)', 'transaction_id': '5950ae52-1c23-4a62-b70d-278275488b47', 'requested_by': 'payouttxn', 'transaction_sub_type': 'Payment', 'detail': '{"type": 2, "amount": {"amount": "0.004"}, "wallet": null, "balance": 1, "route_wallet": {"code": {"role": 2, "chain": "", "symbol": "ETH"}, "step": 0, "account_id": "LT000001.0003.0001.0000.DGT_________", "moneyhouse": "", "amount_type": 2, "legal_entity": 1, "requested_by": "payouttxn", "status_transitions": {"to": "Executing", "from": "Ready"}, "transaction_sub_type": "Payment"}, "transaction_sub_type": ""}', 'status': 0, 'movement_type': 2, 'code': 'ETH', 'amount': '0.004', 'created_at': 'datetime.datetime(2022, 9, 29, 3, 39, 10, 391358)', 'updated_at': 'datetime.datetime(2022, 9, 29, 3, 39, 10, 391358)', 'legal_entity': 'LEGAL_ENTITY_LITHUANIA_DGT', 'moneyhouse': ''},
                #             {'id': 2982883, 'trace_id': 'f44a7f67-f28f-4e3c-88b9-34d539ad73b3', 'movement_id': 'e5347702-76b2-49da-a849-19cb8f43738c', 'account_id': 'LT000001.0003.0001.0000.DGT_________', 'move_index': 2, 'wallet_id': '77b057d5-d40b-11eb-8e66-0a3898443cb8', 'date': 'datetime.datetime(2022, 9, 29, 3, 39, 10)', 'transaction_id': '5950ae52-1c23-4a62-b70d-278275488b47', 'requested_by': 'payouttxn', 'transaction_sub_type': 'Payment', 'detail': '{"type": 1, "amount": {"amount": "0.004"}, "wallet": null, "balance": 1, "route_wallet": {"code": {"role": 2, "chain": "", "symbol": "ETH"}, "step": 0, "account_id": "LT000001.0003.0001.0000.DGT_________", "moneyhouse": "", "amount_type": 2, "legal_entity": 1, "requested_by": "payouttxn", "status_transitions": {"to": "Executing", "from": "Ready"}, "transaction_sub_type": "Payment"}, "transaction_sub_type": ""}', 'status': 0, 'movement_type': 1, 'code': 'ETH', 'amount': '0.004', 'created_at': 'datetime.datetime(2022, 9, 29, 3, 39, 10, 395921)', 'updated_at': 'datetime.datetime(2022, 9, 29, 3, 39, 10, 395921)', 'legal_entity': 'LEGAL_ENTITY_LITHUANIA_DGT', 'moneyhouse': ''}]
                assert len(internal_balance) == 3, 'payout transaction movement缺少了'
                with allure.step("step2：检查3笔动账"):
                    for i in range(0, len(internal_balance)):
                        with allure.step("检查交易阶段：Ready-Executing，本金的动账"):
                            if json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {"to":"Executing","from":"Ready" } \
                                    and internal_balance[i]['requested_by'] =='payouttxn' \
                                    and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                    and internal_balance[i]['amount'] == amount \
                                    and internal_balance[i]['movement_type'] == 1\
                                    and internal_balance[i]['code']:
                                logger.info('本金的动账正确')
                                wallet_id = internal_balance[i]['wallet']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet.wallet where wallet_id= = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name['wallet_name'] == 'LT-Payment Transition-ETH'
                            elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {"to":"Executing","from":"Ready" } \
                                    and internal_balance[i]['requested_by'] =='payouttxn' \
                                    and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                    and internal_balance[i]['amount'] == fee_amount \
                                    and internal_balance[i]['movement_type'] == 1 \
                                    and internal_balance[i]['code'] == ccy:
                                logger.info('贷方向fee的动账正确')
                                wallet_id = internal_balance[i]['wallet']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet.wallet where wallet_id= = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name['wallet_name'] == 'LT-Payment Transition-ETH'
                            elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {"to":"Executing","from":"Ready" } \
                                    and internal_balance[i]['requested_by'] =='payouttxn' \
                                    and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                    and internal_balance[i]['amount'] == fee_amount \
                                    and internal_balance[i]['movement_type'] == 2\
                                    and internal_balance[i]['code']:
                                logger.info('借方向fee的动账正确')
                                wallet_id = internal_balance[i]['wallet']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet.wallet where wallet_id= = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name['wallet_name'] == 'LT-Revenue Fee-ETH'
                            else:
                                assert False, "transaction动账错误，错误的动账为：{}".format(internal_balance[i])
        with allure.step("查客户账"):
            sql = "select * from wallet.client_balancewhere transaction_id = '{}';".format(transaction_id)
            client_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert client_balance['code'] == ccy and client_balance['amount']== amount and client_balance['requested_by'] == 'payouttxn' and client_balance['transaction_sub_type'] == 'Payment', '客户账记账错误'