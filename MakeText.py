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
        self.fntSize = 34

    def Main(self, layer, EditSize):

        print("レイヤーを選択")
        NumberLayer = self.SetSelectLayer.Main(layer)
        if NumberLayer == "Det":
            return "Det"

        print("生成したいテキストを入力")
        self.NewTextString = str(sys.stdin.readline().rstrip())  # 入力させる

        print("フォントサイズを入力")
        try:
            self.fntSize = int(sys.stdin.readline().rstrip())
        except:
            "Det"

        AddText = []

        for imakeImge in range(len(self.NewTextString)):

            print(str(imakeImge) + "文字目の処理")
            SetImg = Image.new(
                "RGBA", (self.fntSize, self.fntSize), (0, 0, 0, 0))
            DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る

            fnt = ImageFont.truetype(
                'logotypejp_mp_b_1.1.ttf', self.fntSize)  # ImageFontインスタンスを作る
            # fontを指定
            DrawSetImg.text((0, 0),
                            self.NewTextString[imakeImge], font=fnt)
            #print("座標" + str(0))
            InTextDrawSetImg = numpy.array(SetImg)
            # print(layer)
            AddText.append(InTextDrawSetImg)

            testoutput101 = Image.fromarray(InTextDrawSetImg)
            testoutput101.save('EncodeTest/EncodeTest101.png')

        # print(layer[NumberLayer].Document)
        #layer[NumberLayer].Point[:][4] = self.fntSize
        layer[NumberLayer].Document = AddText
        return layer
