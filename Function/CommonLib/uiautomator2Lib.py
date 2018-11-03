import subprocess
import sys

import requests
import uiautomator2 as u2

from AutoTest.FunctionTest.comFunction.adb import ADB


# uiautomator2操作类
class U2(ADB):
    # 初始化uiautomator2连接服务
    def init(self):
        global d
        try:
            d = u2.connect(self.get_device_id())
            # 解决出现坐标偏移问题
            d.jsonrpc.setConfigurator({"waitForIdleTimeout": 100})
        except OSError:
            sys.exit()
        except TypeError:
            device_name = input('请输入要使用的设备号：')
            d = u2.connect(device_name)
        except RuntimeError:
            print('设置waitForIdleTimeOut失败')
        # 启动uiautomator2守护程序
        while True:
            try:
                d.service('uiautomator').start()
                break
            except requests.exceptions.HTTPError:
                print('守护进程已启动')
                break
        return d

    # 停止uiautomator2服务
    def stop_uiautomator2(self):
        try:
            d.service('uiautomator').stop()
            print('守护进程已关闭')
        except Exception as e:
            print(e)

    # 亮屏
    def light(self):
        d.screen_on()

    # 切换uiautomator2专用输入法
    def change_ime(self):
        d.set_fastinput_ime(True)  # 切换成FastInputIME输入法

    # 恢复默认输入法
    def reset_ime(self):
        d.set_fastinput_ime(False)  # 切换成正常的输入法

    # 向输入框内输入内容
    def input_text(self, text):
        self.change_ime()
        d.clear_text()  # 清除输入框内的所有内容
        d(focused=True).set_text(text)  # 输入内容方式一
        # d.send_keys(text)             # 输入内容方式二
        self.reset_ime()

    # 检测此后一段时间内某元素是否出现
    def wait_element(self, control, t):
        if ':id/' in control:
            if d(resourceId=control).exists(t):
                return True
            else:
                return False
        else:
            if d(text=control).exists(t):
                return True
            else:
                return False

    # 点击控件
    def click_element(self, control, t):
        if ':id/' in control:
            d(resourceId=control).click(timeout=t)
        else:
            d(text=control).click(timeout=t)


if __name__ == '__main__':
    atx = U2()
    d = atx.init()
