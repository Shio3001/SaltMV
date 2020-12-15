# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2

# オブジェクトのサイズを1/2したものを座標から引いて、でてきた座標に 640 , 360(これは画面サイズの半分)をたす
# ../Nankoku_Workspace/1211/927


class CentralRole:
    def __init__(self):
        pass

    def main(self, export_draw_base, all_elements, now_frame, operation_list, editor):  # フレームごとの処理

        # print(sys._getframe().f_code.co_name)
        substantial = operation_list["out"]["obj_substantial"]["CentralRole"]
        objectdict = {"video": substantial.video, "image": substantial.image, "text": substantial.text}

        export_draw = copy.deepcopy(export_draw_base)

        for this_layer in all_elements.layer_group:  # レイヤー
            print("対象レイヤー [ A ] : " + str(this_layer))
            export_draw = self.apply_layer(objectdict, this_layer, export_draw, operation_list, now_frame, editor)

        return export_draw

    # apply ・・・適用する
    def apply_layer(self, objectdict, this_layer, export_draw, operation_list, now_frame, editor):
        for this_object in this_layer.retention_object:  # ie = i_elementsの訳 #オブジェクト
            if this_object.staend_property[0] <= now_frame <= this_object.staend_property[1]:
                print("レイヤー : 出力対象フレーム")
                export_draw = self.apply_object(objectdict, this_object, export_draw, operation_list, now_frame, editor)
                continue

            else:
                print("レイヤー : 除外フレーム")
        return export_draw

    def apply_object(self, objectdict, this_object, export_draw, operation_list, now_frame, editor):
        # print(sys._getframe().f_code.co_name)
        # 位置以外の、オブジェクト生成はここでやれ

        if not this_object.objectType:
            return export_draw

        draw_substantial, obj_property = objectdict[this_object.objectType](this_object, now_frame, export_draw)

        adjusted_draw = copy.deepcopy(draw_substantial)

        del draw_substantial

        starting_point = []

        for this_effect in this_object.effects:  # エフェクト
            print(this_effect.effectPoint)

            for i in range(len(this_effect.effectPoint)):
                this_effect.effectPoint[i]["time"] += this_object.staend_property[0]
                print("時系列加算")

            print(this_effect.effectPoint)
            print(this_effect.procedure)
            adjusted_draw, starting_point = self.apply_effect(objectdict, this_effect, adjusted_draw, operation_list, now_frame, editor)

        starting_point = list(map(int, starting_point))

        under = [0, 0]

        for i in range(2):
            if starting_point[i] < 0:
                under[i] = int(abs(0 - starting_point[i]))
                starting_point[i] = 0
        adjusted_draw = adjusted_draw[under[1]:, under[0]:, :]
        draw_size = (adjusted_draw.shape[1], adjusted_draw.shape[0])

        draw_range = [int(draw_size[i]) if starting_point[i] + draw_size[i] <= editor[i] else int(editor[i] - starting_point[i]) for i in range(2)]
        print("描画範囲 : " + str(draw_range))
        print("開始地点 : " + str(starting_point))

        # if starting_point > editor

        # んでオブジェクトとエフェクトの合算処理
        draw = self.normal_synthetic(export_draw, adjusted_draw, starting_point, draw_range)

        del adjusted_draw
        return draw

    def apply_effect(self, objectdict, this_effect, adjusted_draw, operation_list, now_frame, editor):
        # print(sys._getframe().f_code.co_name)

        # 前のやつと等しいか、前野より高かったら取得して
        # その次のやつも取得する

        this_point = this_effect.effectPoint
        this_point_number = 0
        print("座標計算開始" + str(this_point))
        point_count = int(len(this_point))
        for i in range(point_count):
            if now_frame >= this_point[i]["time"]:
                this_point_number = i
                print(this_point_number)
                break

        around_point = [{}, {}]
        around_point[0] = this_point[this_point_number]
        if this_point_number == point_count - 1:
            around_point[1] = copy.deepcopy(around_point[0])
            around_point[1]["time"] += 1
        else:
            around_point[1] = this_point[this_point_number + 1]  # 次の地点、に戻すために一をたす

        print("前後の地点 : " + str(around_point))

        whereabouts = {str(j): operation_list["out"]["current_location"]["CentralRole"].main((around_point[0]["time"], around_point[1]["time"]),
                                                                                             (around_point[0][str(j)], around_point[1][str(j)]), now_frame) for j in list(around_point[0].keys()) if j != "time"}
        print(whereabouts)

        print(this_effect)

        draw_operation = operation_list["other"]["effect_auxiliary"]["Calculation"]

        adjusted_draw, starting_point = this_effect.procedure.main(adjusted_draw, whereabouts, now_frame, editor, draw_operation)

        # ここに処理を描く adjusted_draw - > adjusted_draw

        return adjusted_draw, starting_point

    def normal_synthetic(self, export_draw, adjusted_draw, starting_point, draw_range):
        # print("通常合成")

        # スライスで+1しないでいい理由・・・numpyでの画像は0 ~ 1279でやってるから
        # 1 ~ 1280なら + 1しないといけない

        adjusted_range = adjusted_draw[0:draw_range[1], 0:draw_range[0], :]

        print(starting_point, draw_range)

        export_range = export_draw[starting_point[1]:starting_point[1] + draw_range[1], starting_point[0]:starting_point[0] + draw_range[0], :]

        for i in range(3):
            adjusted_range[:, :, i] = (adjusted_range[:, :, i] - export_range[:, :, i]) * (adjusted_range[:, :, 3] / 255)
        export_range[:, :, 0:3] += adjusted_range[:, :, 0:3]
        # 確定色 = 背景色 + (重ねる色 - 背景色) * (アルファ値 / 255)

        print(export_range.shape)

        export_draw[starting_point[1]:starting_point[1] + draw_range[1], starting_point[0]:starting_point[0] + draw_range[0], :] = export_range
        return export_draw
