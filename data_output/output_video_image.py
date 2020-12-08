# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2


class Center:
    def __init__(self):
        pass

    def type_video(self, all_elements, operation_list, user_select):  # 動画で出力
        editor = all_elements.editor_info
        fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)
        size = (editor[0], editor[2])
        writer = cv2.VideoWriter(user_select, fmt, editor[2], size)  # ライター作成

        for now_frame in range(editor[3]):
            pass

    def type_image(self, all_elements, operation_list, select_time, user_select):  # 画像で出力
        pass
