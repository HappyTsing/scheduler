# -*-coding:UTF-8 -*-
from automatic.observer import Observer
from automatic.slots import seer_login
from time import sleep,strftime,gmtime
from aircv import imread
# from cv2 import imwrite
from loguru import logger
from datetime import datetime
from automatic.utils import *
from os import path
class Executor:
    def __init__(self):
        self.observer = Observer()
        
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
            current_screenshot = self.observer.get_screeshot()
            # imwrite(str(iter)+".png",full_window)
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
            current_screenshot = self.observer.get_screeshot()
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
        while iter < 3:
            current_screenshot = self.observer.get_screeshot()
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
            current_screenshot = self.observer.get_screeshot()
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

                
    def submit(self,task):
        
        phases = task["phases"]
        schedule_time = task.get("schedule")
        if schedule_time:
            self.scheduler(schedule_time)
            # 长时间等待似乎会识别错误，消耗几张图片试试
            for _i in range(3):
                self.observer.get_screeshot()
                
        for phase in phases:
            img_path = phase.get("img_path")
            if img_path:
                if path.exists(img_path):
                    target_image = imread(img_path)
                else:
                    logger.error("file: {} does not exist".format(img_path))
            duration= phase.get("duration")
            key = phase.get("key")
            keys = phase.get("keys")
            times = phase.get("times")
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
                    
                
