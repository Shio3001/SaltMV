# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2

# オブジェクトのサイズを1/2したものを座標から引いて、でてきた座標に 640 , 360(これは画面サイズの半分)をたす


class CentralRole:
    def __init__(self):
        pass

    def main(self, export_draw_base, all_elements, now_frame, operation_list):  # フレームごとの処理

        # print(sys._getframe().f_code.co_name)
        substantial = operation_list["out"]["obj_substantial"]["CentralRole"]
        objectdict = {"video": substantial.video, "image": substantial.image, "text": substantial.text}

        export_draw = copy.deepcopy(export_draw_base)

        for this_layer in all_elements.layer_group:  # レイヤー
            print("対象レイヤー [ A ] : " + str(this_layer))
            export_draw = self.apply_layer(objectdict, this_layer, export_draw, operation_list, now_frame)

        return export_draw

    # apply ・・・適用する
    def apply_layer(self, objectdict, this_layer, export_draw, operation_list, now_frame):
        for this_object in this_layer.retention_object:  # ie = i_elementsの訳 #オブジェクト
            if this_object.staend_property[0] <= now_frame <= this_object.staend_property[1]:
                print("レイヤー : 出力対象フレーム")
                export_draw = self.apply_object(objectdict, this_object, export_draw, operation_list, now_frame)
                continue

            else:
                print("レイヤー : 除外フレーム")
        return export_draw

    def apply_object(self, objectdict, this_object, export_draw, operation_list, now_frame):
        # print(sys._getframe().f_code.co_name)
        # 位置以外の、オブジェクト生成はここでやれ

        if not this_object.objectType:
            return export_draw

        draw_substantial, obj_property = objectdict[this_object.objectType](this_object, now_frame, export_draw)

        adjusted_draw = copy.deepcopy(draw_substantial)

        # for this_effect in this_object.effects:  # エフェクト
        adjusted_draw = [self.apply_effect(objectdict, this_effect, draw_substantial, operation_list, now_frame) for this_effect in this_object.effects]

        # んでオブジェクトとエフェクトの合算処理
        draw = self.normal_synthetic(export_draw, adjusted_draw)
        return draw

    def apply_effect(self, objectdict, this_effect, draw_substantial, operation_list, now_frame):
        # print(sys._getframe().f_code.co_name)

        whereabouts = 0

        #departure_point = this_point.index(this_point >= now_frame) - 1

        around_point = [None, None]

        around_point[0] = list(filter(lambda x: x["time"] <= now_frame, this_effect.effectPoint))[0]
        print("前の地点 : " + str(around_point[0]))

        around_point[1] = list(filter(lambda x: x["time"] < now_frame and x["time"] < around_point[0]["time"], this_effect.effectPoint))[0]
        print("次の地点 : " + str(around_point[1]))

        #operation_list["out"]["current_location"]["CentralRole"].main(around_point, now_frame)

        # for i, ie in enumerate(this_effect.effectPoint):
        # for j, this_point in enumerate(ie[1:].values()):
        #this_time = this_point["time"]
        #this_effect.effectPoint[i][ie[j].keys()] = operation_list["out"]["current_location"]["CentralRole"].main(this_time, this_point, now_frame)

        adjusted_draw = draw_substantial

        return adjusted_draw

    def normal_synthetic(self, export_draw, adjusted_draw):
        # print("通常合成")

        for i in range(3):
            adjusted_draw[:, :, i] = (adjusted_draw[:, :, i] - export_draw[:, :, i]) * (adjusted_draw[:, :, 3] / 255)

        export_draw[:, :, 0:3] += adjusted_draw[:, :, 0:3]
        # 確定色 = 背景色 + (重ねる色 - 背景色) * (アルファ値 / 255)
        return export_draw
