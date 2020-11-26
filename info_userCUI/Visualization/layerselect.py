# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def __init__(self):
        pass

    def layer(self, layer_group):

        user_select = -1

        while user_select == -1:
            print("レイヤーを選択してください [ 1 から ] [ 数値 ]")
            user_select = str(sys.stdin.readline().rstrip())

            try:
                if 1 <= int(user_select) <= layer_group.shape[0]:
                    print("問題なし")
                    return int(user_select)
            except:
                print("問題あり")
                user_select = -1

    def object(self, layer_group):
        pass
