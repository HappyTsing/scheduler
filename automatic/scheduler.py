"""
|调度者| --> |执行者| + |监察者| —-> 二者调用 |观察者| 获取当前屏幕情况
具体来说：
scheduler 调度者新建两个通信Queue + 三个子进程：
    1. executor 执行者: 执行任务
    2. inspector 监察者: 监察是否有漏洞出现，并将问题汇报给调度者
    3. observer 观察者: 观察当前屏幕信息，并将二者写入队列中，供 executor 和 inspector 使用
scheduler 不断监听 inspector 的反馈情况，目前的简单处理: 出现漏洞则 清空队列 + 中断所有子进程，并重启所有队列和进程。
"""
from multiprocessing import Queue
from automatic.executor import Executor
from automatic.inspector import Inspector
from automatic.observer import Observer
from automatic.utils import send_email
from time import sleep
from loguru import logger
from os import path

MAX_QUEUE_IMAGE_SIZE = 2
MAX_QUEUE_ERROR_SIZE = 3
MAX_RESTART_TIME = 3 # 最大重启次数
email_notified = False
seer_login_timeout_handler_started = False

class Scheduler:
    def __init__(self):
        logger.info("Scheduler Init!")
        # queue_image 用于传输屏幕截图信息
        self.queue_image = Queue(maxsize=MAX_QUEUE_IMAGE_SIZE)
        # queue_error 用于传输监察者检测到的问题信息，目前检测到问题就立刻重启！
        self.queue_error = Queue(maxsize=MAX_QUEUE_ERROR_SIZE)
        # 创建执行者、监察者和观察者对象
        self.executor = Executor(self.queue_image,self.queue_error)
        self.inspector = Inspector(self.queue_image, self.queue_error)
        self.observer = Observer(self.queue_image)

    def start(self):
        global email_notified
        global seer_login_timeout_handler_started
        restart_times = 0
        self.observer.start()
        self.inspector.start()
        self.executor.start()
        while (self.executor.is_alive()):
            # queue_error_size = self.queue_error.qsize()
            # logger.info("队列大小 {}".format(queue_error_size))
            if not self.queue_error.empty():
                # 如果队列不为空，取出数据
                error_message = self.queue_error.get()
                if "Executor" in error_message:
                    if "Restart" in error_message and restart_times < MAX_RESTART_TIME:
                        logger.error(f"Find Error: {error_message}. Try to Restart SubProcess...")
                        self.restart()
                        restart_times += 1
                    elif "Stop" in error_message:
                        logger.error(f"Find Error: {error_message}. Try to Stop SubProcess...")
                        return
                    return
                elif "Inspector" in error_message:
                    # 出现超时，则等待 ray_update 出现
                    if not seer_login_timeout_handler_started and "seer_login_timeout.png" in error_message:
                        logger.error(f"Find Error: {error_message}. Try to Start seer_login_timeout_handler...")
                        self.stop_and_start(path.join("img","errors","seer_login_timeout_handler"))
                        seer_login_timeout_handler_started = True
                        logger.success("Start seer_login_timeout_handler Success")
                    elif not email_notified and "ray_update.png" in error_message:
                        logger.error(f"Find Error: {error_message}. Try to Send Email Notify Owner...")
                        send_email("Scheduler","雷小伊更新啦~")
                        email_notified = True
                        logger.success("Notify Success")
                        sleep(2)
                        return
            else:
                # 如果队列为空，等待一段时间再尝试
                sleep(1)
    def stop_and_start(self,handler_path):
        self.executor.terminate()
        self.inspector.terminate()
        self.observer.terminate()
        logger.info("Terminal SubProcess Success: Executor, Inspector, Observer")
        self.executor.join()
        self.inspector.join()
        self.observer.join()
        logger.info("Wait SubProcess Finish Success: Executor, Inspector, Observer")
        self.clear_queue()
        logger.info("Clear Queue Success: queue_error, queue_image")
        self.executor = Executor(self.queue_image,self.queue_error,handler_path)
        self.inspector = Inspector(self.queue_image, self.queue_error,handler_path)
        self.observer = Observer(self.queue_image)
        self.start()
        logger.info("Restart SubProcess Success: Executor, Inspector, Observer")
        
    def restart(self):
        self.stop_and_start("default")

    def clear_queue(self):
        self.queue_error.close()
        self.queue_image.close()
        self.queue_image = Queue(maxsize=MAX_QUEUE_IMAGE_SIZE)
        self.queue_error = Queue(maxsize=MAX_QUEUE_ERROR_SIZE)