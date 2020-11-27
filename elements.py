# coding:utf-8
import sys
import numpy as np
import os
import copy


class AllElements:
    def __init__(self):
        self.layer_group = []  # 一番重要だと思われ
        self.editor_info = []  # 動画の画面サイズとかその辺


class layerElements:
    def __init__(self):
        self.layer_cutout = None  # クリップングするか否か しばらく使わないでしょ
        self.retention_object = []


class ObjectElements:
    # GUI
    def __init__(self):
        # self.DrawSetImg = DrawSetImg
        self.document = []  # ファイルが入る
        self.point = []  # 時間,x,y,size  #時間[x,y,a,size][間隔など、いろいろ]こっちの方がいいのでは
        self.staend_property = [None, None]  # 開始地点,終了地点
        self.objectType = 0
        self.unique_property = []  # それぞれ任意 #ObjectTypeによって分別
