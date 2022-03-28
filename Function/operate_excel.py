import xlrd


# 获取excel sheet names
def get_excel_sheet_names(path):
    workbook = xlrd.open_workbook(path)
    return workbook.sheet_names()


# 获取excel sheet行数据
def get_excel_sheet_row(path, line):
    sheet2 = get_excel_sheet_names(path)
    sheet2 = workbook.sheet_by_name('Accounting Subject')
    print(sheet2.col_values(2))


# 获取excel sheet列数据
def get_excel_sheet_column(path):
    workbook = xlrd.open_workbook(path)
    sheet2 = workbook.sheet_by_name('Accounting Subject')



