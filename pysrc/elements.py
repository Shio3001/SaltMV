# coding:utf-8
import sys
import numpy as np
import os
import copy
import datetime
import uuid


def make_id(memo):
    now_time = datetime.datetime.now()
    # new_id =
    new_id = "u"+str(uuid.uuid1()) + "t" + now_time.strftime('%y%m%H%M%S%f') + str(memo)
    return copy.deepcopy(new_id)


class AllElements:  # すごくえらい
    def __init__(self):
        self.scenes = {}
        self.now_scene = None
        print("全てのレイヤー管理 を追加しました : AllElements [ Elements ] ")


class SceneElements:  # えらい
    def __init__(self):
        self.layer_group = LayerElements()
        self.editor = {"x": 1280, "y": 720, "fps": 30, "len": 100, "sound_sampling_rate": 44100, "bpm": 0, "output_folder": "~/"}  # 動画の画面サイズとかその辺
        self.scene_id = make_id("scene")
        self.now_time = 0

        self.editor_select_int = ["x","y","fps","len","sound_sampling_rate","bpm"]
        self.editor_select_file = []
        self.editor_select_folder = ["output_folder"]

        print("各シーンのレイヤー管理 を追加しました : SceneElements [ Elements ] ")


class LayerElements:  # 次にえらい
    def __init__(self):
        self.object_group = {}    # objectID : [object,layerID]
        self.layer_layer_id = {}  # layerID  : layer番号

        print("レイヤーを追加しました : layerElements [ Elements ]")


class ObjectElements:  # その次にえらい
    def __init__(self):
        self.effect_group = {}
        self.installation = [0, 0]  # オブジェクト範囲
        self.synthetic = "normal"  # 合成方法
        self.obj_id = make_id("obj")
        self.effect_point_internal_id_time = {}

        print("オブジェクトを追加しました : ObjectElements [ Elements ]")


class EffectElements:  # えらくない
    def __init__(self):
        self.effect_name = None  # str(os.path.basename(__file__)).replace('.py', '')
        #self.effect_point = {}
        self.procedure = self.non_func  # インスタンス化したclassを詰め込む
        self.various_fixed = {}  # 固定設定
        self.effect_id = None
        self.effect_point_internal_id_point = {}
        self.cpp_file = ""

        self.audio = False
        #self.export_loop = True

        print("エフェクトを追加しました : effectElements [ Elements ]")

    def non_func(self):
        print("関数がありません")
