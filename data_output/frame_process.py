# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2


class CentralRole:
    def __init__(self):
        pass

    def main(self, export_draw_base, all_elements, now_frame, operation_list):  # フレームごとの処理
        print(sys._getframe().f_code.co_name)
        substantial = operation_list["out"]["obj_substantial"]["CentralRole"]
        objectdict = {"video": substantial.video, "image": substantial.image, "text": substantial.text}

        export_draw = copy.deepcopy(export_draw_base)

        for this_layer in all_elements.layer_group:  # レイヤー
            print("対象レイヤー [ A ] : " + str(this_layer))
            export_draw = self.apply_layer(objectdict, this_layer, export_draw, now_frame)

        return export_draw

    # apply ・・・適用する
    def apply_layer(self, objectdict, this_layer, export_draw, now_frame):
        for this_object in this_layer.retention_object:  # ie = i_elementsの訳 #オブジェクト
            if this_object.staend_property[0] <= now_frame <= this_object.staend_property[1]:
                print("レイヤー : 出力対象フレーム")
                export_draw = self.apply_object(objectdict, this_object, export_draw, now_frame)
                continue

            else:
                print("レイヤー : 除外フレーム")
        return export_draw

    def apply_object(self, objectdict, this_object, export_draw, now_frame):
        print(sys._getframe().f_code.co_name)

        print("対象オブジェクト [ C ] : " + str(this_object))

        # 位置以外の、オブジェクト生成はここでやれ

        draw_substantial, obj_property = objectdict[this_object.objectType](this_object, now_frame, export_draw)

        for this_effect in this_object.effects:  # エフェクト
            adjusted_draw = self.apply_effect(objectdict, this_effect, draw_substantial, now_frame)

        # んでオブジェクトとエフェクトの合算処理

        # 通常合成

        export_draw = adjusted_draw

        return export_draw

    def apply_effect(self, objectdict, this_effect, draw_substantial, now_frame):
        print(sys._getframe().f_code.co_name)

        adjusted_draw = draw_substantial

        return adjusted_draw
