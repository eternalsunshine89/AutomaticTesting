# coding=utf-8
import os
import time

from AutoTest.myFuncLib.adb import ADB
from AutoTest.myFuncLib.email import SendEmail
from AutoTest.performancetest.comman import atx_init, pkg_name, QQ_user, QQ_key, U2


# 测试
class BatteryTest(object):

    # 清空手机耗电记录
    def reset_batteryinfo(self):
        os.popen('adb shell dumpsys batterystats --reset')

    # 检查usb连接状态
    def check_usb_status(self):
        data = os.popen('adb shell dumpsys battery').readlines()
        for i in data:
            if 'USB powered' in i:
                # print(i.split()[bad_path])
                return i.split()[2]

    # 设置usb连接为连接不充电状态
    def set_usb_status(self):
        os.popen('adb shell dumpsys battery set usb 0')
        if self.check_usb_status() != 'false':
            print('设置usb不充电状态失败')

    # 恢复手机默认usb连接状态
    def reset_usb_status(self):
        os.popen('adb shell dumpsys battery reset')
        if self.check_usb_status() != 'true':
            print('恢复usb充电状态失败')

    # 获取设置usb连接状态和恢复usb默认连接状态期间的应用耗电量数据
    def get_batteryinfo(self, pkg=pkg_name):
        adb = ADB()
        uid = adb.get_app_uid(pkg)
        content = os.popen('adb shell dumpsys batterystats|findstr "Uid"|findstr ' + uid).readlines()
        # android8.0
        # batteryinfo = (str(re.findall('(?<=[(])[^()]+\.[^()]+(?=[)])', content)).replace('[', '')).replace(']', '')
        for i in content[:int(len(content) / 2)]:
            batteryinfo = i.replace('Uid ' + uid + ': ', '').strip()
            print('消耗电量%0.2f' % float(batteryinfo))
            return round(float(batteryinfo), 2)


# 测试用例（场景设计）
class TestCase(BatteryTest):
    def __init__(self, ti):
        self.ti = ti
        os.popen('adb shell dumpsys batterystats --enable full-wake-history')

    # 场景一：不添加应用挂后台5分钟(调出广告和信息流)
    def test01(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(1)
            d.app_start(pkg_name)
            try:
                if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
                    break
            except Exception as e:
                print(e)
        try:
            if d(text='QQ').exists(3):
                d(text='QQ').long_click()
                d(text=u"删除应用").click(timeout=5)
                d(resourceId="com.excelliance.dualaid:id/tv_left").click(timeout=5)
        except Exception as e:
            print(e)
        self.reset_batteryinfo()
        self.set_usb_status()
        d.press('home')
        time.sleep(self.ti)
        self.reset_usb_status()
        return self.get_batteryinfo(pkg_name)

    # 场景二：不添加应用停留主界面5分钟(调出广告和信息流)
    def test02(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            try:
                if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
                    break
            except Exception as e:
                print(e)
        self.reset_batteryinfo()
        self.set_usb_status()
        time.sleep(self.ti)
        self.reset_usb_status()
        return self.get_batteryinfo(pkg_name)

    # 场景三：双开内浏览信息流5分钟
    def test03(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            try:
                if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
                    break
            except Exception as e:
                print(e)
        self.reset_batteryinfo()
        self.set_usb_status()
        now = time.time()
        while True:
            d(scrollable=True).fling.vert.forward()
            time.sleep(5)
            if time.time() - now >= self.ti:
                break
        self.reset_usb_status()
        return self.get_batteryinfo(pkg_name)

    # 场景四：对比本机和双开QQ登录并置于后台5分钟的功耗(调出广告和信息流)
    def test04(self):
        u2 = U2()
        # 本机QQ功耗
        d.app_clear('com.tencent.mobileqq')
        u2.local_QQ_login(QQ_user, QQ_key)
        self.reset_batteryinfo()
        self.set_usb_status()
        d.press('home')
        time.sleep(self.ti)
        self.reset_usb_status()
        power1 = self.get_batteryinfo('com.tencent.mobileqq')
        d.app_clear('com.tencent.mobileqq')
        # 双开QQ功耗
        d.app_stop('com.tencent.mobileqq')
        u2.multi_QQ_login(QQ_user, QQ_key)
        self.reset_batteryinfo()
        self.set_usb_status()
        d.press('home')
        time.sleep(self.ti)
        self.reset_usb_status()
        power2 = self.get_batteryinfo(pkg_name)
        return power2 - power1

    # 场景五：
    def test05(self):
        return 0


def run_power(state, t=300):
    global d
    d = atx_init()
    test = TestCase(t)
    e = SendEmail('wangzhongchang@excelliance.cn', 'wzc6851498', state)
    mail_content = """
            <html>
            <body>
            <div>
                <h2>双开助手性能测试：功耗测试</h2>
                <p>场景一：不添加应用挂后台5分钟</p>
                <p>场景二：不添加应用停留主界面5分钟</p>
                <p>场景三：双开内浏览信息流5分钟</p>
                <p>场景四：对比本机和双开QQ登录并置于后台5分钟的功耗(双开-本机)</p>
                <div id="content">
                    <table border="path" bordercolor="#87ceeb" width="300">
                        <tr>
                            <td><strong>测试场景</strong></td>
                            <td><strong>耗电量(mAh)</strong></td>
                        </tr>
                        <tr>
                            <td>场景一</td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>场景二</td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>场景三</td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>场景四</td>
                            <td>%s</td>
                        </tr>
                    </table>
                </div>
            </div>
            </body>
            </html>
    """ % (test.test01(), test.test02(), test.test03(), test.test04())
    e.create_email(mail_content)
    os.popen('adb shell dumpsys batterystats --disable full-wake-history')
    print('功耗模块测试结束，性能测试完成')


if __name__ == '__main__':
    run_power(state='debug', t=20)
