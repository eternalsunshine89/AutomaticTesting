# coding=utf-8
import os
import sys
import threading
import time

import uiautomator2
import uiautomator2 as u2

from myFuncLib.adb import ADB


pkg_name = 'com.excelliance.dualaid'
activity = 'com.excelliance.kxqp.ui.HelloActivity'
# QQ_user = input('请输入测试用QQ号：')
# QQ_key = input('请输入QQ密码：')
QQ_user = "1037287177"
QQ_key = "wangchangQQ227x"


# 获取安卓手机的运行日志
class Log(object):
    def start_log(self, log_path):
        adb_list_old = []
        adb_list_new = []
        for i in os.popen('tasklist|findstr "adb.exe"').readlines():
            adb_list_old.append(i.split()[1])
            print(adb_list_old)
        os.popen('adb logcat -v time > ' + log_path)
        time.sleep(1)
        for j in os.popen('tasklist | findstr "adb.exe"').readlines():
            adb_list_new.append(j.split()[1])
            print(adb_list_new)
        for log_pid in adb_list_new:
            if log_pid not in adb_list_old:
                print(log_pid)
                return log_pid

    def stop_log(self, log_pid):
        os.popen('taskkill /f /pid %s' % log_pid)


# 启动和停止线程
class NewThread(object):

    def start_thread(self, func, args=()):
        global thread_flag
        thread_flag = 1
        thread = threading.Thread(target=func, args=args)
        thread.start()

    def stop_thread(self):
        global thread_flag
        thread_flag = 0


# uiautomator2操作类
class U2(object):
    # 停止uiautomator2服务
    def stop_uiautomator2(self):
        try:
            d.service('uiautomator').stop()
        except Exception as e:
            print(e)

    # 向输入框内输入内容
    def input_text(self, text):
        d.set_fastinput_ime(True)     # 切换成FastInputIME输入法
        d.clear_text()                # 清除输入框内的所有内容(Require android-uiautomator.apk version >= path.0.7)
        d(focused=True).set_text(text)  # 输入内容
        # d.send_keys(text)             # 输入内容
        d.set_fastinput_ime(False)    # 切换成正常的输入法

    # 登录本机QQ
    def local_QQ_login(self, user, key):
        d.press('home')
        d.app_clear('com.tencent.mobileqq')
        time.sleep(2)
        d.app_start('com.tencent.mobileqq')
        d(resourceId="com.tencent.mobileqq:id/btn_login").click(timeout=25)
        d(text='QQ号/手机号/邮箱').click(timeout=5)
        self.input_text(user)
        d(resourceId="com.tencent.mobileqq:id/password").click(timeout=5)
        self.input_text(key)
        d(resourceId="com.tencent.mobileqq:id/login").click(timeout=10)
        time.sleep(10)
        while True:
            if not d(text='联系人').exists(5):
                d.press('back')
            else:
                break

    def multi_QQ_login(self, user, key):
        d.app_stop('com.excelliance.dualaid')
        time.sleep(2)
        d.app_start('com.excelliance.dualaid')
        try:
            if d(resourceId="com.excelliance.dualaid:id/add_but").exists(8):
                if d(text='QQ').exists():
                    d(text='QQ').long_click()
                    if d(text=u"删除应用").exists(3):
                        d(text=u"删除应用").click(timeout=5)
                        d(resourceId="com.excelliance.dualaid:id/tv_left").click(timeout=5)
                    else:
                        d(resourceId="com.excelliance.dualaid:id/delete_item").click_exists(5)
                    d(resourceId="com.excelliance.dualaid:id/add_but").click(timeout=5)
                    d(text='QQ').click(timeout=5)
                    time.sleep(5)
                else:
                    d(resourceId="com.excelliance.dualaid:id/add_but").click(timeout=5)
                    d(text='QQ').click(timeout=5)
                    time.sleep(5)
            d(text='QQ').click(timeout=5)
        except Exception as e:
            print(e)
        try:
            if d(resourceId="com.excelliance.dualaid:id/bt_vanish").exists(5):
                d(resourceId="com.excelliance.dualaid:id/bt_vanish").click(timeout=5)
        except Exception as e:
            print(e)
        try:
            d(resourceId="com.tencent.mobileqq:id/btn_login").click(timeout=30)
        except uiautomator2.UiObjectNotFoundError:
            d(resourceId="com.tencent.mobileqq:id/btn_login").click(timeout=15)
        except Exception as e:
            print(e)
            time.sleep(3)
            self.multi_QQ_login(user, key)
        d(text='QQ号/手机号/邮箱').click(timeout=5)
        self.input_text(user)
        d(resourceId="com.tencent.mobileqq:id/password").click(timeout=5)
        self.input_text(key)
        d(resourceId="com.tencent.mobileqq:id/login").click(timeout=10)
        time.sleep(10)
        while True:
            if not d(text='联系人').exists(5):
                d.press('back')
            else:
                break


