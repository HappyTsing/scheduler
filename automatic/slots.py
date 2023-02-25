from automatic.window import Window
from automatic.detector import Detector
from automatic.config import IMAGE_PATH
from aircv import imread
from time import sleep
from loguru import logger
from os import path

# def diamond_mission(window:Window, detector:Detector):
#     TEMPLATE_PATH = path.join(IMAGE_PATH,"tasks","diamond_mission")
#     TEMPLATE_SURE = imread(path.join(TEMPLATE_PATH,"21.png"))
#     while True:
#         full_window = window.screencap()
#         find_sure, x, y = detector.find_location(full_window, TEMPLATE_SURE)
#         if find_sure:
#             window.click(x,y,1)
#             logger.info("[slot: diamond_mission] find confirm window, clicked.")
#         else:
#             logger.success("[slot: diamond_mission] all confirm window has been clicked.")
#             break
        
# def seven_lights_holy_land(window:Window, detector:Detector):
#     TEMPLATE_PATH = path.join(IMAGE_PATH,"tasks","seven_lights_holy_land")
#     TEMPLATE_CHALLENGE = imread(path.join(TEMPLATE_PATH,"5.png"))
#     TEMPLATE_FINISHED = imread(path.join(TEMPLATE_PATH,"6.png"))
#     TEMPLATE_SUCCEED_UNFINISH = imread(path.join(TEMPLATE_PATH,"7.png"))
#     TEMPLATE_SUCCEED_FINISH = imread(path.join(TEMPLATE_PATH,"8.png"))
#     TEMPLATE_FAILED = imread(path.join(TEMPLATE_PATH,"9.png"))
#     while True:
#         full_window = window.screencap()
#         find_finished, _x, _y = detector.find_location(full_window, TEMPLATE_FINISHED)
#         find_succeed_unfinish, _x, _y = detector.find_location(full_window, TEMPLATE_SUCCEED_UNFINISH)
#         find_succeed_finish, _x, _y = detector.find_location(full_window, TEMPLATE_SUCCEED_FINISH)
#         find_failed, _x, _y = detector.find_location(full_window, TEMPLATE_FAILED)
#         if find_finished:
#             logger.info("[slot: seven_lights_holy_land] already finished.")
#             break
#         elif find_succeed_unfinish:
#             logger.success("[slot: seven_lights_holy_land] execute success, next iteration...")
#             sleep(2)
#             window.press("enter",1)
#         elif find_succeed_finish:
#             logger.success("[slot: seven_lights_holy_land] execute finish.")
#             break
#         elif find_failed:
#             logger.info("[slot: seven_lights_holy_land] battle lost, retry...")
#             find_challenge, x, y = detector.find_location(full_window, TEMPLATE_CHALLENGE)
#             if find_challenge:
#                 window.click(x,y,1)
#         sleep(0.5)