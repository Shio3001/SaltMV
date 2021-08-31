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

    def main(self, data):

        path = data.various_fixed["path"]

        try:
            im = cv2.imread(path)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
        except:
            return data.draw, self.starting_point

        return im, self.starting_point
