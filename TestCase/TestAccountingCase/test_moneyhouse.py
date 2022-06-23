from Function.api_function import *
from Function.operate_excel import *
from Function.operate_sql import *


@allure.feature("moneyhouse 相关 testcases")
class TestMoneyHouseApi:

    money_house_path = os.path.split(os.path.realpath(__file__))[0] + '/../../Resource/MoneyHouse Account.xlsx'

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_money_house_001')
    @allure.description('money house 验证')
    def test_money_house_001(self):
        sheet_name = 'Crypto'
        error_list = []
        for i in range(1, OperateExcel.get_excel_sheet_all_row_number(sheet_name, path=self.money_house_path)):
            line_info = OperateExcel.get_excel_sheet_row(sheet_name, i, path=self.money_house_path)
            sql = "select * from money_house_account where code = {} and address = {} and nick_name = {};".format(str(line_info[2]).split(':')[1], str(line_info[5]).split(':')[1], str(line_info[4]).split(':')[1])
            info = sqlFunction().connect_mysql('moneyhouse', sql=sql)
            if not list(info):
                error_list.append(sql)
        assert error_list == [], 'money house 错误, 错误list是{}'.format(error_list)