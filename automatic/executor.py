from automatic.config import config
from automatic.window import Window
from automatic.detector import Detector
from automatic.config import tasks
from time import sleep
from aircv import imread
from cv2 import imwrite
from loguru import logger

class Executor:
    def __init__(self):
        self.window = Window()
        self.detector = Detector()
    def test(self):
        while True:
            full_window = self.window.screencap()
            template = imread("c:\\Users\\leki\\Desktop\\roco-master\\automatic\\img\\tasks\\friend_manor_assistant\\4.png")
            self.detector.find_location(full_window,template)
            sleep(0.3)
    def submit(self, task_name):
        task = tasks.get(task_name)
        phases = task["phases"]
        logger.info(phases)
        for phase in phases:
            phase_action = phase["action"]
            phase_name = phase["name"]
            if(phase.get("template") != None):
                phase_template = imread(phase.get("template"))
            logger.info("任务阶段: {}".format(phase_name))
            iter = 0
            if phase_action == "click":
                while iter < 3:
                    full_window = self.window.screencap()
                    # imwrite(str(iter)+".png",full_window)
                    find, relative_x, relative_y = self.detector.find_location(
                        full_window, phase_template)
                    if find:
                        phase_times = phase["times"]
                        self.window.click(relative_x,relative_y,phase_times)
                        logger.info("点击完成")
                        break
                    else:
                        # 检查是否已经check
                        iter+=1
                        logger.info("action: click, 迭代次数: {}".format(iter))
                        sleep(0.5)
                        
            elif phase_action == "doubleClick":
                while iter < 3:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(
                        full_window, phase_template)
                    if find:
                        self.window.doubleClick(relative_x,relative_y)
                        logger.info("双击完成")
                        break
                    else:
                        # 检查是否已经check
                        iter+=1
                        logger.info("action: click, 迭代次数: {}".format(iter))
                        sleep(0.5)            
                        
            elif phase_action == "press":
                phase_key = phase["key"]
                phase_times = phase["times"]
                self.window.press(phase_key,phase_times)
                logger.info("按下按键{}成功".format(phase_key))
                
                        
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
                    logger.error("检查失败")
                    raise RuntimeError("检查失败")
            
            
            elif phase_action == "finish":
                while True:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(
                        full_window, phase_template)
                    if find:
                        # imwrite(str(iter)+".png",full_window)
                        logger.info("action: finish, 执行完成")
                        break
                    sleep(0.3)
                    
