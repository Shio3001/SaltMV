# coding:utf-8
import sys
import numpy as np
import os
import copy


class AllElements:  # えらい
    def __init__(self):
        self.scenes = []
        print("全てのレイヤー管理 を追加しました : AllElements [ Elements ] ")


class SceneElements:  # えらい
    def __init__(self):
        self.layer_group = []  # 一番重要だと思われ
        self.editor = {"x": 1280, "y": 720, "fps": 30, "len": 100}  # 動画の画面サイズとかその辺
        #self.user_select_range = [0, 100]

        print("各シーンのレイヤー管理 を追加しました : SceneElements [ Elements ] ")


class LayerElements:  # 次にえらい
    def __init__(self):
        self.object_group = []

        print("レイヤーを追加しました : layerElements [ Elements ]")


class ObjectElements:  # その次にえらい
    def __init__(self):
        self.effect_group = []
        self.installation = [0, 0]  # オブジェクト範囲
        self.synthetic = "normal"  # 合成方法

        print("オブジェクトを追加しました : ObjectElements [ Elements ]")


class EffectElements:  # えらくない
    def __init__(self):
        self.effect_name = None
        self.effect_point = []
        self.procedure = self.non_func  # インスタンス化したclassを詰め込む
        self.various_fixed = {}  # 固定設定
        #self.export_loop = True

        print("エフェクトを追加しました : effectElements [ Elements ]")

    def non_func(self):
        print("関数がありません")
