
# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2


class Center:
    def __init__(self):
        self.addNewMov = []

    def main(self, thislayer, thislayer_reobj_now, responselist, inp_in):
        new_video = cv2.VideoCapture(inp_in)

        new_video_getlist = {"width": new_video.get(cv2.CAP_PROP_FRAME_WIDTH), "height": new_video.get(cv2.CAP_PROP_FRAME_HEIGHT), "fps": new_video.get(cv2.CAP_PROP_FPS), "count": new_video.get(cv2.CAP_PROP_FRAME_COUNT)}

        for i in range(int(round(new_video_getlist["count"]))):
            ret, frame = new_video.read()

            if ret == False:
                print("読み込みに失敗")
                return thislayer

            self.addNewMov.append(cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA))

        thislayer.retention_object[thislayer_reobj_now].unique_property = copy.deepcopy(new_video_getlist)
        thislayer.retention_object[thislayer_reobj_now].document = np.array(self.addNewMov)
        del new_video
        del new_video_getlist

        print(thislayer.retention_object[thislayer_reobj_now].unique_property)

        print(len(self.addNewMov))

        print("読み込みに成功")
        return thislayer, responselist[0]
