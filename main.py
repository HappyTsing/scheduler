
# -*-coding:UTF-8 -*-
from multiprocessing import freeze_support
from ctypes import windll
from sys import executable
from automatic.scheduler import Scheduler
from loguru import logger
from os import path,system
from sys import argv
from datetime import datetime
from math import floor
import traceback
from automatic.utils import *
from time import sleep
from automatic.utils import print_hello
CUR_PATH = path.dirname(path.realpath(argv[0]))
LOG_PATH = path.join(CUR_PATH,"scheduler.log")
logger.add(LOG_PATH)

def main():
    print_hello()
    try:
        schedule = Scheduler()
        schedule.start()
    except Exception as e:
        logger.error(f"{e} | scheduler will exit after 1 min...")
        sleep(60)       

if __name__ == '__main__':
    freeze_support()
    # Mac 电脑以管理员启动，否则无法点击
    if windll.shell32.IsUserAnAdmin():
        main()
    else:  # 自动以管理员身份重启
        windll.shell32.ShellExecuteW(
            None, 'runas', executable, __file__, None, 1)
