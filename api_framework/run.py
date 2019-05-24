from BeautifulReport import BeautifulReport
from config.config import *
from lib.send_email import send_email
import pickle
from test_case.test_suite.test_suites import *
from lib.get_lastest_file import get_lastest_file


def discover():
    return unittest.defaultTestLoader.discover(test_case_path)


def save_failures(result, failed_case_file):
    suite = unittest.TestSuite()
    for case_result in result.failures:
        suite.addTest(case_result[0])  # 组装失败的用例，case_result是一个元组，第一个元素是用例对象
    with open(failed_case_file, 'wb') as f:
        pickle.dump(suite, f)  # 使用pickle序列化失败的用例


def collect():
    suite = unittest.TestSuite()

    def _collect(tests):
        if isinstance(tests, unittest.TestSuite):
            if tests.countTestCases() != 0:
                for i in tests:
                    _collect(i)
        else:
            suite.addTest(tests)

    _collect(discover())
    return suite


def makesuite_by_testlist(testlist_file):
    with open(testlist_file) as f:
        testlist = f.readlines()
    testlist = [i.strip() for i in testlist if not i.startswith("#")]
    suite = unittest.TestSuite()
    all_cases = collect()
    for case in all_cases:
        if case._testMethodName in testlist:
            suite.addTest(case)
    return suite


def run(suite):
    logging.info("="*30 + "测试开始" + "="*30)
    result = BeautifulReport(suite)
    result.report(filename='report_{}.html'.format(now), description='接口测试', report_dir=report_file,
                  theme='theme_cyan')
    count_num = result.testsRun
    fail_num = result.failure_count
    error_num = result.error_count
    pass_num = result.success_count
    rate = (pass_num/count_num)*100
    print(count_num, pass_num, fail_num, error_num, rate)

    # 收集失败用例
    if collect_failed_case and fail_num > 0:
        save_failures(result, failed_case_file)

    # 发送邮件
    if send_email_after_run:
        send_email(get_lastest_file(), count_num, pass_num, fail_num, error_num, rate)
    logging.info("="*30 + "测试结束" + "="*30)


def run_all():
    run(discover())


def run_suite(suite_name):
    # suite = get_suite(suite_name)
    if isinstance(suite_name, unittest.TestSuite):
        run(suite_name)
    else:
        print("TestSuite不存在")


def run_by_testlist():
    run(makesuite_by_testlist(testlist_file))


def rerun_fails():
    sys.path.append(test_case_path)
    with open(failed_case_file, 'rb') as f:
        suite = pickle.load(f)
    run(suite)


def main():
    if options.rerun_fails:
        rerun_fails()
    elif options.testlist:
        run(makesuite_by_testlist(testlist_file))
    elif options.testsuite:
        run_suite(options.testsuite)
    else:
        run_all()


if __name__ == '__main__':
    main()
