import os
from config import prj_path


def get_lastest_file():
    report_file_path = prj_path + '\\' + 'report'
    file_list = os.listdir(report_file_path)
    file_list.sort(key=lambda x: os.path.getmtime(report_file_path + '\\'))
    # print(os.path.join(prj_path, 'report', file_list[-1]))
    return os.path.join(prj_path, 'report', file_list[-1])


if __name__ == '__main__':
    print(get_lastest_file())
