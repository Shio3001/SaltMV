
# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2


class Center:
    def __init__(self):
        self.addNewMov = []

    def main(self, thislayer, thislayer_reobj_now, inp_in):
        new_video = cv2.VideoCapture(inp_in)

        new_video_getlist = {"width": new_video.get(cv2.CAP_PROP_FRAME_WIDTH), "height": new_video.get(cv2.CAP_PROP_FRAME_HEIGHT), "fps": new_video.get(cv2.CAP_PROP_FPS), "count": new_video.get(cv2.CAP_PROP_FRAME_COUNT)}

        thislayer.retention_object[thislayer_reobj_now].unique_property = copy.deepcopy(new_video_getlist)
        del new_video_getlist

        print(thislayer.retention_object[thislayer_reobj_now].unique_property)
