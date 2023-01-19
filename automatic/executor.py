from automatic.window import Window
from automatic.detector import Detector
from automatic.config import tasks
from automatic.slots import seven_lights_holy_land,diamond_mission
from time import sleep
from aircv import imread
# from cv2 import imwrite
from loguru import logger
from datetime import datetime
class Executor:
    def __init__(self):
        self.window = Window()
        self.detector = Detector()
        
    # def test(self):
    #     while True:
    #         full_window = self.window.screencap()
    #         template = imread("c:\\Users\\leki\\Desktop\\roco-master\\automatic\\img\\tasks\\friend_manor_assistant\\4.png")
    #         self.detector.find_location(full_window,template)
    #         sleep(0.3)
    
    def submit(self, task_name):
        task = tasks.get(task_name)
        task_name = task["name"]
        logger.info("当前任务: {}".format(task_name))
        phases = task["phases"]
        for phase in phases:
            phase_action = phase["action"]
            phase_name = phase["name"]
            if(phase.get("template") != None):
                phase_template = imread(phase.get("template"))
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
                        logger.success("[{} - {}] click success".format(task_name, phase_name))
                        break
                    else:
                        # 检查是否已经check
                        iter+=1
                        # logger.info(" [{} - {}] click failed: not found, try {} times.".format(task_name, phase_name, iter))
                        sleep(0.5)
                if iter == 3:
                    logger.warning("[{} - {}] click failed, please check if clicked.".format(task_name, phase_name))

            elif phase_action == "doubleClick":
                while iter < 3:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(
                        full_window, phase_template)
                    if find:
                        self.window.doubleClick(relative_x,relative_y)
                        logger.success("[{} - {}] doubleClick success".format(task_name, phase_name))
                        break
                    else:
                        # 检查是否已经check
                        iter+=1
                        # logger.info("[{} - {}] doubleClick failed: not found, try {} times.".format(task_name, phase_name, iter))
                        sleep(0.5)    
                if iter == 3:
                    logger.warning("[{} - {}] doubleClick failed, please check if clicked.".format(task_name, phase_name))
        
            elif phase_action == "press":
                phase_key = phase["key"]
                phase_times = phase["times"]
                if phase_times == "dayOfWeek":
                    # 0~6 
                    dayOfWeek = datetime.today().weekday()
                    phase_times = dayOfWeek
                self.window.press(phase_key,phase_times)
                logger.success("[{} - {}] press {} {} times.".format(task_name, phase_name, phase_key,phase_times))
                        
            elif phase_action == "check":
                while iter < 10:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(
                    full_window, phase_template)
                    if find:
                        logger.success("[{} - {}] check success.".format(task_name, phase_name))
                        break
                    else:
                        iter+=1
                        # logger.info("[{} - {}] check failed, try {} times.".format(task_name, phase_name, iter))
                        sleep(0.3)
                if iter == 10:
                    phase_type = phase.get("type")
                    if phase_type == "strict":
                        logger.error("[{} - {}] strict check failed, 将在 10 秒后结束脚本！".format(task_name, phase_name))
                        sleep(10)
                        raise RuntimeError("检查失败")
                    else:
                        logger.warning("[{} - {}] normal check failed, continue...".format(task_name, phase_name))
                        
            elif phase_action == "move":
                while iter < 3:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(full_window, phase_template)
                    if find:
                        self.window.move(relative_x,relative_y)   
                        logger.success("[{} - {}] move success".format(task_name, phase_name))
                        break
                    else:
                        iter+=1
                        sleep(0.5)    
                if iter == 3:
                    logger.warning("[{} - {}] move failed.".format(task_name, phase_name))
            
            elif phase_action == "wait":
                phase_time = phase.get("duration")
                sleep(int(phase_time))
                logger.success("[{} - {}] wait {} seconds success".format(task_name, phase_name, phase_time))
                    
            elif phase_action == "finish":
                logger.info("[{} - {}] waiting finish...".format(task_name, phase_name))
                while True:
                    full_window = self.window.screencap()
                    find, relative_x, relative_y = self.detector.find_location(
                        full_window, phase_template)
                    if find:
                        # imwrite(str(iter)+".png",full_window)
                        logger.success("[{} - {}] task finish success".format(task_name, phase_name))
                        break
                    sleep(0.5)
            elif phase_action == "slot":
                logger.info("[{} - {}] 转交给自定义插槽执行".format(task_name, phase_name))
                phase_name = phase.get("name")
                if phase_name == "seven_lights_holy_land":
                    seven_lights_holy_land(self.window,self.detector)
                elif phase_name == "diamond_mission":
                    diamond_mission(self.window,self.detector)