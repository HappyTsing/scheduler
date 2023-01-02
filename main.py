
# -*-coding:UTF-8 -*-
import ctypes
import multiprocessing
import sys
import aircv as ac
from threading import Thread
from automatic.window import Window
from automatic.detector import Detector
from automatic.executor import Executor
from time import sleep
from loguru import logger
from automatic.config import tasks
logger.add("roco.log")

def main():
    executor = Executor()
    executor.submit("friend_manor_assistant")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
    else:  # 自动以管理员身份重启
        ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, __file__, None, 1)
