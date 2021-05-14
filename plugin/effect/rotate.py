# coding:utf-8
import sys
import os
import copy

# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effect_point = [{"time": 0, "rotate_z": 0, "rotate_center_x": 0, "rotate_center_y": 0}]
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に現在のフレーム, 第五引数にエディタ情報, 操作一覧

    def main(self, data):
        draw_size = tuple(map(int, data.draw_size.values()))
        center = (draw_size[0] / 2 + data.effect_value["rotate_center_x"], draw_size[1] / 2 + data.effect_value["rotate_center_y"])

        rotate_list = [[self.rotate_z, data.effect_value["rotate_z"]]]

        for i in rotate_list:
            data.draw = i[0](data, data.draw, draw_size, center, i[1])

        return data.draw, self.starting_point

    def rotate_z(self, data, draw, draw_size, center, angle):

        # getRotationMatrix2D関数を使用
        trans = data.cv2.getRotationMatrix2D(center, angle, 1.0)
        # アフィン変換
        draw = data.cv2.warpAffine(draw, trans, draw_size)

        return draw

    """

    def rotate_x(self, draw):
        return draw

    def rotate_y(self, draw):
        return draw

    """
