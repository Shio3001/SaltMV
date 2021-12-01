# coding:utf-8
import sys
import os
import copy
import math
# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effect_point = {"size_x": 100, "size_y": 100}
        setting_effect.various_fixed = {"size_lnk": True}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に現在のフレーム, 第五引数にエディタ情報, 操作一覧

    def main(self, data):

        if data.draw_size["x"] == 0 or data.draw_size["y"] == 0:
            return data.draw, self.starting_point

        size_x = data.effect_value["size_x"]
        size_y = data.effect_value["size_y"]

        print("size_x, size_y", size_x, size_y)

        if data.various_fixed["size_lnk"] == True:
            size_y = size_x

        resize_value = (math.floor(size_x * 0.01 * data.draw_size["x"]), math.floor(size_y * 0.01 * data.draw_size["y"]))

        data.draw = data.cv2.resize(data.draw, resize_value)

        return data.draw, self.starting_point
