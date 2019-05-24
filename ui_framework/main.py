# coding=utf-8
import os
import threading
from Function.App01.CommonLib.installApp import AppManage
from Function.App01.CommonLib.computerInfo import ComputerInfo
from Function.App01.CommonLib.ATXPackage import U2
from Function.App01.TestData.filePath import Path, pkg_name
from Function.App01.CommonLib.AppiumPackage import Appium
from Function.App01.CommonLib.email import SendEmail
from Function.App01.CommonLib.fileOperation import Compression
from Function.App01.CommonLib.HTMLTestRunner import HTMLTestRunner
from Function.App01.CommonLib.log import Analyse
from Function.App01.TestSuit.smoke_test import SmokeTest

#                           APP功能测试系统工作流程
# =============================================================================
#   01.轮询检测安装包(轮询时间可设置)
#   02.启动ATX服务程序辅助完成apk文件的安装
#   03.关闭ATX服务，启动appium并进行初始化(向服务器传递配置信息)
#   04.开启监控线程(检测和处理执行测试用例期间的系统弹窗和app内的弹窗)
#   05.设置测试报告生成路径和格式(默认为txt格式，该系统定制为主流的html格式)
#   06.创建测试套件，加载测试用例(unittest测试组件的testSuite模块)
#   07.执行组装好的测试套件，收集测试过程中产生的相关数据用于生成测试报告
#   08.关闭监控线程和appium服务程序
#   09.分析测试日志并提取anr、crash相关信息
#   10.压缩并保存测试数据和测试结果至公盘指定目录
#   11.根据测试数据生成测试报告
#   12.邮件通知相关部门(测试报告截图和日志信息)
# =============================================================================

# 设置发件人的邮箱地址和邮箱密码
username = input('请输入发件人地址：')
password = input('请输入邮箱密码：')

# 检测待测包并安装(先设置待测APP的路径)
manage = AppManage(pkg_name, Path.path['apk_path'])
atx = U2()
d = atx.init()
manage.monitor()

# 初始化appium连接
app = Appium()
app.check_appium_server()

# 弹窗监控
thread1 = threading.Thread(target=app.system_alert)
thread2 = threading.Thread(target=app.app_alert)
thread1.start()
thread2.start()

# 设置生成测试报告路径, 执行测试并记录测试报告
pc = ComputerInfo()
suite = SmokeTest()
testReport = os.path.join(Path.path['report_path'], '双开测试报告%s.html' % pc.get_time())
with open(testReport, 'wb') as f:
    runner = HTMLTestRunner(stream=f, title='双开助手自动化回归测试报告', description='测试结果饼状图展示')
    # 加载测试套件
    runner.run(suite.create_test_suite())

# 停止弹窗监控, 结束appium会话
app.stop_thread()
app.stop_appium_server()

# 测试用例执行完毕，分析log
log_analyse = Analyse(log_path=Path.path['log_path'], anr_path=Path.path['anr_log_path'],
                      crash_path=Path.path['crash_log_path'])
log_analyse.catch_anr_and_crash()

# 压缩并保存测试结果(数据存入MySQL)
compress = Compression()
compress.compress_dir(Path.path['data_save_path'], Path.path['log_path'])

# 发送测试报告邮件
report = SendEmail(username, password, state='debug', file_path=Path.path['data_save_path'],
                   html_path=Path.path['report_path'])
report.create_email()
