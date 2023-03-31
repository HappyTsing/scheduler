from automatic.window import Window
from automatic.detector import Detector
from automatic.config import IMAGE_PATH
from aircv import imread
from time import sleep
from loguru import logger
from os import path

def seer_login(window:Window, detector:Detector):
    TEMPLATE_PATH = path.join(IMAGE_PATH,"tasks","seer")
    TEMPLATE_LOGIN_SUCCESS = imread(path.join(TEMPLATE_PATH,"7.png"))
    TEMPLATE_LOGIN_NORMAL = imread(path.join(TEMPLATE_PATH,"5.png"))
    TEMPLATE_LOGIN_SELECT = imread(path.join(TEMPLATE_PATH,"6.png"))
    while True:
        full_window = window.screencap()
        find_success, x0, y0 = detector.find_location(full_window, TEMPLATE_LOGIN_SUCCESS)
        find_normal, x1, y1 = detector.find_location(full_window, TEMPLATE_LOGIN_NORMAL)
        find_select, x2, y2 = detector.find_location(full_window, TEMPLATE_LOGIN_SELECT)
        if find_success:
            logger.success("[slot: seer_login] 成功登录")
            break
        elif find_normal:
            window.click(x1,y1,1)
            logger.info("[slot: seer_login] 尝试点击未激活登录图标")
        elif find_select:
            window.click(x2,y2,1)
            logger.info("[slot: seer_login] 尝试点击激活登录图标")
            break
        sleep(1.5)
        logger.info("[slot: seer_login] 循环等待...")
        
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