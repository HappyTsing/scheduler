# from win32gui import EnumWindows, GetClassName, SendMessage, SetForegroundWindow, GetWindowRect, GetWindowText, DeleteObject, GetWindowDC
# from win32ui import CreateBitmap,CreateDCFromHandle
# from win32con import WM_SYSCOMMAND,SC_RESTORE
# from win32con import SRCCOPY
from pyautogui import screenshot as pyautogui_screenshot
from loguru import logger
from multiprocessing import Process
from numpy import uint8, frombuffer, array
from cv2 import cvtColor, COLOR_RGB2BGR
"""
观察者：获取最新的屏幕截图, 守护进程
"""

# 自定义类，继承 Process 类，重写run方法，每次实例化这个类的时候，就等同于实例化一个进程对象
class Observer(Process):
    def __init__(self, queue_image_sender):
        super().__init__(daemon=True)
        # todo 直接改为修改 self.image 是否可行
        self.image = None
        self.sender = queue_image_sender

    # bloonstd无法获取通过win32获取屏幕截图，采用pyautogui的方式
    def run(self):
        logger.info("Observer Start!")
        while True:
            # 截图
            screenshot = pyautogui_screenshot()
            # 先转换为numpy数组，再将rgb格式转换为opencv的bgr格式
            image = cvtColor(array(screenshot), COLOR_RGB2BGR)
            # 将图片数组写入 Queue 中
            self.sender.put(image)
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
