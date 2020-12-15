# coding:utf-8
import sys
import numpy
import os
import copy

# 削除厳禁！


class InitialValue:
    def __init__(self):
        pass

    def main(self, elements):
        setting_effect = elements.effectElements()
        setting_effect.effectname = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effectPoint = [{"time": 0, "x": 0, "y": 0, " z_angle ": 0, " alpha ": 100, "size": 0}]
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()
        setting_effect.calculation_mode = True

        return setting_effect


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]

        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に画面サイズ情報, 第五引数に現在のフレームが入ってくる
    def main(self, draw, whereabouts, now_frame, editor, draw_operation):

        editor_size = {"x": editor[0], "y": editor[1]}
        draw_size = {"x": draw.shape[1], "y": draw.shape[0]}

        for i in ["x", "y"]:
            whereabouts[i] = draw_operation.middle_change(whereabouts[i], draw_size[i], editor_size[i])

        self.starting_point = [whereabouts["x"], whereabouts["y"]]

        print("仮座標決定 : " + str(self.starting_point))

        return draw, self.starting_point
