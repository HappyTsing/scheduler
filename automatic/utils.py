from pyautogui import click as py_click, press as py_press, hotkey as py_hotkey, doubleClick as py_doubleClick, moveTo
from aircv import find_template
from loguru import logger
import json
from os import path
import sys


def print_hello():
    print("""
 ____   ___  _  _  ____  ____  _  _  __    ____  ____ 
/ ___) / __)/ )( \(  __)(    \/ )( \(  )  (  __)(  _ \\
\___ \( (__ ) __ ( ) _)  ) D () \/ (/ (_/\ ) _)  )   /
(____/ \___)\_)(_/(____)(____/\____/\____/(____)(__\_)
          """)
    print("Author: HappyTsing\tVersion: 5.2\t Last Update: 2024-12-19\n")


def get_current_path():
    if getattr(sys, 'frozen', False):
        # pyinstaller
        CUR_PATH = path.dirname(path.realpath(sys.argv[0]))
    else:
        CUR_PATH = path.dirname(path.dirname(path.abspath(__file__)))
    return CUR_PATH


def get_img_path(image_name, type="phases"):
    CUR_PATH = get_current_path()
    IMG_PATH = path.join(CUR_PATH, "img")
    if type == "phases":
        img_path = path.join(IMG_PATH, "phases", "{}.png".format(image_name))
    elif type == "errors":
        img_path = path.join(IMG_PATH, "errors", "{}.png".format(image_name))
    elif type == "loops":
        img_path = path.join(IMG_PATH, "loops", "{}.png".format(image_name))
    else:
        raise
    if not path.exists(img_path):
        logger.error("img file: {} does not exist.".format(img_path))
        raise
    return img_path

'''
@return: task/None
'''
def get_task():
    CUR_PATH = get_current_path()
    TASK_PATH = path.join(CUR_PATH, "task.json")
    if not path.exists(TASK_PATH):
        logger.error("task file: {} does not exist.".format(TASK_PATH))
        return None
    with open(TASK_PATH, 'r', encoding="utf8") as f:
        task = json.load(f)
    task_preprocessed = task
    phases = task.get("phases")
    loops = task.get("loops")
    errors = task.get("errors")
    phases_new = []
    for phase in phases:
        if "image_name" in phase:
            phase["img_path"] = get_img_path(phase["image_name"])
            phase.pop("image_name")
        # print(phase)
        phases_new.append(phase)
    task_preprocessed["phases"] = phases_new
    
    if loops:
        for loop_id, loop_phases in loops.items():
            loop_phase_new = []
            for loop_phase in loop_phases:
                if "image_name" in loop_phase:
                    loop_phase["img_path"] = get_img_path(loop_phase["image_name"],type="loops")
                    loop_phase.pop("image_name")
                loop_phase_new.append(loop_phase)
            task_preprocessed["loops"] = loop_phase_new

    task_preprocessed["errors"] = []
    if errors:
        for image_name in errors:
            task_preprocessed["errors"].append(get_img_path(image_name, type="errors"))
    # logger.info(task_preprocessed)
    return task_preprocessed

def get_config():
    CUR_PATH = get_current_path()
    CONFIG_PATH = path.join(CUR_PATH, "config.json")
    if not path.exists(CONFIG_PATH):
        logger.warning("config file: {} does not exist. using default config".format(CONFIG_PATH))
        return {}
    with open(CONFIG_PATH, 'r', encoding="utf8") as f:
        config = json.load(f)
    return config
CONFIG = get_config()
# aircv相关操作
# 找到 图片A 在 图片B 的位置
def find_location(image_src, image_search):
    threshold = CONFIG.get("threshold",0.99)
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

# pyautogui 键鼠操作
def move(x, y, movetime=0):  # 鼠标移动 x,y_移动位置，movetime_移动时间
    moveTo(x, y, duration=movetime)


def click(x, y, times, type="left"):		# left right middle
    py_click(x, y, clicks=int(times), button=type, interval=0.5)


def doubleClick(x, y, type="left"):
    py_doubleClick(x, y, button=type)


def press(key, times):
    py_press(key, presses=times, interval=0.1)


def hotkey(*keys):
    py_hotkey(*keys)
