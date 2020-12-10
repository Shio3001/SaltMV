# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2


class CentralRole:

    # 揃え位置を取得し調整する

    def __init__(self):
        pass

    def video(self, this_object, now_frame, export_draw):
        # 一律中央ぞろえ

        # obj_property = this_object.
        new_video = this_object.document
        obj_property = this_object.unique_property

        # CV_CAP_PROP_POS_AVI_RATIO

        # print(obj_property)
        use_now_frame = now_frame - this_object.staend_property[0]
        #print("フレーム数 : " + str(use_now_frame))

        if use_now_frame >= obj_property["count"]:
            #print("時間外 : " + str(use_now_frame))
            new_video.set(cv2.CAP_PROP_POS_FRAMES, obj_property["count"] - 1)

        else:
            #print("時間内  - 正常")
            new_video.set(cv2.CAP_PROP_POS_FRAMES, use_now_frame)

        ret, draw_substantial = new_video.read()

        draw_substantial = cv2.cvtColor(draw_substantial.astype('uint8'), cv2.COLOR_BGR2RGBA)

        if ret:
            #print("読み込み成功 ret ")
            #print("読み込んだファイルの大きさ : " + str(draw_substantial.shape))
            pass

        if not ret:
            #print("読み込みに失敗 ret ")
            draw_substantial = export_draw

        return draw_substantial, obj_property

    def image(self, this_object, now_flame, export_draw):
        # 一律中央ぞろえ
        draw_substantial = this_object.document
        obj_property = this_object.unique_property
        #print("読み込んだファイルの大きさ : " + str(draw_substantial.shape))
        draw_substantial = cv2.cvtColor(draw_substantial, cv2.COLOR_BGR2RGBA)
        return draw_substantial, obj_property

    def text(self, this_object, now_flame, export_draw):
        # 任意選択制

        return draw_substantial, obj_property
