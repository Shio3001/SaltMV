# coding:utf-8
import sys
import os
import copy
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import numpy as np
# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effect_point = {"letter_spacing": 0, "R": 255, "G": 255, "B": 255, "X": 0, "Y": 0, "size": 10}
        setting_effect.various_fixed = {"text": "", "placement_width": 0, "placement_height": 0, "path": ""}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]

    def main(self, rendering_main_data):

        dsx = rendering_main_data.draw_size["x"]
        dsy = rendering_main_data.draw_size["y"]

        path = rendering_main_data.various_fixed["path"]
        text = rendering_main_data.various_fixed["text"]
        R = int(rendering_main_data.effect_value["R"])
        G = int(rendering_main_data.effect_value["G"])
        B = int(rendering_main_data.effect_value["B"])
        X = int(rendering_main_data.effect_value["X"] + dsx / 2)
        Y = int(rendering_main_data.effect_value["Y"] + dsy / 2)
        size = int(rendering_main_data.effect_value["size"])

        im = Image.new("RGBA", (dsx, dsy), (R, G, B, 0))  # Imageインスタンスを作る
        draw_pillow = ImageDraw.Draw(im)  # im上のImageDrawインスタンスを作る

        font = ImageFont.truetype(path, size)
        draw_pillow.text((X, Y), text, (R, G, B), font=font, anchor='mm')

        rendering_main_data.draw = np.array(im, dtype=np.uint8)

        print(rendering_main_data.draw.shape)

        return rendering_main_data.draw, self.starting_point
