from run import *
from Function.operate_sql import *


class AccountingFunction:
    # crypto-payout accounting(ETH/USDT/BTC)
    @staticmethod
    def crypto_payout_accouting(transaction_id):
        with allure.step("等待交易成功"):
            sql = "select * from transaction where transaction_id = '{}';".format(transaction_id)
            payout_txn = (sqlFunction().connect_mysql('payouttxn', sql=sql))[0]
            status = payout_txn['status']
            ccy = payout_txn['ccy']
            amount = payout_txn['amount']
            fee = json.loads(payout_txn['fee'])
            if fee == '':
                fee_amount = '0'
            else:
                fee_amount = fee['ccy']['amount']['amount']
            for i in range(0, 60):
                if status == 'PAYOUT_TXN_STATUS_SUCCEEDED':
                    break
                else:
                    if i == 59:
                        assert False, '已等待60分钟，{}提现仍未到账，请手工检查交易是否正常'.format(ccy)
                    else:
                        sql = "select * from transaction where transaction_id = '{}';".format(transaction_id)
                        payout_txn = (sqlFunction().connect_mysql('payouttxn', sql=sql))[0]
                        status = payout_txn['status']
                        sleep(60)
        with allure.step("查transaction的动账"):
            with allure.step("查internal balance表"):
                sql = "select * from internal_balance where transaction_id = '{}';".format(transaction_id)
                internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
                assert len(internal_balance) == 3, 'payout transaction 动账少记了'
                with allure.step("检查3笔动账"):
                    for i in range(0, len(internal_balance)):
                        if json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                            "to": "Executing", "from": "Ready"} \
                                and internal_balance[i]['requested_by'] == 'payouttxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                and internal_balance[i]['amount'] == amount \
                                and internal_balance[i]['movement_type'] == 1 \
                                and internal_balance[i]['code']:
                            logger.info('币种{}在交易阶段：Ready-Executing,transaction本金动账正确', ccy)
                            with allure.step("检查wallet name"):
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Payment Transition-{}'.format(ccy), \
                                        "期望返回结果是:'LT-Payment Transition-{}'，实际结果是:{}".format(ccy,
                                                                                             wallet_name[0]['wallet_name'])
                        elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                            "to": "Executing", "from": "Ready"} \
                                and internal_balance[i]['requested_by'] == 'payouttxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                and internal_balance[i]['amount'] == fee_amount \
                                and internal_balance[i]['movement_type'] == 1 \
                                and internal_balance[i]['code'] == ccy:
                            logger.info('币种{}在交易阶段：Ready-Executing,贷方向(movement_typ=1)transaction fee的动账正确', ccy)
                            with allure.step("检查wallet name"):
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Revenue Fee-{}'.format(ccy), \
                                        "期望返回结果是:'LT-Revenue Fee-{}'，实际结果是:{}".format(ccy, wallet_name[0]['wallet_name'])
                        elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                            "to": "Executing", "from": "Ready"} \
                                and internal_balance[i]['requested_by'] == 'payouttxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                                and internal_balance[i]['amount'] == fee_amount \
                                and internal_balance[i]['movement_type'] == 2 \
                                and internal_balance[i]['code'] == ccy:
                            logger.info('币种{}在交易阶段：Ready-Executing,借方向(movement_typ=2)transaction fee的动账正确', ccy)
                            with allure.step("检查wallet name"):
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Payment Transition-{}'.format(ccy), \
                                        "期望返回结果是:'LT-Payment Transition-{}'，实际结果是:{}".format(ccy,
                                                                                             wallet_name[0]['wallet_name'])
                        else:
                            assert False, "transaction动账错误，错误的动账为：{}".format(internal_balance[i])
        with allure.step("查客户账"):
            with allure.step("client balance表"):
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
                assert wallet_name[0]['wallet_name'] == '', '客户wallet name错误'
        with allure.step("查order的动账"):
            sql = "select * from payoutorder.order where transaction_id = '{}';".format(transaction_id)
            order_original = sqlFunction().connect_mysql('payoutorder', sql=sql)
            order = order_original[0]
            assert order['status'] == 'PAYOUT_ORDER_STATUS_SUCCEEDED' and order['ccy'] == ccy and Decimal(
                order['amount']) == Decimal(amount) - Decimal(fee_amount), 'order错误'
            order_id = order['order_id']
            chain = order['chain']
            sql = "select * from wallet.internal_balance where transaction_id = '{}';".format(order_id)
            internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert len(internal_balance) == 4, 'payout order 动账少记了'
            with allure.step("检查order4笔动账"):
                for i in range(0, len(internal_balance)):
                    if json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Executing", "from": "Created"} \
                            and internal_balance[i]['requested_by'] == 'payoutorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                            and Decimal(internal_balance[i]['amount']) == Decimal(amount) - Decimal(fee_amount) \
                            and internal_balance[i]['movement_type'] == 1 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created-Executing,贷方向(movement_type=1)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Payment Clearing-FireBlocks-{}'.format(ccy), \
                                    "期望返回结果是:'LT-Payment Clearing-FireBlocks-{}'，实际结果是:{}".format(ccy, wallet_name[0][
                                        'wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Executing", "from": "Created"} \
                            and internal_balance[i]['requested_by'] == 'payoutorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                            and Decimal(internal_balance[i]['amount']) == Decimal(amount) - Decimal(fee_amount) \
                            and internal_balance[i]['movement_type'] == 2 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created-Executing,借方向(movement_type=2)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Payment Transition-{}'.format(ccy), \
                                    "期望返回结果是:'LT-Payment Transition-{}'，实际结果是:{}".format(ccy, wallet_name[0]['wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Succeeded", "from": "Executing"} \
                            and internal_balance[i]['requested_by'] == 'payoutorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                            and Decimal(internal_balance[i]['amount']) == Decimal(amount) - Decimal(fee_amount) \
                            and internal_balance[i]['movement_type'] == 1 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Executing-Succeeded,贷方向(movement_type=1)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Cash MP-FireBlocks-{}_{}'.format(ccy, chain), \
                                    "期望返回结果是:'LT-Cash MP-FireBlocks-{}_{}'，实际结果是:{}".format(ccy, chain,
                                                                                            wallet_name[0]['wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Succeeded", "from": "Executing"} \
                            and internal_balance[i]['requested_by'] == 'payoutorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Payment' \
                            and Decimal(internal_balance[i]['amount']) == Decimal(amount) - Decimal(fee_amount) \
                            and internal_balance[i]['movement_type'] == 2 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Executing-Succeeded,借方向(movement_type=2)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Payment Clearing-FireBlocks-{}'.format(ccy), \
                                    "期望返回结果是:'LT-Payment Clearing-FireBlocks-{}'，实际结果是:{}".format(ccy, wallet_name[0][
                                        'wallet_name'])
                    else:
                        assert False, "order动账错误，错误的动账为：{}".format(internal_balance[i])


    # crypto-payin accounting(ETH/USDT/BTC)
    @staticmethod
    def crypto_payin_accouting(transaction_id):
        with allure.step("查询payin transaction"):
            sql = "select * from transaction where transaction_id = '{}';".format(transaction_id)
            payin_txn = (sqlFunction().connect_mysql('payintxn', sql=sql))[0]
            transaction_id = payin_txn['transaction_id']
            order_id = payin_txn['order_id']
            ccy = payin_txn['ccy']
            amount = payin_txn['amount']
            fee = json.loads(payin_txn['fee'])
            if fee == '':
                fee_amount = '0'
            else:
                fee_amount = fee['ccy']['amount']['amount']
        with allure.step("查transaction的动账"):
            with allure.step("查internal balance表"):
                sql = "select * from internal_balance where transaction_id = '{}';".format(transaction_id)
                internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
                assert len(internal_balance) == 3, 'payin transaction 动账少记了'
                with allure.step("检查3笔动账"):
                    for i in range(0, len(internal_balance)):
                        if json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                            "to": "Succeed", "from": "Pending"} \
                                and internal_balance[i]['requested_by'] == 'payintxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                                and internal_balance[i]['amount'] == amount \
                                and internal_balance[i]['movement_type'] == 2 \
                                and internal_balance[i]['code']:
                            logger.info('币种{}在交易阶段：Pending-Succeed,transaction本金的动账正确', ccy)
                            with allure.step("检查wallet name"):
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Collection Transition-{}'.format(ccy)
                        elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                            "to": "New", "from": ""} \
                                and internal_balance[i]['requested_by'] == 'payintxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                                and internal_balance[i]['amount'] == fee_amount \
                                and internal_balance[i]['movement_type'] == 1 \
                                and internal_balance[i]['code'] == ccy:
                            logger.info('币种{}在交易阶段：New,贷方向(movement_type=1)的transaction fee动账正确', ccy)
                            with allure.step("检查wallet name"):
                                logger.info('贷方向fee的动账正确')
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Revenue Fee_Deposit-{}'.format(ccy)
                        elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                            "to": "New", "from": ""} \
                                and internal_balance[i]['requested_by'] == 'payintxn' \
                                and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                                and internal_balance[i]['amount'] == fee_amount \
                                and internal_balance[i]['movement_type'] == 2 \
                                and internal_balance[i]['code'] == ccy:
                            logger.info('币种{}在交易阶段：New,借方向(movement_type=2)的transaction fee动账正确', ccy)
                            with allure.step("检查wallet name"):
                                wallet_id = internal_balance[i]['wallet_id']
                                with allure.step("检查wallet name"):
                                    sql = "select * from wallet where wallet_id = '{}';".format(
                                        wallet_id)
                                    wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                    assert wallet_name[0]['wallet_name'] == 'LT-Collection Transition-{}'.format(ccy)
                        else:
                            assert False, "transaction动账错误，错误的动账为：{}".format(internal_balance[i])
        with allure.step("查客户账"):
            with allure.step("查client balance表"):
                sql = "select * from client_balance where transaction_id = '{}';".format(transaction_id)
                client_balance = sqlFunction().connect_mysql('wallet', sql=sql)
                wallet_id = client_balance[0]['wallet_id']
                assert client_balance[0]['code'] == ccy and client_balance[0]['amount'] == amount \
                       and client_balance[0]['requested_by'] == 'payintxn' \
                       and client_balance[0]['transaction_sub_type'] == 'Collection', '客户账记账错误,'
            with allure.step("检查wallet name"):
                sql = "select * from wallet where wallet_id = '{}';".format(
                    wallet_id)
                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                assert wallet_name[0]['wallet_name'] == '', '客户wallet name错误'
        with allure.step("查order的动账"):
            sql = "select * from payinorder.order where order_id = '{}';".format(order_id)
            order_original = sqlFunction().connect_mysql('payinorder', sql=sql)
            order = order_original[0]
            print(ccy + 'payin order 为:' + order)
            assert order['status'] == 'PAYIN_ORDER_STATUS_SUCCEEDED' and order['ccy'] == ccy and Decimal(
                order['amount']) == Decimal(amount) - Decimal(fee_amount), 'order错误'
            chain = order['chain']
            sql = "select * from wallet.internal_balance where transaction_id = '{}';".format(order_id)
            internal_balance = sqlFunction().connect_mysql('wallet', sql=sql)
            assert len(internal_balance) == 6, 'payin order 动账少记了'
            with allure.step("检查order6笔动账"):
                for i in range(0, len(internal_balance)):
                    if json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Created", "from": ""} \
                            and internal_balance[i]['requested_by'] == 'payinorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Unknown' \
                            and Decimal(internal_balance[i]['amount']) == amount \
                            and internal_balance[i]['movement_type'] == 1 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created阶段,step=0,贷方向(movement_type=1)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Pending PayIn -FireBlocks-{}'.format(ccy), \
                                    "期望返回结果是:''LT-Pending PayIn -FireBlocks-{}''，实际结果是:{}".format(ccy, chain,
                                                                                                  wallet_name[0][
                                                                                                      'wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Created", "from": ""} \
                            and internal_balance[i]['requested_by'] == 'payinorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Unknown' \
                            and internal_balance[i]['amount'] == amount \
                            and internal_balance[i]['movement_type'] == 2 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created阶段,step=0,借方向(movement_type=2)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Collection Clearing-FireBlocks-{}'.format(ccy), \
                                    "期望返回结果是:'LT-Collection Clearing-FireBlocks-{}'，实际结果是:{}".format(ccy, chain,
                                                                                                     wallet_name[0][
                                                                                                         'wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Succeeded", "from": "Created"} \
                            and json.loads(internal_balance[i]['detail']['route_wallet']['step'] == 0) \
                            and internal_balance[i]['requested_by'] == 'payinorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                            and internal_balance[i]['amount'] == amount \
                            and internal_balance[i]['movement_type'] == 1 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created-Success阶段,step=0,贷方向(movement_type=1)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Collection Clearing-FireBlocks-{}'.format(ccy), \
                                    "期望返回结果是:'LT-Collection Clearing-FireBlocks-{}'，实际结果是:{}".format(ccy, wallet_name[0][
                                        'wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Success", "from": "Created"} \
                            and json.loads(internal_balance[i]['detail']['route_wallet']['step'] == 0) \
                            and internal_balance[i]['requested_by'] == 'payin' \
                            and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                            and internal_balance[i]['amount'] == amount \
                            and internal_balance[i]['movement_type'] == 2 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created-Success阶段,step=0,贷方向(movement_type=2)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Cash CA-FireBlocks-{}_{}'.format(ccy, chain), \
                                    "期望返回结果是:'LT-Cash CA-FireBlocks-{}_{}'，实际结果是:{}".format(ccy, chain,
                                                                                            wallet_name[0]['wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Succeeded", "from": "Created"} \
                            and json.loads(internal_balance[i]['detail']['route_wallet']['step'] == 0) \
                            and internal_balance[i]['requested_by'] == 'payinorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                            and internal_balance[i]['amount'] == amount \
                            and internal_balance[i]['movement_type'] == 1 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created-Success阶段,step=0,贷方向(movement_type=1)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Collection Clearing-FireBlocks-{}'.format(ccy), \
                                    "期望返回结果是:'LT-Collection Clearing-FireBlocks-{}'，实际结果是:{}".format(ccy, wallet_name[0][
                                        'wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Success", "from": "Created"} \
                            and json.loads(internal_balance[i]['detail']['route_wallet']['step'] == 0) \
                            and internal_balance[i]['requested_by'] == 'payin' \
                            and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                            and internal_balance[i]['amount'] == amount \
                            and internal_balance[i]['movement_type'] == 2 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created-Success阶段,step=0,贷方向(movement_type=2)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Cash CA-FireBlocks-{}_{}'.format(ccy, chain), \
                                    "期望返回结果是:'LT-Cash CA-FireBlocks-{}_{}'，实际结果是:{}".format(ccy, chain,
                                                                                            wallet_name[0]['wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Succeeded", "from": "Created"} \
                            and json.loads(internal_balance[i]['detail']['route_wallet']['step'] == 1) \
                            and internal_balance[i]['requested_by'] == 'payinorder' \
                            and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                            and internal_balance[i]['amount'] == amount \
                            and internal_balance[i]['movement_type'] == 1 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created-Success阶段,step=1,贷方向(movement_type=1)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Collection Transition-{}'.format(ccy), \
                                    "期望返回结果是:'LT-Collection Transition-{}'，实际结果是:{}".format(ccy,
                                                                                            wallet_name[0]['wallet_name'])
                    elif json.loads(internal_balance[i]['detail'])['route_wallet']['status_transitions'] == {
                        "to": "Success", "from": "Created"} \
                            and json.loads(internal_balance[i]['detail']['route_wallet']['step'] == 1) \
                            and internal_balance[i]['requested_by'] == 'payin' \
                            and internal_balance[i]['transaction_sub_type'] == 'Collection' \
                            and internal_balance[i]['amount'] == amount \
                            and internal_balance[i]['movement_type'] == 2 \
                            and internal_balance[i]['code'] == ccy:
                        logger.info('币种{}在交易阶段：Created-Success阶段,step=1,贷方向(movement_type=2)的order动账正确', ccy)
                        with allure.step("检查wallet name"):
                            wallet_id = internal_balance[i]['wallet_id']
                            with allure.step("检查wallet name"):
                                sql = "select * from wallet where wallet_id = '{}';".format(
                                    wallet_id)
                                wallet_name = sqlFunction().connect_mysql('wallet', sql=sql)
                                assert wallet_name[0]['wallet_name'] == 'LT-Pending PayIn -FireBlocks-{}'.format(ccy), \
                                    "期望返回结果是:'LT-Pending PayIn -FireBlocks-{}'，实际结果是:{}".format(ccy, wallet_name[0][
                                        'wallet_name'])
                    else:
                        assert False, "order动账错误，错误的动账为：{}".format(internal_balance[i])