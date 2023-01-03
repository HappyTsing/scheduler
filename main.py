
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
    # tasks = ["brave_train_hall"]
    # tasks = ["dark_far_force"]
    # tasks = ["paradise_adventure"]
    # tasks = ["dark_city_everyday"]
    # tasks = ["fetch_assistant"]
    # tasks = ["friend_manor_assistant"]
    # executor.submit("fetch_assistant")
    # executor.test()
    
    for task in task_name_list:
        executor.submit(task)
        logger.info("============================")


if __name__ == '__main__':
    freeze_support()
    if windll.shell32.IsUserAnAdmin():
        main()
    else:  # 自动以管理员身份重启
        windll.shell32.ShellExecuteW(
            None, 'runas', executable, __file__, None, 1)
