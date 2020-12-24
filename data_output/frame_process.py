# coding:utf-8
import sys
import os
import copy
import numpy as np
import cv2

# オブジェクトのサイズを1/2したものを座標から引いて、でてきた座標に 640 , 360(これは画面サイズの半分)をたす


class CentralRole:
    def __init__(self):
        pass

    def main(self, export_draw_base, all_elements, now_frame, operation_list, editor):  # フレームごとの処理

        # print(sys._getframe().f_code.co_name)
        substantial = operation_list["out"]["obj_substantial"]["CentralRole"]
        objectdict = {"video": substantial.video, "image": substantial.image, "text": substantial.text}

        export_draw = copy.deepcopy(export_draw_base)

        for this_layer in all_elements.layer_group:  # レイヤー
            export_draw = self.apply_layer(objectdict, this_layer, export_draw, operation_list, now_frame, editor)

        return export_draw

    # apply ・・・適用する
    def apply_layer(self, objectdict, this_layer, export_draw, operation_list, now_frame, editor):
        for this_object in this_layer.retention_object:  # ie = i_elementsの訳 #オブジェクト
            if this_object.staend_property[0] <= now_frame <= this_object.staend_property[1]:
                export_draw = self.apply_object(objectdict, this_object, export_draw, operation_list, now_frame, editor, this_object.staend_property)
                continue

            else:
                pass
        return export_draw

    def apply_object(self, objectdict, this_object, export_draw, operation_list, now_frame, editor, staend_property):
        # print(sys._getframe().f_code.co_name)
        # 位置以外の、オブジェクト生成はここでやれ

        if not this_object.objectType:
            return export_draw

        draw_substantial, obj_property = objectdict[this_object.objectType](this_object, now_frame, export_draw)

        adjusted_draw = copy.deepcopy(draw_substantial)

        del draw_substantial

        starting_point = [0, 0]

        draw_operation = operation_list["useful"]["effect_auxiliary"]["Calculation"]

        for this_effect in this_object.effects:  # エフェクト

            for i in range(len(this_effect.effectPoint)):
                this_effect.effectPoint[i]["time"] += this_object.staend_property[0]  # 時系列加算

            adjusted_draw, new_starting_point = self.apply_effect(objectdict, this_effect, adjusted_draw, operation_list, now_frame, editor, draw_operation, staend_property)
            starting_point = [x + y for (x, y) in zip(starting_point, new_starting_point)]  # 新しいのと古いのを混ぜる

        editor_size = [editor[0], editor[1]]
        draw_size = [adjusted_draw.shape[1], adjusted_draw.shape[0]]
        starting_point = [draw_operation.middle_change(starting_point[i], draw_size[i], editor_size[i]) for i in range(2)]

        starting_point = list(map(int, starting_point))

        under = [0, 0]

        for i in range(2):
            if starting_point[i] < 0:
                under[i] = int(abs(0 - starting_point[i]))
                starting_point[i] = 0
        adjusted_draw = adjusted_draw[under[1]:, under[0]:, :]
        draw_size = (adjusted_draw.shape[1], adjusted_draw.shape[0])

        if 0 in draw_size:
            return export_draw

        draw_range = [int(draw_size[i]) if starting_point[i] + draw_size[i] <= editor[i] else int(editor[i] - starting_point[i]) for i in range(2)]

        if 0 != int(len([i for i in draw_range if i <= 0])):
            return export_draw

        # if starting_point > editor

        # んでオブジェクトとエフェクトの合算処理
        draw = self.normal_synthetic(export_draw, adjusted_draw, starting_point, draw_range)

        del adjusted_draw
        return draw

    def apply_effect(self, objectdict, this_effect, adjusted_draw, operation_list, now_frame, editor, draw_operation, staend_property):
        # print(sys._getframe().f_code.co_name)

        # 前のやつと等しいか、前野より高かったら取得して
        # その次のやつも取得する

        this_point = this_effect.effectPoint
        this_point_number = 0
        point_count = int(len(this_point))
        for i in range(point_count):
            if now_frame >= this_point[i]["time"]:
                this_point_number = i
                break

        around_point = [{}, {}]
        around_point[0] = this_point[this_point_number]
        if this_point_number == point_count - 1:
            around_point[1] = copy.deepcopy(around_point[0])
            around_point[1]["time"] += 1
        else:
            around_point[1] = this_point[this_point_number + 1]  # 次の地点、に戻すために一をたす

        starting_point = [0, 0]

        loop_this_effect = copy.deepcopy(this_effect)

        if loop_this_effect.export_loop is True:
            for loop_now_frame in range(staend_property[0], now_frame + 1):
                adjusted_draw, starting_point = self.loop_effect(operation_list, loop_this_effect, adjusted_draw, loop_now_frame, editor, draw_operation, staend_property, around_point)

        if loop_this_effect.export_loop is False:
            adjusted_draw, starting_point = self.loop_effect(operation_list, loop_this_effect, adjusted_draw, now_frame, editor, draw_operation, staend_property, around_point)

        del loop_this_effect

        adjusted_draw = adjusted_draw.astype('uint8')

        #adjusted_draw, starting_point = this_effect.procedure.main(adjusted_draw, position, now_frame, editor, draw_operation)

        # ここに処理を描く adjusted_draw - > adjusted_draw

        return adjusted_draw, starting_point

    def loop_effect(self, operation_list, loop_this_effect, adjusted_draw, now_frame, editor, draw_operation, staend_property, around_point):
        position = {str(j): operation_list["out"]["current_location"]["CentralRole"].main((around_point[0]["time"], around_point[1]["time"]),
                                                                                          (around_point[0][str(j)], around_point[1][str(j)]), now_frame) for j in list(around_point[0].keys()) if j != "time"}

        data = pluginElements(adjusted_draw, position, now_frame, editor, draw_operation, staend_property)
        adjusted_draw, starting_point = loop_this_effect.procedure.main(data)
        del data

        return adjusted_draw, starting_point

    def normal_synthetic(self, export_draw, adjusted_draw, starting_point, draw_range):
        # print("通常合成")

        # スライスで+1しないでいい理由・・・numpyでの画像は0 ~ 1279でやってるから
        # 1 ~ 1280なら + 1しないといけない

        change_end = [starting_point[i] + draw_range[i] for i in range(2)]

        adjusted_range = adjusted_draw[0:draw_range[1], 0:draw_range[0], :]

        export_range = export_draw[starting_point[1]:change_end[1], starting_point[0]:change_end[0], :]

        for i in range(3):
            adjusted_range[:, :, i] = (adjusted_range[:, :, i] - export_range[:, :, i]) * (adjusted_range[:, :, 3] / 255)
            # a = (重ねる色 - 背景色) * (アルファ値 / 255)
        export_range[:, :, 0:3] += adjusted_range[:, :, 0:3]
        # 確定色 = 背景色 + a
        # 確定色 = 背景色 + (重ねる色 - 背景色) * (アルファ値 / 255)

        export_draw[starting_point[1]:change_end[1], starting_point[0]:change_end[0], :] = export_range
        return export_draw


class pluginElements:
    def __init__(self, adjusted_draw, position, now_frame, editor, draw_operation, staend_property):
        self.draw = adjusted_draw
        self.position = position
        self.now_frame = now_frame
        self.editor = editor
        self.draw_operation = draw_operation

        self.editor_size = {"x": self.editor[0], "y": self.editor[1]}
        self.draw_size = {"x": self.draw.shape[1], "y": self.draw.shape[0]}
        self.staend_property = staend_property

        self.cv2 = cv2
        self.np = np
