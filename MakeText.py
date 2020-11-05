# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

#input = sys.stdin.readline
import PrintLayers
import SelectLayer


class MakeTexts:
    def __init__(self):
        self.SetSelectLayer = SelectLayer.SelectLayer()
        self.NewTextString = None

    def Main(self, layer, EditSize):

        print("レイヤーを選択")
        NumberLayer = self.SetSelectLayer.Main(layer)
        if NumberLayer == "Det":
            return "Det"

        print("生成したいテキストを入力")
        self.NewTextString = str(sys.stdin.readline().rstrip())  # 入力させる

        for imakeImge in range(len(self.NewTextString)):
            print(str(imakeImge) + "文字目の処理")
            SetImg = Image.new(
                "RGBA", (EditSize[0], EditSize[1]), (0, 0, 0, 0))
            DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る

            fntSize = 30
            fnt = ImageFont.truetype(
                'logotypejp_mp_b_1.1.ttf', fntSize)  # ImageFontインスタンスを作る
            # fontを指定
            DrawSetImg.text((imakeImge * fntSize, 0),
                            self.NewTextString[imakeImge], font=fnt)
            print("座標" + str(imakeImge * fntSize))
            InTextDrawSetImg = numpy.array(SetImg)
            # print(layer)
            layer[NumberLayer].Document.append(InTextDrawSetImg)

        # print(layer[NumberLayer].Document)
        return layer
