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
        setting_effect.path_type = {"path": "image"}


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]

        self.image_rendering_main_data = None
        self.now_file = "test_none"
        self.open_status = False

        print("初期化CentralRole")

        #self.main = main

    def main(self, rendering_main_data):

        path = rendering_main_data.various_fixed["path"]

        # if not self.open_status:
        #     self.image_rendering_main_data = rendering_main_data.draw

        if rendering_main_data.salt_file.get_bool(rendering_main_data.various_fixed["path"]) is False:
            pass
        else:
            rendering_main_data.draw = rendering_main_data.salt_file.get_image(rendering_main_data.various_fixed["path"])

        return self.image_rendering_main_data, self.starting_point
