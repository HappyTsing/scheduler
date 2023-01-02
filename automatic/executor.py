# from loguru import logger
# from window import Window
# from detector import Detector
# from time import sleep
# from threading import Thread
# import aircv as ac 
# import cv2
# import os
# import yaml
# import os


# class Executor:
#     def __init__(self):
#         self.window = Window()
#         self.detector = Detector()
        
#         CUR_PATH = os.path.abspath(os.path.dirname(__file__))
#         with open(os.path.join(CUR_PATH, "task.yaml"), 'r', encoding='utf-8') as _fp:
#             self.tasks = yaml.safe_load(_fp)
        
#         self.img_path = os.path.join(CUR_PATH,"img")
    
    
#     # 根据输入的队名更改相应的队伍
#     def change_team(self,team_name):
#         return
    
#     def submit(self,task_name):
#         # with os.scandir("C:/Users/leki/Desktop/roco-master/automatic/img") as entries:
#         #     for entry in entries:
#         #         if entry.is_dir and entry.name == task_name:
#         #             with os.scandir(entry.path) as target_entries:
#         #                 for target_entry in target_entries:
#         #                     if target_entry.is_file:
#         #                         logger.info(target_entry.name)
#         task = self.tasks[task_name]
#         logger.info(task)
        
        
                                
                        
#         while True:
#             real_time_window = self.window.screencap()
#             # cv2.imshow("main", screen)
#             template = ac.imread("C:/Users/leki/Desktop/roco-master/automatic/img/template/template1.png")
#             self.detector.find_location(real_time_window,template)
        
#         sleep(20)

    
# executor = Executor()        
# executor.submit("friend_manor_assistant")
