# coding=utf-8
import os
import time

from Performance.TestScript.launch_time import run_start_time
from Performance.CommonLib.comman import stop_atx
from Performance.TestScript.cpu_mem import run_cpu_mem
from Performance.TestScript.net_data_flow import run_network
from Performance.TestScript.power import run_power


def run(state):
    run_start_time(state, 5)
    time.sleep(5)
    run_cpu_mem(state, 3, 6)
    time.sleep(5)
    run_network(state, 30)
    time.sleep(5)
    run_power(state, 30)
    time.sleep(5)
    stop_atx()


# 执行各项性能测试的run方法
while True:
    try:
        run(state='debug')
        time.sleep(10)
    except Exception as e:
        print(e)
        print('重启设备')
        os.popen('adb reboot')
        time.sleep(180)
