# coding:utf-8
import sys
import os
import copy
import cv2
# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = "画像"
        setting_effect.effect_point = {}
        setting_effect.various_fixed = {"path": ""}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]

        self.image_data = None
        self.now_file = None
        self.open_status = False

    def setup(self, file_name):
        try:
            image_dataBGR = cv2.imread(file_name)
            self.image_data = cv2.cvtColor(image_dataBGR, cv2.COLOR_BGR2RGBA)
            self.now_file = copy.deepcopy(file_name)
            self.open_status = True

        except:
            self.open_status = False

    def main(self, data):

        path = data.various_fixed["path"]

        if path != self.now_file or not self.open_status:
            self.setup(path)

        if not self.open_status:
            self.image_data = data.draw

        return self.image_data, self.starting_point
