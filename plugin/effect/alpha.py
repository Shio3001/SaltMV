# coding:utf-8
import sys
import os
import copy

# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = "透明度"
        setting_effect.effect_point = {"alpha": 100}
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に現在のフレーム, 第五引数にエディタ情報, 操作一覧

    def main(self, data):

        data.draw = data.draw.astype('float32')

        # 透明度
        alpha_draw = data.np.full(data.draw[:, :, 3].shape, data.effect_value["alpha"] * 0.01)
        data.draw[:, :, 3] *= alpha_draw

        return data.draw, self.starting_point
