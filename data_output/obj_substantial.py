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

    def video(self, this_objct, now_frame, export_draw):
        # 一律中央ぞろえ
        new_video = ""
        try:
            new_video = cv2.VideoCapture(this_objct.document)
        except:
            print("読み込みに失敗 try - except")

        if new_video.isOpened() != True:
            print("読み込みに失敗 isOpened")

        obj_property = {"width": new_video.get(cv2.CAP_PROP_FRAME_WIDTH), "height": new_video.get(cv2.CAP_PROP_FRAME_HEIGHT), "fps": new_video.get(cv2.CAP_PROP_FPS), "count": new_video.get(cv2.CAP_PROP_FRAME_COUNT)}

        # CV_CAP_PROP_POS_AVI_RATIO

        print(obj_property)
        use_now_frame = now_frame - this_objct.staend_property[0]
        print("フレーム数 : " + str(use_now_frame))

        if use_now_frame >= obj_property["count"]:
            print("時間外です : " + str(use_now_frame))
            new_video.set(cv2.CAP_PROP_POS_FRAMES, obj_property["count"] - 1)

        else:
            print("時間内、正常です")
            new_video.set(cv2.CAP_PROP_POS_FRAMES, use_now_frame)

        ret, draw_substantial = new_video.read()

        if ret:
            print("読み込み成功 ret ")
            print("読み込んだファイルの大きさ : " + str(draw_substantial.shape))

        if not ret:
            print("読み込みに失敗 ret ")
            draw_substantial = export_draw

        return draw_substantial, obj_property

    def image(self, this_objct, now_flame, export_draw):
        # 一律中央ぞろえ

        return draw_substantial, obj_property

    def text(self, this_objct, now_flame, export_draw):
        # 任意選択制

        return draw_substantial, obj_property
