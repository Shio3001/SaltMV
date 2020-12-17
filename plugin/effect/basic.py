# coding:utf-8
import sys
import numpy as np
import os
import copy

# 削除厳禁！


class InitialValue:
    def __init__(self):
        pass

    def main(self, elements):
        setting_effect = elements.effectElements()
        setting_effect.effectname = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effectPoint = [{"time": 0, "x": 0, "y": 0, "angle_z": 0, "alpha": 100, "size_x": 100, "size_y": 100}]
        setting_effect.various_fixed = {"size_lnk": True}
        setting_effect.procedure = CentralRole()

        return setting_effect


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に現在のフレーム, 第五引数にエディタ情報, 操作一覧

    def main(self, data):

        # 座標
        self.starting_point = [data.position["x"], data.position["y"]]

        data.draw = data.draw.astype('float32')

        # 透明度
        alpha_draw = np.full(data.draw[:, :, 3].shape, data.position["alpha"] * 0.01)
        data.draw[:, :, 3] *= alpha_draw

        # 拡大縮小
        # = (data.position["size_x"] * 0.01, data.position["size_y"] * 0.01)
        #data.draw = np.kron(np.eye(data.position["size_x"] * 0.01), data.draw)

        # 回転

        return data.draw, self.starting_point
