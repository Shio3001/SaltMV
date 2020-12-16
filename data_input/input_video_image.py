
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

    def video_image(self, thislayer, thislayer_reobj_now, responselist, operation_list, elements, inp_in, inp_type):
        #thislayer.retention_object[thislayer_reobj_now].unique_property = copy.deepcopy(new_video_getlist)
        thislayer.retention_object[thislayer_reobj_now].document = inp_in
        thislayer.retention_object[thislayer_reobj_now].objectType = str(inp_type)
        #thislayer = operation_list["set"]["input_point"]["CentralRole"].effect_Initial_setting(thislayer, operation_list, elements, "basic")

        return thislayer, responselist[0]
