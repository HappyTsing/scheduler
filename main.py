
# -*-coding:UTF-8 -*-
from multiprocessing import freeze_support
from ctypes import windll
from sys import executable
from automatic.executor import Executor
from loguru import logger
from automatic.config import task_name_list
from os import path,system
from sys import argv
from tqdm import tqdm
from datetime import datetime
from math import floor
CUR_PATH = path.dirname(path.realpath(argv[0]))
LOG_PATH = path.join(CUR_PATH,"roco.log")
logger.add(LOG_PATH)

def main():
    print("""
 _______ .__   __.        __    ______   ____    ____
|   ____||  \ |  |       |  |  /  __  \  \   \  /   /
|  |__   |   \|  |       |  | |  |  |  |  \   \/   /
|   __|  |  . `  | .--.  |  | |  |  |  |   \_    _/
|  |____ |  |\   | |  `--'  | |  `--'  |     |  |
|_______||__| \__|  \______/   \______/      |__|""")
    start = datetime.now()
    executor = Executor()
    with tqdm(total=len(task_name_list)) as pbar:
        pbar.set_description("任务进度")
        for task in task_name_list:
            executor.submit(task)
            pbar.update(1)
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
