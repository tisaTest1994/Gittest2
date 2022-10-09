from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("PayOut accounting相关 testcases")
class TestPayOutAccountingApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_payout_accounting_001')
    @allure.description('ETH Payout Accounting校验')
    def test_payout_accounting_001(self):
        with allure.step("生成一笔ETH payout订单"):
            transaction_id = ApiFunction.get_payout_transaction_id(amount='0.02', address='0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C', code_type='ETH')
        with allure.step("等待交易成功"):
            sql = "select * from transaction where transaction_id = '{}';".format(transaction_id)
            payout_txn = (sqlFunction().connect_mysql('payouttxn', sql=sql))[0]
            status = payout_txn['status']
            ccy = payout_txn['ccy']
            amount = payout_txn['amount']
            fee = json.loads(payout_txn['fee'])
            fee_amount = fee['ccy']['amount']['amount']
            for i in range(0, 20):
                if status == 'PAYOUT_TXN_STATUS_SUCCEEDED':
                    break
                else:
                    if i == 19:
                        assert False, '已等待20分钟，ETH提现仍未到账，请手工检查交易是否正常'
                    else:
                        sql = "select * from transaction where transaction_id = '{}';".format(transaction_id)
                        payout_txn = (sqlFunction().connect_mysql('payouttxn', sql=sql))[0]
                        status = payout_txn['status']
                        sleep(60)
        with allure.step("查transaction的动账"):
            with allure.step("step1：查internal balance表"):
                sql = "select * from internal_balance where transaction_id = '{}';".format(transaction_id)
                internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
                assert len(internal_balance) == 3, 'payout transaction 动账少记了'
                with allure.step("step2：检查3笔动账"):
                    for i in range(0, len(internal_balance)):
                        if json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {"to":"Executing","from":"Ready" } \
                                and internal_balance[i]['requested_by'] =='payouttxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                and internal_balance[i]['amount'] == amount \
                                and internal_balance[i]['movement_type'] == 1\
                                and internal_balance[i]['code']:
                            with allure.step("检查交易阶段：Ready-Executing，本金的动账"):
                                logger.info('检查交易阶段：Ready-Executing，本金的动账')
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Payment Transition-ETH'
                        elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {"to":"Executing","from":"Ready" } \
                                and internal_balance[i]['requested_by'] =='payouttxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                and internal_balance[i]['amount'] == fee_amount \
                                and internal_balance[i]['movement_type'] == 1 \
                                and internal_balance[i]['code'] == ccy:
                            with allure.step("检查交易阶段：Ready-Executing，贷方向fee的动账"):
                                logger.info('贷方向fee的动账正确')
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Revenue Fee-ETH'
                        elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {"to":"Executing","from":"Ready" } \
                                and internal_balance[i]['requested_by'] =='payouttxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                and internal_balance[i]['amount'] == fee_amount \
                                and internal_balance[i]['movement_type'] == 2\
                                and internal_balance[i]['code'] == ccy:
                            with allure.step("检查交易阶段：Ready-Executing，借方向fee的动账"):
                                logger.info('借方向fee的动账正确')
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Payment Transition-ETH'
                        else:
                            assert False, "transaction动账错误，错误的动账为：{}".format(internal_balance[i])
        with allure.step("查客户账"):
            with allure.step("step1：查internal balance表"):
                sql = "select * from client_balance where transaction_id = '{}';".format(transaction_id)
                client_balance = sqlFunction().connect_mysql('wallet', sql=sql)
                wallet_id = client_balance[0]['wallet_id']
                assert client_balance[0]['code'] == ccy and client_balance[0]['amount'] == amount \
                       and client_balance[0]['requested_by'] == 'payouttxn' \
                       and client_balance[0]['transaction_sub_type'] == 'Payment', '客户账记账错误'
            with allure.step("检查wallet name"):
                sql = "select * from wallet where wallet_id = '{}';".format(
                    wallet_id)
                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                assert wallet_name[0]['wallet_name'] == ''
        with allure.step("查order的动账"):
            sql = "select * from payoutorder.order where transaction_id = '{}';".format(transaction_id)
            order_original = sqlFunction().connect_mysql('payoutorder', sql=sql)
            order = order_original[0]
            assert order['status'] == 'PAYOUT_ORDER_STATUS_SUCCEEDED' and order['ccy'] == ccy and Decimal(order['amount']) == Decimal(amount) - Decimal(fee_amount), 'order错误'
            order_id = order['order_id']
            sql = "select * from wallet.internal_balance where transaction_id = '{}';".format(order_id)
            internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert len(internal_balance) == 4, 'payout order 动账少记了'
            with allure.step("step2：检查order4笔动账"):
                for i in range(0, len(internal_balance)):
                    if json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Executing", "from": "Created"} \
                            and internal_balance[i]['requested_by'] == 'payoutorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                            and Decimal(internal_balance[i]['amount']) == Decimal(amount) - Decimal(fee_amount) \
                            and internal_balance[i]['movement_type'] == 1 \
                            and internal_balance[i]['code'] == ccy:
                        with allure.step("检查交易阶段：Created-Executing阶段，贷方向的order动账"):
                            logger.info('交易阶段：Created-Executing阶段，贷方向的order动账正确')
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Payment Clearing-FireBlocks-ETH'
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Executing", "from": "Created"} \
                            and internal_balance[i]['requested_by'] == 'payoutorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                            and Decimal(internal_balance[i]['amount']) == Decimal(amount) - Decimal(fee_amount) \
                            and internal_balance[i]['movement_type'] == 2 \
                            and internal_balance[i]['code'] == ccy:
                        with allure.step("检查交易阶段：Created-Executing阶段，借方向的order动账"):
                            logger.info('交易阶段：Created-Executing阶段，借方向的order动账正确')
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Payment Transition-ETH'
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Succeeded", "from": "Executing"} \
                            and internal_balance[i]['requested_by'] == 'payoutorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                            and Decimal(internal_balance[i]['amount']) == Decimal(amount) - Decimal(fee_amount) \
                            and internal_balance[i]['movement_type'] == 1 \
                            and internal_balance[i]['code'] == ccy:
                        with allure.step("检查交易阶段：Executing-Succeeded阶段，贷方向的order动账"):
                            logger.info('交易阶段：Executing-Succeeded阶段，贷方向的order动账正确')
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Cash MP-FireBlocks-ETH_ETH'
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Succeeded", "from": "Executing"} \
                            and internal_balance[i]['requested_by'] == 'payoutorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                            and Decimal(internal_balance[i]['amount']) == Decimal(amount) - Decimal(fee_amount) \
                            and internal_balance[i]['movement_type'] == 2 \
                            and internal_balance[i]['code'] == ccy:
                        with allure.step("检查交易阶段：Executing-Succeeded阶段，借方向的order动账"):
                            logger.info('交易阶段：Executing-Succeeded阶段，借方向的order动账正确')
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Payment Clearing-FireBlocks-ETH'
                    else:
                        assert False, "order动账错误，错误的动账为：{}".format(internal_balance[i])

