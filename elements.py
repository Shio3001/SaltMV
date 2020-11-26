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
        self.layer_cutout = None
        self.RetentionObject = []


class ObjectElements:
    # GUI
    def __init__(self):
        # self.DrawSetImg = DrawSetImg
        self.Document = []  # ファイルが入る
        self.Point = []  # 時間,x,y,size  #時間[x,y,a,size][間隔など、いろいろ]こっちの方がいいのでは
        self.Property = [None, None]  # 開始地点,終了地点
        self.ObjectType = 0
        self.UniqueProperty = []  # それぞれ任意 #ObjectTypeによって分別
