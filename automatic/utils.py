# -*-coding:UTF-8 -*-
from pyautogui import click as py_click,press as py_press,hotkey as py_hotkey,doubleClick as py_doubleClick,moveTo
from aircv import find_template
from loguru import logger
import json
from os import path
import sys


def print_hello():
    print("""
 _______ .__   __.        __    ______   ____    ____
|   ____||  \ |  |       |  |  /  __  \  \   \  /   /
|  |__   |   \|  |       |  | |  |  |  |  \   \/   /
|   __|  |  . `  | .--.  |  | |  |  |  |   \_    _/
|  |____ |  |\   | |  `--'  | |  `--'  |     |  |
|_______||__| \__|  \______/   \______/      |__|""")
    print("\n\tAuthor: HappyTsing\tVersion: 2.0\n")


def get_current_path():
    if getattr(sys,'frozen',False):
        # pyinstaller
        CUR_PATH = path.dirname(path.dirname(path.realpath(sys.argv[0])))
    else:
        CUR_PATH = path.dirname(path.dirname(path.abspath(__file__)))
    return CUR_PATH


def get_img_path(id,task_name):
    CUR_PATH = get_current_path()
    IMG_PATH = path.join(CUR_PATH,"img")
    return path.join(IMG_PATH,task_name,"phases","{}.png".format(id))
    

def get_config():
    CUR_PATH = get_current_path()
    CONFIG_PATH = path.join(CUR_PATH,"task.json")
    with open(CONFIG_PATH, 'r',encoding="utf8") as f:
        config = json.load(f)
    # print(config)
    config_preprocessed = config
    for task_name,task in config.items():
        phases = task.get("phases")
        loops = task.get("loops")
        phases_new = []
        for phase in phases:
            if "img_id" in phase:
                phase["img_path"] = get_img_path(phase["img_id"],task_name)
                phase.pop("img_id")
            print(phase)
            phases_new.append(phase)
        config_preprocessed[task_name]["phases"] = phases_new
        
        for loop_name,loop_phases in loops.items():
            loop_phase_new =[]
            for loop_phase in loop_phases:
                if "img_id" in loop_phase:
                    loop_phase["img_path"] = get_img_path(loop_phase["img_id"],task_name)
                    loop_phase.pop("img_id")
                loop_phase_new.append(phase)
            config_preprocessed[task_name]["loops"][loop_name] = loop_phase_new
    # logger.info(config_preprocessed)
    return config_preprocessed


# aircv相关操作
# 找到图片A在图片B的位置
def find_location(image_src, image_search):
    # todo 从配置文件读入
    threshold=0.99
    result = find_template(image_src, image_search, threshold)
    if (result != None):
        # logger.info(result)
        x = result['result'][0]
        y = result['result'][1]
        # logger.info('找到目标，中点位于：({},{})'.format(x, y))
        return True, x, y
    else:
        # logger.info("模板图片未找到！")
        return False, 0, 0
    
def move( x, y, movetime=0):  # 鼠标移动 x,y_移动位置，movetime_移动时间
    moveTo(x, y, duration=movetime)

def click(x, y, times, type="left"):		# left right middle
    py_click(x, y, clicks=int(times), button=type,interval=0.5)

def doubleClick(x, y, type="left"):
    py_doubleClick(x, y, button=type)

def press(key, times):
    py_press(key, presses=times, interval=0.1)

def hotkey(*keys):
    py_hotkey(*keys)