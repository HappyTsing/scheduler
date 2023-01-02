
# -*-coding:UTF-8 -*-
import ctypes
import multiprocessing
import sys
from threading import Thread
from time import sleep
import aircv as ac 
import os

# image = pyautogui.screenshot()
# image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
# cv2.imshow("Screenshot", image)
# cv2.waitKey(0)
import cv2
from automatic.window import Window
from automatic.detector import Detector
from loguru import logger
from automatic.config import config
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
    logger.info("main")
    window = Window()
    
    tasks = config["tasks"]
    img_path = config["img_path"]
    detector = Detector()
    Timer()
    tasks_num = 0
    for task in tasks:
        phase_num = 0
        logger.info(task)
        for task_name,task_phases in task.items():
            logger.info("任务: {}".format(task_name))
            i = 0
            while True:
                
                full_window = window.screencap()
                image_name = str(i)+".png"
                i+=1
                cv2.imwrite(image_name,full_window)
                phase_template_img_name = str(task_phases[phase_num]["id"])+".png"
                logger.info(phase_template_img_name)
                phase_template_path = os.path.join(img_path,task_name,phase_template_img_name)
                logger.info("获取阶段 {} 模板路径：{}".format(phase_num,phase_template_path))
                phase_template = ac.imread(phase_template_path)
                phase_action = task_phases[phase_num]["action"]
                phase_name = task_phases[phase_num]["name"]
                logger.info("任务阶段：{}".format(phase_name))
                if phase_action == "click":
                    find,relative_x,relative_y = detector.find_location(full_window,phase_template)
                    if find:
                        window.click(relative_x,relative_y)
                    else:
                        # 检查是否已经check
                        logger.info("action: click, 未找到")
                elif phase_action == "check":
                    find,relative_x,relative_y = detector.find_location(full_window,phase_template)
                    
                    if find:
                        logger.info("action_click, 已经点击")
                elif phase_action == "finish":
                    
                    sleep(2)
                    find,relative_x,relative_y = detector.find_location(full_window,phase_template)
                    
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
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)
