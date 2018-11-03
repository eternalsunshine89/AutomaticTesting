# coding=utf-8
import os
import time
import winreg


class ComputerInfo(object):

    # 获取系统当前时间
    def get_time(self):
        return time.strftime('%Y%m%d%H%M%S')

    # 获取电脑ip地址
    def get_pc_ip(self):
        for i in os.popen('ipconfig').readlines():
            if 'IPv4' in i:
                print('电脑ip地址：%s' % i.split()[-1])
                return i.split()[-1]

    # 获取系统桌面路径
    def get_desktop_path(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        print('电脑桌面路径：%s' % winreg.QueryValueEx(key, "Desktop")[0])
        return winreg.QueryValueEx(key, "Desktop")[0]


if __name__ == '__main__':
    a = ComputerInfo()
    a.get_pc_ip()
    a.get_desktop_path()