# coding:utf-8
import sys
import numpy as np
import os
import copy


class AllElements:  # えらい
    def __init__(self):
        self.layer_group = []  # 一番重要だと思われ
        self.editor_info = []  # 動画の画面サイズとかその辺

        print("全てのレイヤー管理 を追加しました : AllElements [ Elements ] ")


class layerElements:  # 次にえらい
    def __init__(self):
        self.layer_cutout = None  # クリップングするか否か しばらく使わないでしょ
        self.retention_object = []

        print("レイヤーを追加しました : layerElements [ Elements ]")


class ObjectElements:  # その次にえらい
    # GUI
    def __init__(self):
        # self.DrawSetImg = DrawSetImg
        self.document = []  # ファイルが入る
        # self.point = [{}]  # 時間,x,y,size  #時間[x,y,a,size][間隔など、いろいろ]こっちの方がいいのでは
        self.staend_property = [None, None]  # 開始地点,終了地点
        self.objectType = None
        self.unique_property = []  # それぞれ任意 #ObjectTypeによって分別
        self.effects = []

        print("オブジェクトを追加しました : ObjectElements [ Elements ]")


class effectElements:  # えらくない
    def __init__(self):
        #basic : 座標など
        #color : 色に関すること
        #text : テキストなど
        self.effectname = None
        self.effectPoint = []
        self.procedurelist = None  # インスタンス化したclassを詰め込む

        print("エフェクトを追加しました : effectElements [ Elements ]")
