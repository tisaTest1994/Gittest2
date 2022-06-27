from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("moneyhouse 相关 testcases")
class TestMoneyHouseApi:

    money_house_path = os.path.split(os.path.realpath(__file__))[0] + '/../../Resource/MoneyHouse Account.xlsx'

    # 初始化class
    def setup_method(self):
        pass
    #
    # @allure.title('test_money_house_001')
    # @allure.description('money house 验证')
    # def test_money_house_001(self):
    #     sheet_name = 'Crypto'
    #     error_list = []
    #     for i in range(1, OperateExcel.get_excel_sheet_all_row_number(sheet_name, path=self.money_house_path)):
    #         line_info = OperateExcel.get_excel_sheet_row(sheet_name, i, path=self.money_house_path)
    #         if str(line_info[3]).split(':')[1] == 'CA':
    #             type = 1
    #         elif str(line_info[3]).split(':')[1] == 'MP':
    #             type = 2
    #         elif str(line_info[3]).split(':')[1] == 'COST':
    #             type = 3
    #         else:
    #             type = 0
    #         sql = "select * from money_house_account where code = {} and address = {} and nick_name = {} and network = {} and type = {};".format(str(line_info[2]).split(':')[1], str(line_info[5]).split(':')[1], str(line_info[4]).split(':')[1], str(line_info[0]).split(':')[1], type)
    #         info = sqlFunction().connect_mysql('moneyhouse', sql=sql)
    #         if not list(info):
    #             error_list.append(sql)
    #     assert error_list == [], 'money house 错误, 错误list是{}'.format(error_list)

    @allure.title('test_money_house_002')
    @allure.description('money house kend和')
    def test_money_house_002(self):
        sheet_name = 'Crypto'
        for i in range(1, OperateExcel.get_excel_sheet_all_row_number(sheet_name, path=self.money_house_path)):
            line_info = OperateExcel.get_excel_sheet_row(sheet_name, i, path=self.money_house_path)
            sql = "select money_house_id from money_house where id = (select money_house_id from moneyhouse.money_house_account where nick_name = {});".format(str(line_info[4]).split(':')[1])
            info = sqlFunction().connect_mysql('moneyhouse', sql=sql)
            print(info)
            print(1111111)
            money_house_id = info[0]['money_house_id']
            print(money_house_id)


