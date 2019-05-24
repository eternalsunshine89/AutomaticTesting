import time
import unittest

from Function.App01.CommonLib.AppiumPackage import Appium
from Function.App01.CommonLib.computerInfo import ComputerInfo
from Function.App01.CommonLib.log import Log
from Function.App01.TestData.elements import Elements
from Function.App01.TestData.filePath import Path


class AddApp(unittest.TestCase, Appium, Log, Elements, ComputerInfo):

    def setUp(self):
        print("用例开始时间:", self.get_time())

    def tearDown(self):
        print("用例结束时间:", self.get_time())

    def test_01(self):
        """正确的账号，正确的密码"""
        # 开启log
        log = self.start_log(Path.path['log_path'])
        self.app_data_clear()
        time.sleep(1)
        self.skimover_welpage()
        time.sleep(1)
        self.find_element(self.addGuidePage['跳过']).click()
        # 停止log
        self.stop_log(log)
