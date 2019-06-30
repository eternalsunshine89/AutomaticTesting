import os
import sys
import time
import urllib
from telnetlib import EC
from urllib.error import URLError
from Function.App01.TestData.filePath import launch_activity, pkg_name
from Function.App01.CommonLib.adbCommand import ADB
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException


# 对appium的api进行的二次封装
class Appium(ADB):
    # 初始化appium,获取手机屏幕尺寸
    def appium_init(self):
        global driver, window_size
        desired_cups = {}
        window_size = os.popen('adb shell wm size').read().split()[2]
        desired_cups['platformName'] = 'Android'
        desired_cups['platformVersion'] = self.get_android_version()
        desired_cups['deviceName'] = self.get_device_id()
        desired_cups['appPackage'] = pkg_name
        desired_cups['appActivity'] = launch_activity
        desired_cups['autoLaunch'] = 'false'
        desired_cups['noReset'] = 'true'
        desired_cups['automationName'] = 'uiautomator2'
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_cups)
        return driver

    # 结束当前会话（session）
    def quit(self):
        driver.quit()

    # 获取手机系统当前时间
    def device_time(self):
        return driver.device_time

    # 获取当前页面内容，以xml格式返回
    def page_source(self):
        return driver.page_source

    # 手机截图
    def screenshot(self, img_path):
        driver.get_screenshot_as_file(img_path)

    # 检测appium服务是否已开启，如未开启则自动开启服务并进行初始化，如已开启直接进行初始化
    def check_appium_server(self):
        adb = ADB()
        if adb.check_adb_connect() is True:
            if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
                while True:
                    try:
                        driver = self.appium_init()
                        print('appium初始化完成')
                        return driver
                    except ConnectionRefusedError:
                        time.sleep(3)
                    except urllib.error.URLError:
                        time.sleep(3)
            else:
                os.popen("start appium")
                print("正在启动appium服务程序，请稍等...")
                while True:
                    if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
                        while True:
                            try:
                                d = self.appium_init()
                                print('appium初始化完成')
                                return d
                            except ConnectionRefusedError:
                                time.sleep(3)
                            except URLError:
                                time.sleep(3)
                    else:
                        time.sleep(1)
        else:
            sys.exit()

    # 结束appium进程（适用Windows）
    def stop_appium_server(self):
        driver.quit()
        pid_node = os.popen('tasklist | findstr "node.exe"').readlines()
        for i in pid_node:
            os.popen('taskkill /f /pid ' + i.split()[1])
        pid_cmd = os.popen('tasklist | findstr "cmd.exe"').readlines()
        for i in pid_cmd:
            os.popen('taskkill /f /pid ' + i.split()[1])
        print('appium服务已关闭')

    # 定位名称唯一的控件，返回该控件对象
    def find_element(self, control):
        if "//" in control:
            return driver.find_element_by_xpath(control)
        elif ":id/" in control:
            return driver.find_element_by_id(control)
        else:
            try:
                return driver.find_element_by_class_name(control)
            except Exception:
                print("不支持的控件名")

    # 定位多个同名控件，返回控件对象列表
    def find_elements(self, control):
        if "//" in control:
            return driver.find_elements_by_xpath(control)
        elif ":id/" in control:
            return driver.find_elements_by_id(control)
        else:
            try:
                return driver.find_elements_by_class_name(control)
            except Exception:
                print("不支持的控件名")

    # uiautomator定位方式，定位唯一控件，返回该控件对象
    def find_element2(self, control):
        if ":id/" in control:
            return driver.find_element_by_android_uiautomator("new UiSelector().resouceId(control)")
        elif "//" in control:
            return driver.find_element_by_android_uiautomator("new Uiselector().xpath(control)")
        else:
            print("不支持的控件名")

    # uiautomator定位方式，定位多个同名控件，返回控件对象列表
    def find_elements2(self, control):
        if ":id/" in control:
            return driver.find_elements_by_android_uiautomator("new UiSelector().resouceId(control)")
        elif "//" in control:
            return driver.find_elements_by_android_uiautomator("new Uiselector().xpath(control)")
        else:
            print("不支持的控件名")

    # 显式等待元素出现（直到until方法执行完毕，或者等待10秒后等待取消）
    def wait_for_element(self, control, t=10, frequency=1):
        try:
            WebDriverWait(driver, t, frequency).until(self.find_element(control))
        except selenium.common.exceptions.WebDriverException:
            try:
                WebDriverWait(driver, t, frequency).until(self.find_element2(control))
            except selenium.common.exceptions.WebDriverException:
                print('等待元素%s出错' % control)

    # 控件操作："长按"
    def long_press(self, control, t=1000):
        touch = TouchAction(driver)
        touch.long_press(control).wait(t).release().perform()

    # 控件操作："长按 + 拖动"
    def drag_and_drop(self, control1, control2):
        touch = TouchAction(driver)
        touch.long_press(control1).wait(1000).move_to(control2).wait(1000).release().perform()

    # 控件操作："滑动"
    def swipe(self, direction, duration=200):
        # window_size = os.popen('adb shell wm size').read().split()[2]
        width = int(window_size.split('x')[0])
        height = int(window_size.split('x')[1])
        center_x = int(width / 2)
        center_y = int(height / 2)
        up = int(0.9 * height)
        down = int(0.1 * height)
        left = int(0.1 * width)
        right = int(0.9 * width)
        if direction == "u":
            driver.swipe(center_x, center_y, center_x, up, duration=duration)
        elif direction == "d":
            driver.swipe(center_x, center_y, center_x, down, duration=duration)
        elif direction == "l":
            driver.swipe(center_x, center_y, left, center_y, duration=duration)
        elif direction == "r":
            driver.swipe(center_x, center_y, right, center_y, duration=duration)
        else:
            print('参数输入有误')

    # 滑动查找控件
    def swipe_to_find_element(self, control, direction='U'):
        count = 0
        while True:
            try:
                self.find_element(control).click()
                break
            except Exception:
                count += 1
                if count == 5:
                    print('控件未找到')
                else:
                    self.swipe(direction)
                    time.sleep(1)

    # 显式等待元素出现（直到until方法执行完毕，或者等待10秒后等待取消）
    def wait_element(self, control, t=10, frequency=1):
        WebDriverWait(driver, t, frequency).until(self.find_element(control))

    # 显式等待activity出现（直到until方法执行完毕，或者等待10秒后等待取消）
    def wait_activity(self, activity, t=10, frequency=1):
        driver.wait_activity(activity, t, frequency)

    # 查找指定内容的toast并返回布尔类型结果
    def toast(self, message):
        toast = '//*[@text="%s"]' % message
        try:
            WebDriverWait(driver, 5, 0.1).until(EC.presence_of_element_located((By.XPATH, toast)))
            return True
        except Exception:
            return False

    # 系统弹窗处理
    def system_alert(self):
        """监控并处理系统弹窗"""
        global system_alert_flag
        system_alert_flag = True
        key_word = ['允许', '始终允许', '确定', '忽略', '以后再说', '同意并继续', '不再提醒']
        while system_alert_flag:
            try:
                data = os.popen('adb shell dumpsys window|find "permission"').read()
                if "SYSTEM_ALERT_WINDOW" in data:
                    for i in key_word:
                        if i in driver.page_source:
                            try:
                                driver.find_element_by_xpath('//*[@text="%s"]' % i).click()
                            except Exception as e:
                                print(e)
                elif "mFocusedApp" in data:
                    for i in key_word:
                        if i in driver.page_source:
                            try:
                                driver.find_element_by_xpath('//*[@text="%s"]' % i).click()
                            except Exception as e:
                                print(e)
            except Exception as e:
                print(e)
        else:
            print('system_alert is stopped')

    # app弹窗处理
    def app_alert(self):
        """监控并处理应用安装弹窗"""
        global app_alert_flag
        app_alert_flag = True
        while app_alert_flag:
            try:
                data = driver.page_source
                if "com.android.packageinstaller:id/apk_info_view" in data:
                    print('检测到apk安装提示，开始处理...')
                    try:
                        driver.find_element_by_id('com.android.packageinstaller:id/btn_continue_install').click()
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@text="安装"]').click()
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@text="完成"]').click()
                        print('apk安装完成')
                    except selenium.common.exceptions.NoSuchElementException:
                        driver.find_element_by_xpath('//*[@text="继续安装"]').click()
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@text="安装"]').click()
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@text="完成"]').click()
                        print('apk安装完成2')
            except Exception as e:
                print(e)
        else:
            print('app_alert is stopped')

    def stop_monitor(self):
        global system_alert_flag, app_alert_flag
        system_alert_flag = False
        app_alert_flag = False


if __name__ == '__main__':
    a = Appium()
    a.check_appium_server()
