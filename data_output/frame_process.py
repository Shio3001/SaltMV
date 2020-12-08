# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2


class CentralRole:
    def __init__(self):
        pass

    def main(self, export_draw, all_elements, now_frame, operation_list):  # フレームごとの処理

        objectdict = {"video": self.video, "image": self.image, "text": self.text}

        for this_objct in all_elements.retention_object:
            export_draw = objectdict[this_objct.objectType](this_objct, export_draw)

        return export_draw

    def video(self, this_objct, export_draw):
        # 一律中央ぞろえ

        return export_draw

    def image(self, this_objct, export_draw):
        # 一律中央ぞろえ

        return export_draw

    def text(self, this_objct, export_draw):
        # 任意選択制

        return export_draw