# 安卓设备相关操作
class PhoneSetting(object):
    # 设置手机（oppoR7/honor9）系统时间
    def set_phone_time(phone='oppoR7', kind='normal'):
        while True:
            if phone == 'oppoR7':
                try:
                    if kind == 'normal':
                        print('正在设置手机时间')
                        d.app_stop(pkg_name)
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d(text='设置').click()
                        time.sleep(1)
                        d(scrollable=True).fling()
                        time.sleep(2)
                        d(text='日期和时间').click(timeout=5)
                        time.sleep(1)
                        if d(text='设置日期').info['enabled'] is False:
                            d(resourceId='android:id/checkbox')[0].click(timeout=5)
                            time.sleep(1)
                            d(text='设置日期').click(timeout=5)
                            time.sleep(1)
                            d(resourceId='oppo:id/increment')[1].click(timeout=5)
                            time.sleep(1)
                            d(resourceId='android:id/button1').click(timeout=5)
                            time.sleep(1)
                        else:
                            d(text='设置日期').click(timeout=5)
                            time.sleep(1)
                            d(resourceId='oppo:id/increment')[1].click(timeout=5)
                            time.sleep(1)
                            d(resourceId='android:id/button1').click(timeout=5)
                            time.sleep(1)
                        d.press('home')
                        time.sleep(2)
                        d.app_start(pkg_name)
                        d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                        d.press('back')
                        time.sleep(2)
                        break
                    elif kind == 'recovery':
                        print('正在恢复手机时间')
                        d.press('home')
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d(text='设置').click(timeout=5)
                        time.sleep(1)
                        d(scrollable=True).fling()
                        time.sleep(2)
                        d(text='日期和时间').click(timeout=5)
                        time.sleep(1)
                        if d(text='设置日期').info['enabled'] is True:
                            time.sleep(1)
                            d(resourceId='android:id/checkbox')[0].click(timeout=5)
                            time.sleep(1)
                            d.press('home')
                            time.sleep(2)
                            print('手机时间已恢复至当前时间')
                            break
                        else:
                            d.press('home')
                            time.sleep(2)
                            print('手机时间已经为当前时间')
                            break
                except uiautomator2.UiObjectNotFoundError:
                    continue


# 双开助手相关操作
class MutipleApp(object):

    def set_app_state(self):
        setting = PhoneSetting()
        """首次启动双开助手至调出banner，icon"""
        d.app_clear(pkg_name)
        time.sleep(2)
        d.app_start(pkg_name)
        while True:
            if d(text=u'点击加号，添加双开应用').exists(5):
                d(scrollable=True).fling.horiz.forward(100)
                d(scrollable=True).fling.horiz.forward(100)
                d(text='开始体验').click_exists(8)
                d(text='跳过').click_exists(8)
                break
            else:
                d.screenshot(r'C:\Users\BAIWAN\Desktop\error%s.png' % time.strftime('%H%M%S'))
                d.app_stop(pkg_name)
                time.sleep(2)
                d.app_start(pkg_name)
        d(resourceId='com.excelliance.dualaid:id/tv_bt_add').exists(10)
        d.press('back')
        if d(resourceId='com.excelliance.dualaid:id/iv_close').exists(5):
            d(resourceId='com.excelliance.dualaid:id/iv_close').click(timeout=5)
            print('关闭banner上部提示成功')
        time.sleep(2)
        d.press('back')
        time.sleep(2)
        d.app_start(pkg_name)
        time.sleep(2)
        d.press('back')
        time.sleep(3)
        d.app_start(pkg_name)
        # 检测非标位
        # print('正在检测非标位')
        # if d(resourceId='com.excelliance.dualaid:id/fl_off_standard_position').exists(10) is True:
        #     print('带非标位版本')
        i = 1
        while i <= 10:
            try:
                if not d(resourceId="com.excelliance.dualaid:id/iv_ad_alimama").exists(3) and not d(
                        resourceId="com.excelliance.dualaid:id/ad_but").exists(3):
                    print("广告拉取失败%d次" % i)
                    if i == 3:
                        print('尝试设置手机时间后拉取')
                        setting.set_phone_time()
                        if d(resourceId="com.excelliance.dualaid:id/iv_ad_alimama").exists(3) or d(
                                resourceId="com.excelliance.dualaid:id/ad_but").exists(3):
                            print('广告拉取成功')
                            break
                    elif i == 5:
                        print('尝试恢复手机时间后拉取')
                        setting.set_phone_time('recovery')
                        if d(resourceId="com.excelliance.dualaid:id/iv_ad_alimama").exists(3) or d(
                                resourceId="com.excelliance.dualaid:id/ad_but").exists(3):
                            print('广告拉取成功')
                            break
                    elif i == 10:
                        print('测试失败，未配置广告或广告展示部分可能有问题')
                        sys.exit()
                    else:
                        d.press('back')
                        time.sleep(2)
                        d.app_start(pkg_name)
                else:
                    print('广告拉取成功')
                    break
            except Exception as e:
                print(e)
                continue
            i += 1


# 初始化uiautomator2连接服务
def atx_init():
    global d
    adb = ADB()
    try:
        d = u2.connect(adb.get_device_id())
        return d
    except TypeError:
        device_name = input('请输入要使用的设备号：')
        d = u2.connect(device_name)
        return d


def stop_atx():
    d.service("uiautomator").stop()


if __name__ == '__main__':
    a = U2()
    atx_init()
    a.multi_QQ_login(QQ_user, QQ_key)
    stop_atx()