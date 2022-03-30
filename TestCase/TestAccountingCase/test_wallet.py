from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("accounting 相关 testcases")
class TestAccountingApi:

    # 初始化class
    def setup_method(self):
        pass

    def test_accounting_001(self):
        for i in OperateExcel.get_excel_sheet_names():
            print(i)

    def test_accounting_002(self):
        for i in range(1, OperateExcel.get_excel_sheet_all_row_number('Cash Wallet')):
            line_info = OperateExcel.get_excel_sheet_row('Cash Wallet', i)
            sql = "select * from wallet where wallet_name = '{}';".format(line_info[3])
            info = sqlFunction().connect_mysql('wallet', sql=sql)
            print(info)
