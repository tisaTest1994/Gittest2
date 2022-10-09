from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("PayOut accounting相关 testcases")
class TestPayOutAccountingApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_payout_accounting_001')
    @allure.description('Payout Crypto Accounting校验')
    def test_payout_accounting_001(self):
        for currency in ['ETH', 'USDT', 'BTC']:
            if currency == 'ETH':
                amount = '0.02'
                address = '0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C'
            elif currency == 'USDT':
                amount = '40'
                address ='0xf48e06660E4d3D7Cf89B6977463379bcCD5c0d1C'
            else:
                amount = '0.01'
                address = 'tb1qqfs5u6lhqgcl2d40p203756ls6x2jqn89amnv3'
            with allure.step("生成一笔ETH payout订单"):
                transaction_id = ApiFunction.get_payout_transaction_id(amount=amount, address=address, code_type=currency)
                ApiFunction.crypto_payout_accouting(transaction_id)

