from automatic.config import config
from automatic.window import Window
from automatic.detector import Detector
from automatic.config import tasks
from time import sleep
import aircv as ac
from loguru import logger

class Executor:
    def __init__(self):
        self.window = Window()
        self.detector = Detector()

    def submit(self, task_name):
        task = tasks.get(task_name)
        phases = task["phases"]
        for phase in phases:
            phase_template = ac.imread(phase["template"])
            phase_action = phase["action"]
            phase_name = phase["name"]
            logger.info("任务阶段: {}".format(phase_name))
            iter = 0
            if phase_action == "click":
                while iter < 3:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(
                        full_window, phase_template)
                    if find:
                        self.window.click(relative_x,relative_y)
                        logger.info("点击完成")
                        break
                    else:
                        # 检查是否已经check
                        iter+=1
                        logger.info("action: click, 迭代次数: {}".format(iter))
                        sleep(0.5)
            elif phase_action == "check":
                while iter < 10:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(
                    full_window, phase_template)
                    if find:
                        logger.info("action: check, 检查完成")
                        break
                    else:
                        iter+=1
                        logger.info("action: check, 迭代次数: {}".format(iter))
                        sleep(0.3)
                if iter == 10:
                    raise RuntimeError("检查失败")
            
            elif phase_action == "finish":
                while True:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(
                        full_window, phase_template)
                    if find:
                        logger.info("action: finish, 执行完成")
                        break
