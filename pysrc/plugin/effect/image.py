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
        setting_effect.effect_point_path_name = ["path"]
        setting_effect.procedure = CentralRole()

        print(setting_effect.procedure.setup.__self__)


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]

        self.image_data = None
        self.now_file = "test_none"
        self.open_status = False

        print("初期化CentralRole")

        #self.main = main

    def setup(self, file_name):

        try:
            image_dataBGR = cv2.imread(file_name)
            self.image_data = cv2.cvtColor(image_dataBGR, cv2.COLOR_BGR2RGBA)
            self.now_file = copy.deepcopy(file_name)
            self.open_status = True
            print("try-成功")

        except:
            self.open_status = False
            print("try-失敗")

        print("setup", self.now_file, self.open_status)

    def main(self, data):

        print("main", self.now_file, self.open_status, self)

        path = data.various_fixed["path"]

        if path != self.now_file or not self.open_status:
            print(path != self.now_file, not self.open_status, self.now_file, path, self.open_status)
            self.setup(path)

        if not self.open_status:
            self.image_data = data.draw

        print("main_end", self.now_file, self.open_status)

        print(self.image_data, self.image_data.dtype, self.image_data.shape)

        return self.image_data, self.starting_point
