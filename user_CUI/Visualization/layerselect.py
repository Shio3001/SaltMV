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
                if 1 <= int(user_select) <= len(layer_group):
                    print("問題なし")
                    return int(user_select) - 1  # ユーザーからみたら1からだけど中身は0からだから1だけ引くんだぞ
                else:
                    user_select = -1
            except:
                print("問題あり" + str(sys.exc_info()))
                user_select = -1

    def object(self, object_group):
        user_select = -1

        while user_select == -1:
            print("オブジェクトを選択してください [ 1 から ] [ 数値 ]")
            user_select = str(sys.stdin.readline().rstrip())

            try:
                if 1 <= int(user_select) <= len(object_group):
                    print("問題なし")
                    return int(user_select) - 1  # ユーザーからみたら1からだけど中身は0からだから1だけ引くんだぞ
                else:
                    user_select = -1
            except:
                print("問題あり" + str(sys.exc_info()))
                user_select = -1
