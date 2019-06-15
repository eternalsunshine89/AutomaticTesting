import logging
import os
import time
from optparse import OptionParser

# 切换测试环境
ENV = 'test'
HOST = ''
BASE_URL = ''

# 切换测试模式(smoke-冒烟测试)
MODAL = 'all'

# 时间/日期获取
today = time.strftime('%Y%m%d', time.localtime())
now = time.strftime('%Y%m%d_%H%M%S', time.localtime())

# 文件路径
prj_path = os.path.dirname(os.path.abspath(__file__))  # 项目路径(根目录)
test_case_path = os.path.join(prj_path, 'cases\case')  # 用例路径
if not os.path.exists("log"):
    os.popen("mkdir {}".format("log"))
    time.sleep(1)
log_file = os.path.join(prj_path, 'log', 'log_{}.txt'.format(today))  # log文件
report_path = os.path.join(prj_path, 'report')  # 测试报告存放路径
test_data_file = os.path.join(prj_path, 'test/cases', 'test_data.xlsx')  # 测试数据存放路径
testlist_file = os.path.join(prj_path, 'test_case', 'testlist.txt')  # 测试用例执行列表文件路径
failed_case_file = os.path.join(prj_path, 'failed_case', 'failed_{}.pickle'.format(now))  # 运行失败用例集文件路径

# log配置
logging.basicConfig(
    # log级别
    level=logging.INFO,
    # log格式
    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
    # 日期格式
    datefmt='%Y-%m-%d %H:%M:%S',
    # 日志输出文件
    filename=log_file,
    # 追加模式
    filemode='a')

# 数据库配置
db_host = 'localhost'
db_port = 3306
db_user = 'root'
db_passwd = 'root'
db = 'test'

# 邮件配置
smtp_server = 'smtp.163.com'
smtp_user = 'eternalsunshine89@163.com'
smtp_password = 'sunshine89'
sender = smtp_user  # 发件人
receiver = 'eternalsunshine89@163.com'  # 收件人
subject = '接口自动化测试报告'  # 邮件主题
send_email_after_run = 0  # 邮件发送开关

# 用例运行配置
collect_failed_case = 0  # 失败用例重跑

# 配置命令行运行参数
parser = OptionParser()
parser.add_option('--testsuite', action='store', dest='testsuite', help='运行指定的TestSuite')

# 命令行模式运行生效
(options, args) = parser.parse_args()
