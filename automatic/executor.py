from multiprocessing import Process
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
    def __init__(self,queue_image_receiver,queue_error_sender):
        super().__init__()  
        self.receiver = queue_image_receiver
        self.sender = queue_error_sender
        
    def get_screeshot(self):
        return self.receiver.get()
    
    def scheduler(self,task_schedule):
        now = datetime.now()
        schedule_hour,schedule_minute,schedule_second = str(task_schedule).split(":")
        schedule = datetime(year=now.year,month=now.month,day= now.day,hour=int(schedule_hour),minute=int(schedule_minute),second=int(schedule_second))
        sleep_time = schedule - now
        logger.info("将在 {} 后自动开始, 等待中...".format(strftime("%H:%M:%S", gmtime(sleep_time.seconds))))
        sleep(sleep_time.seconds)
        # 长时间等待似乎会识别错误，消耗几张图片试试
        for _i in range(5):
            self.get_screeshot()
        
    def click(self,target_image,times):
        for i in range(5):
            current_screenshot = self.get_screeshot()
            # imwrite(str(i)+".png",current_screenshot)
            find, x, y = find_location(current_screenshot, target_image)
            if find:
                click(x,y,times)
                return True
            else:
                # logger.info(" [{} - {}] click failed: not found, try {} times.".format(task_name, phase_name, i))
                sleep(0.5)
        return False
            
    def double_click(self,target_image):
        for i in range(5):
            current_screenshot = self.get_screeshot()
            find, x, y = find_location(current_screenshot, target_image)
            if find:
                doubleClick(x,y)
                return True
            else:
                # logger.info("[{} - {}] doubleClick failed: not found, try {} times.".format(task_name, phase_name, i))
                sleep(0.5)    
        return False
    
    # 键盘
    def keyboard(self,input:list):
        # logger.info(f"input: {input}")
        # 列表为空，则返回
        if not input:
            return True
        unique_list = []
        unique_list.append(input[0])
        pre = input[0]
        index = 1
        while(index < len(input)):
            now = input[index]
            if pre == now:
                if len(unique_list) == 1:
                    press(unique_list[0],1)
                    # logger.info(f"press: {unique_list}")
                else:
                    hotkey(*unique_list)
                    # logger.info(f"hotkey: {unique_list}")
                unique_list.clear()
            pre=now
            unique_list.append(now)
            index = index + 1
        if len(unique_list) == 1:
            press(unique_list[0],1)
            # logger.info(f"press: {unique_list}")
        else:
            hotkey(*unique_list)
            # logger.info(f"hotkey: {unique_list}")
        return True
    
    # 移动鼠标到某个地方
    def move_to(self,target_image):
        for i in range(5):
            current_screenshot = self.get_screeshot()
            find, x, y = find_location(current_screenshot, target_image)
            if find:
                move(x,y)   
                return True
            else:
                sleep(0.5)    
        return False
            
    def sleep(self,duration):
        sleep(int(duration))
        return True
        
    def wait_until(self,target_image):
        while True:
            current_screenshot = self.get_screeshot()
            find, x, y = find_location(current_screenshot, target_image)
            if find:
                return True
            sleep(0.5)
    
    # handler 为处理方法
    def slot(self,handler):
        if handler == "seer_login":
            # seer_login()
            return True
        # 没有对应 slot 的处理方法就返回 Fasle
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
        # 未匹配到就返回 False
        return False
    
    def exec_phase(self,phase):
        error_flag = False
        error_message = None
        if "img_path" in phase:
            target_image = imread(phase.get("img_path"))
        duration= phase.get("duration",1)
        input = phase.get("input",[])
        times = phase.get("times",1)
        path = phase.get("path")
        handler = phase.get("handler")
        action = phase.get("action")
        comment = phase.get("comment")
        action_handler = {
            "click":lambda:self.click(target_image,times),
            "doubleClick":lambda:self.double_click(target_image),
            "move":lambda:self.move_to(target_image),
            "keyboard":lambda:self.keyboard(input),
            "sleep":lambda:self.sleep(duration),
            "wait_until":lambda:self.wait_until(target_image),
            "open":lambda:self.open_app(path),
            "slot":lambda:self.slot(handler),
        }
        if action not in action_handler.keys():
            logger.error (f"action not found: {action}")
            error_message = f"Scheduler | action not found: {action}"
            error_flag = True
        try:
            if action_handler[action]():
                logger.success(f"{comment} success")
            else:
                logger.error(f"{comment} failed")
                error_message = f"Scheduler | {comment} failed"
                error_flag = True
        except Exception as e:
            logger.error(f"{e}")
            error_message = f"Scheduler | Exception {e}"
            error_flag = True
        # 若某个阶段执行失败，通知调度者
        if error_flag:
            self.sender.put(error_message)
            
            
    def exec_full(self):
        logger.info("Executor Start!")
        task = get_task()
        phases = task["phases"]
        times = task.get("times",1) # 默认为 1 次
        schedule_time = task.get("schedule")
        if times == 0:
            times = maxsize
            max_times = "INF" # 若为 0，则认为是无限循环
        else:
            max_times = times
        for i in range(times):
            logger.info(f"Round: {i+1}/{max_times}")
            if schedule_time:
                self.scheduler(schedule_time)
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
    def run(self):
        try:
            self.exec_full()
        except Exception as e:
            logger.error(f"{e} | executor will exit after 10s...")
            sleep(10)       
            
            