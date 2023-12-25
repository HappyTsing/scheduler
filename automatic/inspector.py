# -*-coding:UTF-8 -*-
from automatic.utils import find_location, get_task
from multiprocessing import Process
from time import sleep
from loguru import logger
from aircv import imread
from cv2 import imwrite
"""
监察者: 获取异常状态, 守护进程
"""


class Inspector(Process):
    # queue_image_receiver 从 Observer 中获取当前屏幕信息
    # queue_error_sender 将发现的漏洞写到 Queue 中，供执行者处理。Todo 当前的策略是发现问题就从头开始执行
    def __init__(self, queue_image_receiver, queue_error_sender):
        super().__init__(daemon=True)
        self.sender = queue_error_sender
        self.receiver = queue_image_receiver

    def get_screeshot(self):
        return self.receiver.get()

    # 获取图像，检查是否存在漏洞，存在则写入管道
    def exec_full(self):
        logger.info("Inspector Start!")
        task = get_task()
        error_image_paths = task.get("errors")
        while True:
            current_screenshot = self.get_screeshot()
            # imwrite("current_screenshot.png", current_screenshot)
            for error_image_path in error_image_paths:
                error_image = imread(error_image_path)
                find, x, y = find_location(current_screenshot, error_image)
                if find:
                    logger.error("Inspector Find Error: image path: {}".format(error_image_path))
                    error_message = "Inspector| Hit Error Image: {}".format(error_image_path)
                    self.sender.put(error_message)
                sleep(2)
    def run(self):
        try:
            self.exec_full()
        except Exception as e:
            logger.error(f"{e} | inspector will exit after 10s...")
            sleep(10)       