
# -*-coding:UTF-8 -*-
import ctypes
import multiprocessing
import sys
import aircv as ac
from threading import Thread
from automatic.window import Window
from automatic.detector import Detector
from time import sleep
from loguru import logger
from automatic.config import tasks
logger.add("roco.log")


class Timer(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.start()

    def run(self):
        global dps
        while True:
            # logger.info(f'{dps} detects per second.')
            dps = 0
            sleep(1)


def main():
    global dps
    window = Window()
    detector = Detector()
    Timer()
    tasks_num = 0
    for task in tasks:
        logger.info("当前任务: {}".format(task["name"]))
        phases = task["phases"]
        for phase in phases:
            phase_template = ac.imread(phase["template"])
            phase_action = phase["action"]
            phase_name = phase["name"]
            logger.info("任务阶段：{}".format(phase_name))
            if phase_action == "click":
                while True:
                    full_window = window.screencap()
                    find, relative_x, relative_y = detector.find_location(
                        full_window, phase_template)
                    if find:
                        logger.info("找到了")
                        # window.click(relative_x,relative_y)
                    else:
                        # 检查是否已经check
                        logger.info("action: click, 未找到")
                    sleep(1)
            elif phase_action == "check":
                find, relative_x, relative_y = detector.find_location(
                    full_window, phase_template)

                if find:
                    logger.info("action_click, 已经点击")
            elif phase_action == "finish":
                sleep(2)
                find, relative_x, relative_y = detector.find_location(
                    full_window, phase_template)

                if find:
                    logger.info("当前任务完成！")
                    break
                else:
                    continue
                    phase_num = phase_num + 1
                    sleep(1)
                sleep(20)

    # while True:
    #     if tasks_num>= len(tasks):
    #         logger.info("所有任务都已经完成")
    #         break
    #     full_window = window.screencap()
    #     # cv2.imshow("main", screen)
    #     # cv2.imwrite("full_window.png", full_window)

    #     detector.find_location(full_window,template)
    #     sleep(20)

    #     dps += 1
    print("find!")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    if ctypes.windll.shell32.IsUserAnAdmin():
        dps = 0
        main()
    else:  # 自动以管理员身份重启
        ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, __file__, None, 1)
