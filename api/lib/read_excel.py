import xlrd
from config import *


def excel_to_list(datafile, sheet, modal=''):
    data = []  # 新建个空列表，来乘装所有的数据
    wb = xlrd.open_workbook(datafile)  # 打开excel
    sh = wb.sheet_by_name(sheet)  # 获取工作簿
    header = sh.row_values(0)  # 获取标题行数据
    for i in range(1, sh.nrows):  # 跳过标题行，从第二行开始取数据
        d = dict(zip(header, sh.row_values(i)))  # 将标题和每行数据组装成字典
        if modal == 'smoke':
            if d['smoke'] == 1:
                data.append(d)
        elif modal == 'all':
            data.append(d)
    return data  # 列表嵌套字典格式，每个元素是一个字典


def get_test_data(data, case_name='', serial=''):
    if serial:
        for case in data:
            if serial == case['id']:
                return case
    for case in data:
        if case_name == case['name']:  # 如果字典数据中case_name与参数一致
            return case
            # 如果查询不到会返回None
    logging.error("用例数据不存在")


if __name__ == '__main__':
    data_list = excel_to_list(test_data_file, "case")
    # print(data_list)
    case_data = get_test_data(data_list, 'AddressList')
    print(case_data['data'])
