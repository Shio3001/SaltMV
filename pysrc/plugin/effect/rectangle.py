# coding:utf-8
import sys
import os
import copy

import numpy as np
# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = "図形[四角形]"
        setting_effect.effect_point = {"R": 255, "G": 255, "B": 255, "A": 255, "X size": 50, "Y size": 50}
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に現在のフレーム, 第五引数にエディタ情報, 操作一覧

    def main(self, data):

        # print("aho")

        X = int(data.effect_value["X size"])
        Y = int(data.effect_value["Y size"])

        #px = np.array([255, 255, 255, 100])

        #p = np.full(20, px)
        p2 = np.full((Y, X, 4), 255)
        p2[:, :, 0] = np.full((Y, X), data.effect_value["R"])
        p2[:, :, 1] = np.full((Y, X), data.effect_value["G"])
        p2[:, :, 2] = np.full((Y, X), data.effect_value["B"])
        p2[:, :, 3] = np.full((Y, X), data.effect_value["A"])

        print(p2.shape)

        data.draw = p2.astype('uint8')

        return "DRAW", data.draw, self.starting_point
