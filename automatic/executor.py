from multiprocessing import Process
from automatic.slots import seer_login
from time import sleep,strftime,gmtime
from aircv import imread
# from cv2 import imwrite
from loguru import logger
from datetime import datetime
from automatic.utils import *
from os import path, listdir, system, rename
from re import search
from automatic.utils import get_task
from sys import maxsize
class Executor(Process):
    def __init__(self,queue_image_receiver):
        super().__init__()  
        self.receiver = queue_image_receiver
        
    def get_screeshot(self):
        return self.receiver.get()
    
    def scheduler(self,task_schedule):
        now = datetime.now()
        schedule_hour,schedule_minute,schedule_second = str(task_schedule).split(":")
        schedule = datetime(year=now.year,month=now.month,day= now.day,hour=int(schedule_hour),minute=int(schedule_minute),second=int(schedule_second))
        wait = schedule - now
        logger.info("将在 {} 后自动开始, 等待中...".format(strftime("%H:%M:%S", gmtime(wait.seconds))))
        sleep(wait.seconds)
        
    def click(self,target_image,times):
        iter = 0
        while iter < 5:
            current_screenshot = self.get_screeshot()
            # imwrite(str(iter)+".png",current_screenshot)
            find, x, y = find_location(
                current_screenshot, target_image)
            if find:
                click(x,y,times)
                return True
            else:
                # 检查是否已经check
                iter+=1
                # logger.info(" [{} - {}] click failed: not found, try {} times.".format(task_name, phase_name, iter))
                sleep(0.5)
        return False
            
    def double_click(self,target_image):
        iter = 0
        while iter < 5:
            current_screenshot = self.get_screeshot()
            find, x, y = find_location(
                current_screenshot, target_image)
            if find:
                doubleClick(x,y)
                return True
            else:
                # 检查是否已经check
                iter+=1
                # logger.info("[{} - {}] doubleClick failed: not found, try {} times.".format(task_name, phase_name, iter))
                sleep(0.5)    
        return False

    def press(self,key,times):
        press(key,times)
        return True
        
    def hotkey(self,keys):
        hotkey(*keys)
        return True
    
    def move(self,target_image):
        iter = 0
        while iter < 5:
            current_screenshot = self.get_screeshot()
            find, x, y = find_location(current_screenshot, target_image)
            if find:
                move(x,y)   
                return True
            else:
                iter+=1
                sleep(0.5)    
        return False
            
    def wait(self,duration):
        sleep(int(duration))
        return True
        
    def finish(self,target_image):
        while True:
            current_screenshot = self.get_screeshot()
            find, x, y = find_location(
                current_screenshot, target_image)
            if find:
                return True
            sleep(0.5)
    
    def slot(self,handler):
        if handler == "seer_login":
            seer_login(self.observer)
            return True
        return False
    
    def open_app(self,full_path):
        dir_path = path.dirname(full_path)
        # 文件名可以是正则表达式
        file_name_reg = path.basename(full_path)
        files_list = listdir(dir_path)
        for file_name in files_list:
            # 返回第一个正则匹配的软件
            if search(file_name_reg,file_name):
                # logger.info("匹配成功：{}".format(file_name))
                app_path  = path.join(dir_path,file_name)
                cmd = "start \"\" \"{}\"".format(app_path)
                # logger.info(cmd)
                system(cmd)
                return True
        return False
    
    def exec_phase(self,phase):
        if "img_path" in phase:
            target_image = imread(phase.get("img_path"))
        duration= phase.get("duration")
        key = phase.get("key")
        keys = phase.get("keys")
        times = phase.get("times")
        path = phase.get("path")
        if not times:
            times = 1
        handler = phase.get("handler")
        action = phase.get("action")
        comment = phase.get("comment")
        if action == "click":
            if self.click(target_image,times):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        elif action == "doubleClick":
            if self.double_click(target_image):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        elif action == "press":
            if self.press(key,times):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        elif action == "hotkey":
            if self.hotkey(keys):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        elif action == "move":
            if self.move(target_image):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        elif action == "wait":
            if self.wait(duration):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        elif action == "finish":
            if self.finish(target_image):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        elif action == "slot":
            if self.slot(handler):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        elif action == "open":
            if self.open_app(path):
                logger.success("{} success".format(comment))
            else:
                logger.error("{} failed".format(comment))
        else:
            logger.error ("action not found: {}".format(action))
            
    def run(self):
        logger.info("Executor Start!")
        task = get_task()
        phases = task["phases"]
        times = task.get("times")
        schedule_time = task.get("schedule")
        # 默认为 1
        if not times:
            times = 1
        # 若为 0，则认为是无限循环
        if times == 0:
            times = maxsize
            max_times = "INF"
        else:
            max_times = times
        for i in range(times):
            logger.info(f"Round: {i+1}/{max_times}")
            if schedule_time:
                self.scheduler(schedule_time)
                # 长时间等待似乎会识别错误，消耗几张图片试试
                for _i in range(3):
                    self.get_screeshot()
            for phase in phases:
                action = phase.get("action")
                if action != "loop":
                    self.exec_phase(phase)
                else:
                    loop_id = phase.get("loop_id")
                    times = phase.get("times")
                    loop_phases = task["loops"][loop_id]
                    for i in range(times):
                        for loop_phase in loop_phases:
                            self.exec_phase(loop_phase)
                        
                
            
            