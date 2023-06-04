
# -*-coding:UTF-8 -*-
from multiprocessing import freeze_support
from ctypes import windll
from sys import executable
from automatic.executor import Executor
from loguru import logger
from os import path,system
from sys import argv
from datetime import datetime
from math import floor
import traceback
from automatic.utils import *
from time import sleep
CUR_PATH = path.dirname(path.realpath(argv[0]))
LOG_PATH = path.join(CUR_PATH,"scheduler.log")
logger.add(LOG_PATH)

def main():

    start = datetime.now()
    executor = Executor()
    print_hello()
    # todo 改为支持多个任务同时执行,或可选任务
    task = get_config()
    try:
        executor.submit(task["seer"])
    except Exception as e:
        sleep(5)
        traceback.print_exc()
        logger.error(e)
    end = datetime.now()
    total = (end-start).seconds
    minute = floor(total / 60)
    second = total % 60
    logger.info("共计用时: {} 分 {} 秒.".format(minute,second))
    system('pause')

if __name__ == '__main__':
    freeze_support()
    if windll.shell32.IsUserAnAdmin():
        main()
    else:  # 自动以管理员身份重启
        windll.shell32.ShellExecuteW(
            None, 'runas', executable, __file__, None, 1)
