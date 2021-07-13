import cv2
import numpy as np

class Video_Image_Stack:
    def __init__(self):
        self.new_video = None
        self.video_property = None

    def video_image_import(self,path):
        try:
            self.new_video = cv2.VideoCapture(path)
        except:
            print("読み込みに失敗 try - except")
        if self.new_video.isOpened() != True:
            print("読み込みに失敗 isOpened")
        else:
            self.video_property = {"width": self.new_video.get(cv2.CAP_PROP_FRAME_WIDTH),
                                    "height": self.new_video.get(cv2.CAP_PROP_FRAME_HEIGHT), 
                                    "fps": self.new_video.get(cv2.CAP_PROP_FPS), 
                                    "count": self.new_video.get(cv2.CAP_PROP_FRAME_COUNT)}

    def  video_image_get(self,frame):

        if self.video_property["count"] - 1 < frame:
            frame = self.video_property["count"] - 1

        self.new_video.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, draw = self.new_video.read()

        if ret:
            pass

        if not ret:
            return -1

        draw_uint8 = cv2.cvtColor(draw.astype('uint8'), cv2.COLOR_BGR2RGBA)
        return draw_uint8

