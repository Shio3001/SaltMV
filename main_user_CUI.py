# coding:utf-8
import sys
import numpy
import os
import copy

# GUI処分ファイル(CUI中継)


class Center:
    def __init__(self):
        pass

    def UserNextSelect(self, layer_group, elements, userCUI_rally_Center):
        print("次の動作を入力 [ 番号 ] もしくは [ 文字列 ]")

        hold_layer_group = copy.deepcopy(layer_group)  # 問題があった時にはこれを返すようにすればいい
        user_select = str(sys.stdin.readline().rstrip())

        if user_select == "0":  # 終了
            sys.exit()

        if user_select == "1":  # 保存
            return layer_group

        if user_select == "2":  # レイヤー生成
            print("レイヤー生成")
            layer_group.append(elements.layerElements())
            userCUI_rally_Center.printlayer_Center.viaLayer(layer_group)
            return layer_group

        if user_select == "3":  # オブジェクト生成
            return layer_group

        return hold_layer_group
