# coding:utf-8
import sys
import os
import copy
import cv2
import numpy as np
# 削除厳禁！
# coding:utf-8
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import numpy as np


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effect_point = {"rotate_z": 0, "rotate_center_x": 0, "rotate_center_y": 0}
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        # 第一引数にself, 第二引数にメディアデータ、第三引数に居場所、第四引数に現在のフレーム, 第五引数にエディタ情報, 操作一覧

    def main(self, rendering_main_data):
        draw_size = tuple(map(int, rendering_main_data.draw_size.values()))
        center = (draw_size[0] / 2 + rendering_main_data.effect_value["rotate_center_x"], draw_size[1] / 2 + rendering_main_data.effect_value["rotate_center_y"])

        angle = rendering_main_data.effect_value["rotate_z"]
        PILdraw = Image.fromarray(rendering_main_data.draw)  # ImageTkフォーマットへ変換
        PILdraw = self.rotate_z(PILdraw, center, angle)

        rendering_main_data.draw = np.array(PILdraw, dtype=np.uint8)

        return "DRAW", rendering_main_data.draw, self.starting_point

    def rotate_z(self, PILdraw, center, angle):

        PILdraw2 = PILdraw.rotate(angle, expand=True, center=center)
        return PILdraw2

    def rotate_x(self, draw):
        return draw

    def rotate_y(self, draw):
        return draw
