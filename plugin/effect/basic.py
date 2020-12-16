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

        return setting_effect


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に現在のフレーム, 第五引数にエディタ情報, 操作一覧

    def main(self, data):
        self.starting_point = [data.position["x"], data.position["y"]]

        print("仮座標決定 : " + str(self.starting_point))
        return data.draw, self.starting_point
