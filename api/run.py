import unittest
from BeautifulReport import BeautifulReport
from config import *
from lib.send_email import send_email
from lib.get_lastest_file import get_lastest_file


def test_suite():
    suite = unittest.defaultTestLoader.discover(test_case_path, pattern="*_test.py")
    return suite


def run(suite):
    if not os.path.exists(report_path):
        os.popen("mkdir {}".format(report_path))
    logging.info("=" * 30 + "测试开始" + "=" * 30)
    result = BeautifulReport(suite)
    result.report(filename='report_{}.html'.format(now), description='接口测试', report_dir=report_path,
                  theme='theme_cyan')
    count_num = result.testsRun
    fail_num = result.failure_count
    error_num = result.error_count
    pass_num = result.success_count
    rate = (pass_num / count_num) * 100
    print(count_num, pass_num, fail_num, error_num, rate)

    # 发送邮件
    if send_email_after_run:
        send_email(get_lastest_file(), count_num, pass_num, fail_num, error_num, rate)
    logging.info("=" * 30 + "测试结束" + "=" * 30)


if __name__ == '__main__':
    run(test_suite())
