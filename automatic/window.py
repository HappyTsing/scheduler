# -*-coding:UTF-8 -*-
from pyautogui import click,press,hotkey,doubleClick,moveTo,screenshot as pyautogui_screenshot
# from win32gui import EnumWindows, GetClassName, SendMessage, SetForegroundWindow, GetWindowRect, GetWindowText, DeleteObject, GetWindowDC
# from win32ui import CreateBitmap,CreateDCFromHandle
# from win32con import WM_SYSCOMMAND,SC_RESTORE
# from win32con import SRCCOPY
# from loguru import logger
from multiprocessing import Process, Pipe
from numpy import uint8,frombuffer,array
from cv2 import cvtColor,COLOR_RGB2BGR
"""
游戏窗口，不断获取窗口截图
"""


class Window(Process):
    def __init__(self):
        super().__init__(daemon=True)
        # 创建两个Pipe，通过sender.send()写入，receiver.recv()取出
        self.receiver, self.sender = Pipe(False)
        self.start()

    def screencap(self):
        # 返回屏幕截图
        return self.receiver.recv()

    # bloonstd无法获取通过win32获取屏幕截图，采用pyautogui的方式
    def run(self):
        while True:
            # 截图
            screenshot = pyautogui_screenshot()
            # 先转换为numpy数组，再将rgb格式转换为opencv的bgr格式
            image = cvtColor(array(screenshot), COLOR_RGB2BGR)
            # 将图片数组写入管道中
            self.sender.send(image)

    # win32方式截图，参考：https://blog.csdn.net/weixin_40875387/article/details/127716504
    # 若使用这种方式截图，请采用相对位置点击等...
    # def run(self):
    #     hwnd_dc = GetWindowDC(self.hwnd)
    #     mfc_dc = CreateDCFromHandle(hwnd_dc)
    #     save_dc = mfc_dc.CreateCompatibleDC()
    #     while True:
    #         # 屏幕截图
    #         bitmap = CreateBitmap()
    #         rect = GetWindowRect(self.hwnd)
    #         width = rect[2] - rect[0]
    #         height = rect[3] - rect[1]
    #         bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    #         save_dc.SelectObject(bitmap)
    #         save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), SRCCOPY)
    #         ints_array = bitmap.GetBitmapBits(True)
    #         DeleteObject(bitmap.GetHandle())
    #         image = frombuffer(ints_array, dtype=uint8)
    #         image.shape = (height, width, 4)

    #         # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 转换RGB顺序
    #         # cv2.imshow('baofeng', image)
    #         # cv2.imwrite("main1.png", intdata)
    #         # cv2.waitKey()

    #         self.sender.send(image)


    def move(self, x, y, movetime=0):  # 鼠标移动 x,y_移动位置，movetime_移动时间
        moveTo(x, y, duration=movetime)

    def click(self, x, y, times, type="left"):		# left right middle
        click(x, y, clicks=int(times), button=type,interval=0.5)

    def doubleClick(self, x, y, type="left"):
        doubleClick(x, y, button=type)

    def press(self, key, times):
        press(key, presses=times, interval=0.1)
    
    def hotkey(self,*keys):
        hotkey(*keys)
