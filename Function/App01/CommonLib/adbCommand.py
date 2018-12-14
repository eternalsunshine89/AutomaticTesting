# coding=utf-8
import os

from Function.App01.TestData.filePath import pkg_name


class ADB(object):
    """调用adb命令获取设备或者app的相关信息"""
    __adbCommand__ = {
        'adb devices': "检查USB连接的设备",
        'adb shell netcfg': "获取安卓手机已连接WiFi的ip地址",
        "adb shell pm dump 包名 | findstr 'u0a'": "根据app包名获取其uid号",
        "adb shell monkey -v -v -v 0": "根据app包名获取其启动入口类",
        "adb shell am start 包名/入口类名": "启动app",
        "adb shell input keyevent 4": "back",
        "adb shell input keyevent 3": "home",
        "adb shell am force-stop 包名": "强行停止app",
        "adb shell pm clear 包名": "清除app本地数据",
        "adb uninstall 包名": "卸载app",
        "adb shell getprop ro.build.version.release": "获取Android版本号",
        "adb shell pm dump 包名 | findstr 'versionName'": "获取app版本号",
    }

    def commands(self):
        for j, k in self.__adbCommand__.items():
            print(k + '——————>' + j)

    def get_device_id(self):
        texts = os.popen('adb devices').readlines()
        text = []
        for i in texts:
            if len(i) > 1:
                text.append(i)
        if len(text) == 1:
            print('未检测到已连接设备')
        elif len(text) == 2:
            device = text[1].split()[0]
            print('设备号：%s' % device)
            return device
        else:
            print('检测到已连接多台设备')
            device_list = []
            for i in list(range(1, len(text))):
                device_list.append(text[i].split()[0])
            print(device_list)
            return device_list

    def check_adb_connect(self):
        """查看USB连接状态"""
        text = os.popen('adb devices').readlines()
        if 'device' in text[1]:
            print('USB连接正常')
            return True
        else:
            print('USB未连接')
            return False

    # 获取安卓手机的ip地址
    def get_phone_ip(self):
        data = os.popen('adb shell netcfg').readlines()
        for i in data:
            if 'wlan0' in i:
                ip = i.split()[2].split('/')[0]
                print(ip)
                return ip

    def get_app_uid(self, pkg=pkg_name):
        """根据app包名获取其uid号"""
        content = os.popen('adb shell pm dump ' + pkg + ' | findstr "u0a"').read()
        uid = content.split()[-1].replace(':', '')
        print('%s的uid为：%s' % (pkg_name, uid))
        return uid

    def get_app_launch_activity(self, pkg=pkg_name):
        """根据app包名获取其启动入口类"""
        if pkg_name not in os.popen('adb shell pm list package').read():
            print('本机未安装该应用')
        else:
            activity = (x.split()[5] for x in os.popen('adb shell monkey -v -v -v 0').readlines() if pkg in x)
            launch_activity = pkg + '/' + activity.__next__()
            print('app启动入口:%s' % launch_activity)
            return launch_activity

    def app_start(self):
        """启动app"""
        os.popen('adb shell am start ' + self.get_app_launch_activity())

    def back(self):
        """back按键"""
        os.popen('adb shell input keyevent 4')

    def home(self):
        """home按键"""
        os.popen('adb shell input keyevent 3')

    def app_force_stop(self):
        """强行停止app"""
        os.popen('adb shell am force-stop ' + pkg_name)

    def app_data_clear(self):
        """清除app数据"""
        os.popen('adb shell pm clear ' + pkg_name)

    def uninstall_app(self):
        """卸载app"""
        os.popen('adb uninstall ' + pkg_name)

    def get_android_version(self):
        """获取设备的Android版本号"""
        version = os.popen('adb shell getprop ro.build.version.release').read().strip()
        print('安卓版本：%s' % version)
        return version

    def get_app_version(self):
        # 获取app的版本号
        version = os.popen(
            'adb shell pm dump ' + pkg_name + ' | findstr "versionName"').read().replace('versionName=', '').strip()
        print('app版本号：%s' % version)
        return version


if __name__ == '__main__':
    a = ADB()
    a.commands()
