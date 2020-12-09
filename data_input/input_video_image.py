
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


class CentralRole:
    def __init__(self):
        self.addNewMov = []

    def video(self, thislayer, thislayer_reobj_now, responselist, inp_in):
        #thislayer.retention_object[thislayer_reobj_now].unique_property = copy.deepcopy(new_video_getlist)
        thislayer.retention_object[thislayer_reobj_now].document = inp_in
        thislayer.retention_object[thislayer_reobj_now].objectType = "video"
        #del new_video
        #del new_video_getlist

        print(thislayer.retention_object[thislayer_reobj_now].unique_property)

        # print(len(self.addNewMov))

        print("読み込みに成功")
        return thislayer, responselist[0]

    def image(self, thislayer, thislayer_reobj_now, responselist, inp_in):
        #thislayer.retention_object[thislayer_reobj_now].document = np.array([cv2.cvtColor(new_image, cv2.COLOR_RGB2RGBA)])
        thislayer.retention_object[thislayer_reobj_now].document = inp_in
        thislayer.retention_object[thislayer_reobj_now].objectType = "image"

        return thislayer, responselist[0]
