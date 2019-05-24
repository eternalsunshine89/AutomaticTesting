# coding=utf-8
import time
import unittest

from Function.App01.CommonLib.AppiumPackage import Appium
from Function.App01.CommonLib.computerInfo import ComputerInfo
from Function.App01.TestData.elements import Elements
from Function.App01.CommonLib.log import Log
from Function.App01.TestData.filePath import Path


# 用户登录测试
class Login(unittest.TestCase, Appium, Log, Elements, ComputerInfo):

    def setUp(self):
        print("用例开始时间:", self.get_time())
        time.sleep(1)

    def tearDown(self):
        print("用例结束时间:", self.get_time())
        time.sleep(1)

    def test_01(self):
        """正确的账号，正确的密码"""
        log = self.start_log(Path.path['log_path'])
        self.skimover_welpage()
        time.sleep(1)
        self.find_element(self.addGuidePage['跳过']).click()
        self.stop_log(log)

    def test_02(self):
        """正确的账号，错误的密码"""
        pass

    def test_03(self):
        """错误的账号，正确的密码"""
        pass

    def test_04(self):
        """错误的账号，错误的密码"""
        pass


if __name__ == '__main__':
    unittest.main()
