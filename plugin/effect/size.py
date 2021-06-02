# coding:utf-8
import sys
import os
import copy
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
        resize_value = (round(data.effect_value["size_x"] * 0.01 * data.draw_size["x"]), round(data.effect_value["size_y"] * 0.01 * data.draw_size["y"]))
        data.draw = data.cv2.resize(data.draw, (resize_value))

        return data.draw, self.starting_point
