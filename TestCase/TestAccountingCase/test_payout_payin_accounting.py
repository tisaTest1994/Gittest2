from Function.api_function import *
from Function.accounting import *
from Function.operate_sql import *


@allure.feature("PayOut & PayIn accounting相关 testcases")
class TestPayOutPayInAccountingApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_payout_payin_accounting_001')
    @allure.description('Payout&Payin Crypto Accounting校验')
    def test_payout_payin_accounting_001(self):
        account_id = 'b013327e-ae65-4197-acf6-806f03873f51'
        for currency in ['ETH', 'USDT', 'BTC']:
            # 提现的地址用的account_id = 'b013327e-ae65-4197-acf6-806f03873f51'这个账号的地址（为了方便查payin）
            if currency == 'ETH':
                amount = random.uniform(0.02, 0.39999999)
                amount = format(amount, '.8f')
                fee = '0.004'
                address = '0xb34876a77826F1bb564872e0470c242e561e68be'
            elif currency == 'USDT':
                amount = random.uniform(40, 500.999999)
                amount = format(amount, '.6f')
                fee = '12'
                address ='0xb34876a77826F1bb564872e0470c242e561e68be'
            else:
                amount = random.uniform(0.001, 0.002)
                amount = format(amount, '.8f')
                fee = '0.0006'
                address = 'tb1qqfs5u6lhqgcl2d40p203756ls6x2jqn89amnv3'
            with allure.step("生成一笔payout订单"):
                transaction_id = ApiFunction.get_payout_transaction_id(amount=amount, address=address, code_type=currency)
            with allure.step("payout账务测试"):
                AccountingFunction.crypto_payout_accouting(transaction_id)
            with allure.step("通过payout查询对应一笔payin"):
                sql = "select * from payintxn.transaction where account_id = '{}' and ccy='{}' and amount= '{}' order by id desc limit 1;".format(account_id, currency, Decimal(amount)-Decimal(fee))
                payin_txn = (sqlFunction().connect_mysql('payintxn', sql=sql))[0]
                transaction_id = payin_txn['transaction_id']
            with allure.step("payin账务测试"):
                AccountingFunction.crypto_payin_accouting(transaction_id)

