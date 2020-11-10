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
        self.fntSize = None
        self.WritingDirection = 0  # 書字方向 #初期値横書き
        self.CharacterSpacing = 0  # 初期値 -で狭める、+で広げる
        self.TextIndividualObject = True  # 文字毎に個別オブジェクト

    def Main(self, layer, EditSize, NumberLayer):

        print("生成したいテキストを入力 [ 文字列 ]")
        self.NewTextString = str(sys.stdin.readline().rstrip())  # 入力させる

        print("フォントサイズを入力 [ 数値 ]")
        try:
            self.fntSize = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("横書き [ 0 ] 縦書き [ 1 ] を入力 [ 数値 ]")
        try:
            self.WritingDirection = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("文字間隔 を入力 [ 数値 ]")
        try:
            self.CharacterSpacing = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        AddText = []

        for imakeImge in range(len(self.NewTextString)):

            print(str(imakeImge) + "文字目の処理")

            try:
                SetImg = Image.new(
                    "RGBA", (self.fntSize, self.fntSize), (0, 0, 0, 0))
            except:
                return "Det"
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

        # print(layer[NumberLayer].Document)
        #layer[NumberLayer].Point[:][4] = self.fntSize
        layer[NumberLayer].Document = AddText

        #layer[NumberLayer].Point[:][4] = self.fntSize

        layer[NumberLayer].UniqueProperty = [
            self.WritingDirection, self.CharacterSpacing, self.TextIndividualObject, self.fntSize]  # 書字方向, 文字間隔 ,文字毎に個別オブジェクト , フォントサイズの順に設定
        return layer
