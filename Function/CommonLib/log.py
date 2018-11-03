# coding=utf-8
import os
import time

from AutoTest.FunctionTest.comFunction.computerInfo import ComputerInfo


# 获取安卓手机的运行日志,可同时抓取多个log
from AutoTest.FunctionTest.testData.filePath import Path


class Log(ComputerInfo):

    def start_log(self, log_path):
        adb_list_old = []
        adb_list_new = []
        for i in os.popen('tasklist|findstr "adb.exe"').readlines():
            adb_list_old.append(i.split()[1])
        print(adb_list_old)
        os.popen('adb logcat -c && adb logcat -v  time > ' + log_path + '\%s.txt' % self.get_time())
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


class Analyse(ComputerInfo):
    def __init__(self, log_path, anr_path, crash_path):
        self.log_path = log_path
        self.anr_path = anr_path
        self.crash_path = crash_path

    def catch_anr_and_crash(self):
        for i in os.listdir(os.path.join(self.log_path)):
            if i.endswith('txt'):
                with open(os.path.join(self.log_path, i), 'rb') as f:
                    for j in f.readlines():
                        if b'anr' in j:
                            with open(os.path.join(self.anr_path, 'anr.txt'), 'a') as f1:
                                f1.write(str(j) + '\n')
                        elif b'CrashHandler' in j:
                            with open(os.path.join(self.crash_path, 'crash.txt'), 'a') as f2:
                                f2.write(str(j) + '\n')


if __name__ == '__main__':
    a = Log()
    b = Log()
    l1 = a.start_log(Path.path['log_path'])
    time.sleep(3)
    a.stop_log(l1)
    l2 = b.start_log(Path.path['log_path'])
    time.sleep(3)
    b.stop_log(l2)