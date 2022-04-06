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



