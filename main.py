
# -*-coding:UTF-8 -*-
from multiprocessing import freeze_support
from ctypes import windll
from sys import executable
from automatic.executor import Executor
from loguru import logger
from automatic.config import task_name_list
logger.add("roco.log")

def main():
    executor = Executor()
    
    for task in task_name_list:
        executor.submit(task)
        logger.info("=============================== next task ===============================")


if __name__ == '__main__':
    freeze_support()
    if windll.shell32.IsUserAnAdmin():
        main()
    else:  # 自动以管理员身份重启
        windll.shell32.ShellExecuteW(
            None, 'runas', executable, __file__, None, 1)
