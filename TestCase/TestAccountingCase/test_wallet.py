import json

from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("accounting 相关 testcases")
class TestAccountingApi:

    # 初始化class
    def setup_method(self):
        pass

    # def test_accounting_001(self):
    #     for i in OperateExcel.get_excel_sheet_names():
    #         print(i)

    def test_accounting_002(self):
        for i in range(1, OperateExcel.get_excel_sheet_all_row_number('Cash Wallet')):
            line_info = OperateExcel.get_excel_sheet_row('Cash Wallet', i)
            with allure.step("判断是否需要"):
                if 'Yes' in str(line_info[17]):
                    with allure.step("账户状态"):
                        if '正常' in str(line_info[16]):
                            status = 1
                        else:
                            status = 2
                    with allure.step("是否可透支"):
                        if 'Yes' in str(line_info[15]):
                            allow_overdraft = 1
                        else:
                            allow_overdraft = 2
                    with allure.step("借贷关系"):
                        if 'Debit' in str(line_info[13]).split(':')[1]:
                            balance_direction = 2
                        else:
                            balance_direction = 1
                    with allure.step("账户子类型"):
                        wallet_subType = str(line_info[8]).split('(')[0].split(":'")[1].strip()
                    sql = "select * from wallet where wallet_name = {} and code = {} and account_code = {} and status = {} and allow_overdraft = {} and balance_direction = {} and wallet_type = {};".format(
                        str(line_info[3]).split(':')[1], str(line_info[5]).split(':')[1], int(float(str(line_info[9]).split(':')[1])), status, allow_overdraft, balance_direction, wallet_subType)
                    info = sqlFunction().connect_mysql('wallet', sql=sql)
                    print(info[0])
                    print(info[0]['code'])
