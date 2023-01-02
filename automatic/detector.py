from automatic.config import config
# from config import config
import cv2
import aircv as ac 
from loguru import logger

class Detector:
    def __init__(self):
        self.threshold = 0.995
        logger.info("init detector")
        
    # aircv相关操作
    # 找到图片A在图片B的位置
    def find_location(self,image_src,image_search):
        result = ac.find_template(image_src,image_search,self.threshold)
        if(result!=None):        
            logger.info(result)
            x = result['result'][0]
            y = result['result'][1]
            logger.info('找到目标，位于：({},{})'.format(x,y))
            return True,x,y
        else:
            logger.info("未找到！")
            return False,0,0