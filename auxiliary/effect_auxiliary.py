# coding:utf-8
import sys
import numpy
import os
import copy


class Calculation:
    # 第一引数に座標などが入って物を入れる, 第二引数にメディアデータのサイズを、第三引数にエディタのサイズを入れる
    def middle_change(self, coordinate, draw_size, editor_size):
        coordinate = (editor_size / 2) + coordinate - (draw_size / 2)
        return coordinate

    def upperleft_change(self):
        pass
