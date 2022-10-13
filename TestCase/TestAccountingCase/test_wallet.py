from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("accounting 相关 testcases")
class TestAccountingWalletApi:

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_accounting_wallet_001')
    @allure.description('wallet 验证')
    def test_accounting_wallet_001(self):
        error_list = []
        for y in OperateExcel.get_excel_sheet_names():
            if 'Wallet' in y and 'Entity-Clearing Wallet' not in y:
                for i in range(1, OperateExcel.get_excel_sheet_all_row_number(y)):
                    line_info = OperateExcel.get_excel_sheet_row(y, i)
                    with allure.step("判断是否需要"):
                        if 'Yes' in str(line_info[16]):
                            if 'Cabital-Connect Wallet' in y:
                                with allure.step("账户状态"):
                                    if '正常' in str(line_info[15]):
                                        status = 1
                                    else:
                                        status = 2
                                with allure.step("是否可透支"):
                                    if 'Yes' in str(line_info[14]):
                                        allow_overdraft = 1
                                    else:
                                        allow_overdraft = 0
                                with allure.step("借贷关系"):
                                    if 'Debit' in str(line_info[12]).split(':')[1]:
                                        balance_direction = 2
                                    else:
                                        balance_direction = 1
                                with allure.step("账户子类型"):
                                    if '(' in str(line_info[7]):
                                        wallet_subType = str(line_info[7]).split('(')[0].split(":'")[1]
                                    else:
                                        wallet_subType = str(line_info[7]).split("'")[1]
                                with allure.step("Account_Type"):
                                    account_type = str(line_info[5]).split('=')[1].split("'")[0]
                                sql = "select * from wallet where code = {} and account_code = {} and status = {} and allow_overdraft = {} and balance_direction = {} and wallet_type = '{}' and account_type = '{}';".format(
                                    str(line_info[4]).split(':')[1], int(float(str(line_info[8]).split(':')[1])),
                                    status, allow_overdraft, balance_direction, wallet_subType, account_type)
                                info = sqlFunction().connect_mysql('wallet', sql=sql)
                                if not list(info):
                                    error_list.append({y: sql})
                            else:
                                with allure.step("账户状态"):
                                    if '正常' in str(line_info[15]):
                                        status = 1
                                    else:
                                        status = 2
                                with allure.step("是否可透支"):
                                    if 'Yes' in str(line_info[14]):
                                        allow_overdraft = 1
                                    else:
                                        allow_overdraft = 0
                                with allure.step("借贷关系"):
                                    if 'Debit' in str(line_info[12]).split(':')[1]:
                                        balance_direction = 2
                                    else:
                                        balance_direction = 1
                                with allure.step("账户子类型"):
                                    if '(' in str(line_info[7]):
                                        wallet_subType = str(line_info[7]).split('(')[0].split(":'")[1]
                                    else:
                                        wallet_subType = str(line_info[7]).split("'")[1]
                                with allure.step("Currency 币种解析"):
                                    if ',' in str(line_info[4]).split(':')[1]:
                                        currency_list = str(line_info[4]).split(':')[1].strip("'").split(',')
                                        for z in currency_list:
                                            sql = "select * from wallet where code = {} and account_code = {} and status = {} and allow_overdraft = {} and balance_direction = {} and wallet_type = '{}';".format(
                                                z,
                                                int(float(str(line_info[8]).split(':')[1])),
                                                status, allow_overdraft, balance_direction, wallet_subType)
                                            print(sql)
                                            info = sqlFunction().connect_mysql('wallet', sql=sql)
                                            if not list(info):
                                                error_list.append({y: sql})
                                    else:
                                        sql = "select * from wallet where code = {} and account_code = {} and status = {} and allow_overdraft = {} and balance_direction = {} and wallet_type = '{}';".format(
                                            str(line_info[4]).split(':')[1],
                                            int(float(str(line_info[8]).split(':')[1])),
                                            status, allow_overdraft, balance_direction, wallet_subType)
                                        info = sqlFunction().connect_mysql('wallet', sql=sql)
                                        if not list(info):
                                            error_list.append({y: sql})
        logger.info(error_list)
        assert error_list == [], 'error list 是{}'.format(error_list)

    @allure.title('test_accounting_wallet_002')
    @allure.description('ledger 测试')
    def test_accounting_wallet_002(self):
        error_list = []
        for i in range(1, OperateExcel.get_excel_sheet_all_row_number('Accounting Subject')):
            line_info = OperateExcel.get_excel_sheet_row('Accounting Subject', i)
            with allure.step("判断是否需要"):
                with allure.step("判断是否需要"):
                    if 'Yes' in str(line_info[9]):
                        if "empty:''" not in str(line_info[0]):
                            with allure.step("科目类别"):
                                if 'ASSET' in str(line_info[5]):
                                    category = 1
                                elif 'LIABILITY' in str(line_info[5]):
                                    category = 2
                                elif 'EQUITY' in str(line_info[5]):
                                    category = 3
                                elif 'PROFIT_AND_LOSS' in str(line_info[5]):
                                    category = 4
                                else:
                                    category = 0
                            with allure.step("科目状态"):
                                if 'Enable' in str(line_info[6]):
                                    status = 1
                                else:
                                    status = 2
                            with allure.step("借贷关系"):
                                if 'Debit' in str(line_info[7]):
                                    balance_direction = 2
                                else:
                                    balance_direction = 1
                            with allure.step("parent_code"):
                                if "empty:''" in str(line_info[8]):
                                    parent_code = ''
                                else:
                                    parent_code = int(float(str(line_info[8]).split(':')[1]))
                            sql = "select * from accounting_subject where name = {} and code = {} and level = {} and status = {} and category = {} and direction = {} and parent_code = '{}';".format(
                                str(line_info[1]).split(':')[1], int(float(str(line_info[0]).split(':')[1])),
                                int(float(str(line_info[4]).split(':')[1])), status, category, balance_direction,
                                parent_code)
                            info = sqlFunction().connect_mysql('ledger', sql=sql)
                            if not list(info):
                                error_list.append(sql)
        logger.info(error_list)
        assert error_list == [], 'error list 是{}'.format(error_list)
