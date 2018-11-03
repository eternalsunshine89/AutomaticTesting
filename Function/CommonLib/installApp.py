import os
import time
import uiautomator2

from AutoTest.FunctionTest.comFunction.adb import ADB
from AutoTest.FunctionTest.comFunction.uiautomator2Lib import U2
from AutoTest.FunctionTest.comFunction.fileOperation import Document
from AutoTest.FunctionTest.testData.filePath import Path, pkg_name


# 安装和卸载app
class AppManage(U2):
    def __init__(self, pkg_name, apk_path, phone='oppoR7'):
        self.pkg_name = pkg_name
        self.apk_path = apk_path
        self.phone = phone

    def uninstall_apk(self, pkg_name):
        """卸载本机已有双开助手apk"""
        try:
            os.popen('adb uninstall ' + pkg_name)
        except Exception:
            print('本机未安装%s' % pkg_name)

    # 非通用方法（自动安装仅支持oppoR7和允许静默安装应用的手机）
    def install_apk(self):
        doc = Document(self.apk_path)
        os.popen('adb install -r ' + doc.get_latest_file())
        self.light()
        if self.phone == 'oppoR7':
            while True:
                try:
                    if self.wait_element("com.android.packageinstaller:id/apk_info_view", 15):
                        self.click_element('继续安装', 10)
                        self.click_element('安装', 3)
                        self.click_element('完成', 3)
                        print('apk安装完成')
                        break
                    else:
                        continue
                except uiautomator2.UiObjectNotFoundError:
                    print('apk安装失败，正在尝试重新安装')
        else:
            if self.wait_element('确定', 5) is True:
                self.click_element('确定', 5)

    def install_control(self):
        self.uninstall_apk(self.pkg_name)
        time.sleep(2)
        self.install_apk()
        print('开始配置测试环境')

    # 监控指定目录下是否有待测包，有就安装，没有就继续检测
    def monitor(self):
        doc = Document(self.apk_path)
        while True:
            if doc.get_latest_file() is not None:
                print('检测到apk安装包')
                self.install_control()
                u2 = U2()
                u2.stop_uiautomator2()
                adb = ADB()
                # 获取app版本号
                app_version = adb.get_app_version()
                return app_version
            else:
                print('未检测到双开助手安装包\n本次检测时间：%s' % time.strftime('%Y.%m.%d_%H:%M:%S'))
                time.sleep(10)


if __name__ == '__main__':
    manage = AppManage(pkg_name, Path.path['apk_path'])
    manage.monitor()