import xlrd
import os



class OperateExcel:

    path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/Accounting Route Configuration.xlsx'

    # 获取excel sheet names
    @staticmethod
    def get_excel_sheet_names(path=path):
        workbook = xlrd.open_workbook(path)
        return workbook.sheet_names()

    # 获取一个sheet的总行数
    @staticmethod
    def get_excel_sheet_all_row_number(sheet_name, path=path):
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_name(sheet_name)
        return sheet.nrows

    # 获取excel一个sheet某行数据
    @staticmethod
    def get_excel_sheet_row(sheet_name, row, path=path):
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_name(sheet_name)
        return sheet.row_slice(row)

    # 获取excel sheet列数据
    @staticmethod
    def get_excel_sheet_column(path):
        workbook = xlrd.open_workbook(path)
        sheet2 = workbook.sheet_by_name('Accounting Subject')

    @staticmethod
    def get_product_limit(sheet_name='Acquiring', path=os.path.split(os.path.realpath(__file__))[0] + '/../Resource/Product Limit.xlsx'):
        row = OperateExcel.get_excel_sheet_all_row_number(sheet_name, path=path)
        product_limit_list = []
        for i in range(1, row):
            line = OperateExcel.get_excel_sheet_row(sheet_name, i, path=path)
            product_limit_list.append({'code': str(line[0]).split(':')[1].replace("'", ""), 'transaction_type':
                str(line[1]).split(':')[1].replace("'", ""), 'min': str(line[5]).split(':')[1], 'max': str(line[4]).split(':')[1]})
        return product_limit_list
