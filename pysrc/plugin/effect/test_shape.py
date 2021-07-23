# coding:utf-8
import sys
import os
import copy

import numpy as np
# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = "シーン"
        setting_effect.effect_point = {}
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に現在のフレーム, 第五引数にエディタ情報, 操作一覧

    def main(self, data):

        print("aho")

        x = int(round(data.draw_size["x"] / 2))
        y = int(round(data.draw_size["y"] / 2))

        px = [255, 255, 255, 100]

        data.draw[y:y+20, x:x+20, :] = np.full((20, 20, 4), 100)

        return data.draw, self.starting_point
