
# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class Center:
    def __init__(self):
        self.addNewMov = []

    def video(self, thislayer, thislayer_reobj_now, responselist, inp_in):

        try:
            new_video = cv2.VideoCapture(inp_in)
        except:
            print("読み込みに失敗 try - except")
            return thislayer, responselist[2]

        if new_video.isOpened() != True:
            print("読み込みに失敗 isOpened")
            return thislayer, responselist[2]

        new_video_getlist = {"width": new_video.get(cv2.CAP_PROP_FRAME_WIDTH), "height": new_video.get(cv2.CAP_PROP_FRAME_HEIGHT), "fps": new_video.get(cv2.CAP_PROP_FPS), "count": new_video.get(cv2.CAP_PROP_FRAME_COUNT)}

        # for i in new_video_getlist["count"]:
        #    ret, frame = new_video.read()
        #
        #    self.addNewMov.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))

        thislayer.retention_object[thislayer_reobj_now].unique_property = copy.deepcopy(new_video_getlist)
        thislayer.retention_object[thislayer_reobj_now].document = inp_in
        thislayer.retention_object[thislayer_reobj_now].objectType = "video"
        #del new_video
        #del new_video_getlist

        print(thislayer.retention_object[thislayer_reobj_now].unique_property)

        # print(len(self.addNewMov))

        print("読み込みに成功")
        return thislayer, responselist[0]

    def image(self, thislayer, thislayer_reobj_now, responselist, inp_in):

        new_image = None
        try:
            #new_image = np.array(Image.open(inp_in))
            new_image = Image.open(inp_in)
        except FileNotFoundError:
            print("読み込みに失敗 ファイルが存在しないか、動画を読み込もうとしています")
            return thislayer, responselist[1]
        except:
            print("読み込みに失敗" + str(sys.exc_info()))
            return thislayer, responselist[1]

        #thislayer.retention_object[thislayer_reobj_now].document = np.array([cv2.cvtColor(new_image, cv2.COLOR_RGB2RGBA)])
        thislayer.retention_object[thislayer_reobj_now].document = inp_in
        thislayer.retention_object[thislayer_reobj_now].objectType = "image"
        print("読み込みに成功")

        return thislayer, responselist[0]
