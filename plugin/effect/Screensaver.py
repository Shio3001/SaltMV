# coding:utf-8
import sys
import numpy
import os
import copy


class InitialValue:
    def __init__(self):
        pass

    def main(self, elements):
        setting_effect = elements.effectElements()
        setting_effect.effectname = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effectPoint = [{"time": 0, "speed": 1}]
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()

        return setting_effect


class CentralRole:
    def __init__(self):

        self.direction = [1, 1]
        self.starting_point = [0, 0]
        print("設定方向 : " + str(os.path.basename(__file__)).replace('.py', ''))

        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に画面サイズ情報, 第五引数に現在のフレームが入ってくる

    def main(self, draw, whereabouts, now_frame, editor, draw_operation):

        editor_size = {"x": editor[0], "y": editor[1]}
        draw_size = {"x": draw.shape[1], "y": draw.shape[0]}
        speed = whereabouts["speed"]

        direction_range = [list(editor_size.values())[i] / 2 - list(draw_size.values())[i] / 2 for i in range(2)]

        print(direction_range)

        # self.direction =

        print("方向A : " + str(self.direction))
        print(self.starting_point)

        for j in range(2):
            if -1 * direction_range[j] < speed + self.direction[j] + self.starting_point[j] < direction_range[j]:
                pass
            else:
                self.direction[j] *= -1

        print("方向B : " + str(self.direction))

        #self.starting_point = [x + y for x, y in zip(self.starting_point, self.direction)]
        self.starting_point = [self.starting_point[m] + self.direction[m] for m in range(2)]
        send_starting_point = [draw_operation.middle_change(self.starting_point[k], list(draw_size.values())[k], list(editor_size.values())[k]) for k in range(2)]

        print("仮座標決定 : " + str(send_starting_point))
        return draw, send_starting_point
