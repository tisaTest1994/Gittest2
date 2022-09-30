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
            # payout_txn = {"transaction_id":"af242aec-6b4e-4285-8c30-a497f7f249d1","txn_id":"af242aec-6b4e-4285-8c30-a497f7f249d1","status":1,"code":"ETH","amount":"0.02","fee":{"code":"ETH","amount":"0.004"},"receivable_amount":"0.016","return_amount":None,"failed_reason":""}
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
                sql = "select * from internal_balance where transaction_id = '{}';".format(transaction_id)
                internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
                assert len(internal_balance) == 3, 'payout transaction 动账少记了'
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
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    print(wallet_name)
                                    # assert wallet_name['wallet_name'] == 'LT-Payment Transition-ETH'
                            elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {"to":"Executing","from":"Ready" } \
                                    and internal_balance[i]['requested_by'] =='payouttxn' \
                                    and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                    and internal_balance[i]['amount'] == fee_amount \
                                    and internal_balance[i]['movement_type'] == 1 \
                                    and internal_balance[i]['code'] == ccy:
                                logger.info('贷方向fee的动账正确')
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    print(wallet_name)
                                    # assert wallet_name['wallet_name'] == 'LT-Payment Transition-ETH'
                            elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {"to":"Executing","from":"Ready" } \
                                    and internal_balance[i]['requested_by'] =='payouttxn' \
                                    and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                    and internal_balance[i]['amount'] == fee_amount \
                                    and internal_balance[i]['movement_type'] == 2\
                                    and internal_balance[i]['code'] == ccy:
                                logger.info('借方向fee的动账正确')
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    print(wallet_name)
                                    # assert wallet_name['wallet_name'] == 'LT-Revenue Fee-ETH'
                            else:
                                assert False, "transaction动账错误，错误的动账为：{}".format(internal_balance[i])
        # with allure.step("查客户账"):
        #     sql = "select * from client_balance where transaction_id = '{}';".format(transaction_id)
        #     client_balance = sqlFunction().connect_mysql('wallet', sql=sql)
        #     assert client_balance['code'] == ccy and client_balance['amount'] == amount \
        #            and client_balance['requested_by'] == 'payouttxn' \
        #            and client_balance['transaction_sub_type'] == 'Payment', '客户账记账错误'
        # with allure.step("查order的动账"):
        #     sql = "select * from order where transaction_id = '{}';".format(transaction_id)
        #     order = sqlFunction().connect_mysql('payoutorder', sql=sql)
        #     assert order['status'] == 'PAYOUT_ORDER_STATUS_SUCCEEDED' and order['ccy'] == ccy and order['amount'] == amount - fee_amount, 'order错误'
        #     order_id = order['order_id']
        #     sql = "select * from wallet.internal_balance where transaction_id= = '{}';".format(order_id)
        #     internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
        #     assert len(internal_balance) == 4, 'payout order 动账少记了'
        #     with allure.step("step2：检查order4笔动账"):
        #         for i in range(0, len(internal_balance)):
        #             if json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
        #                 "to": "Executing", "from": "Ready"} \
        #                     and internal_balance[i]['requested_by'] == 'payoutorder' \
        #                     and internal_balance[i]['transaction_sub_type'] == 'Payment' \
        #                     and internal_balance[i]['amount'] == amount - fee_amount \
        #                     and internal_balance[i]['movement_type'] == 1 \
        #                     and internal_balance[i]['code'] == ccy:
        #                     logger.info('贷方向Created-Executing阶段的order动账正确')
        #                     wallet_id = internal_balance[i]['wallet_id']
        #                     with allure.step("检查wallet name"):
        #                         sql = "select * from wallet where wallet_id = '{}';".format(
        #                             wallet_id)
        #                         wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
        #                         assert wallet_name['wallet_name'] == 'LT-Payment Clearing-FireBlocks-ETH'
        #             elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
        #                 "to": "Executing", "from": "Ready"} \
        #                     and internal_balance[i]['requested_by'] == 'payoutorder' \
        #                     and internal_balance[i]['transaction_sub_type'] == 'Payment' \
        #                     and internal_balance[i]['amount'] == amount - fee_amount \
        #                     and internal_balance[i]['movement_type'] == 2 \
        #                     and internal_balance[i]['code'] == ccy:
        #                     logger.info('借方向Created-Executing阶段的order动账正确')
        #                     wallet_id = internal_balance[i]['wallet_id']
        #                     with allure.step("检查wallet name"):
        #                         sql = "select * from wallet where wallet_id = '{}';".format(
        #                             wallet_id)
        #                         wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
        #                         assert wallet_name['wallet_name'] == 'LT-Payment Transition-ETH'
        #             elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
        #                 "to": "Succeeded", "from": "Excuting"} \
        #                     and internal_balance[i]['requested_by'] == 'payoutorder' \
        #                     and internal_balance[i]['transaction_sub_type'] == 'Payment' \
        #                     and internal_balance[i]['amount'] == amount - fee_amount \
        #                     and internal_balance[i]['movement_type'] == 1 \
        #                     and internal_balance[i]['code'] == ccy:
        #                     logger.info('贷方向Executing-Succeeded阶段的order动账正确')
        #                     wallet_id = internal_balance[i]['wallet_id']
        #                     with allure.step("检查wallet name"):
        #                         sql = "select * from wallet where wallet_id = '{}';".format(
        #                             wallet_id)
        #                         wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
        #                         assert wallet_name['wallet_name'] == 'LT-Cash MP-FireBlocks-ETH_ETH'
        #             elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
        #                 "to": "Succeeded", "from": "Excuting"} \
        #                     and internal_balance[i]['requested_by'] == 'payoutorder' \
        #                     and internal_balance[i]['transaction_sub_type'] == 'Payment' \
        #                     and internal_balance[i]['amount'] == amount - fee_amount \
        #                     and internal_balance[i]['movement_type'] == 2 \
        #                     and internal_balance[i]['code'] == ccy:
        #                     logger.info('借方向Executing-Succeeded阶段的order动账正确')
        #                     wallet_id = internal_balance[i]['wallet_id']
        #                     with allure.step("检查wallet name"):
        #                         sql = "select * from wallet where wallet_id = '{}';".format(
        #                             wallet_id)
        #                         wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
        #                         assert wallet_name['wallet_name'] == 'LT-Payment Clearing-FireBlocks-ETH'
        #             else:
        #                 assert False, "order动账错误，错误的动账为：{}".format(internal_balance[i])

