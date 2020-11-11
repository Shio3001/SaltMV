# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

# input = sys.stdin.readline
import PrintLayers
import SelectLayer


class MakeTexts:
    def __init__(self):
        self.SetSelectLayer = SelectLayer.SelectLayer()
        self.NewTextString = None  # 生成するてきすと
        self.fntSize = None  # Pointスキップ方法に基づきNone
        self.addfntSize = []

        # self.WritingDirection = 0  # 書字方向 #初期値横書き
        # self.TextSpacing  # 初期値 -で狭める、+で広げる
        # self.TextIndividualObject = True  # 文字毎に個別オブジェクト

    def Main(self, layer, EditSize, NumberLayer):

        # fntSizeは定数 拡大縮小は基本pointのsizeからやること

        layer[NumberLayer].UniqueProperty = TextElements()

        print("生成したいテキストを入力 [ 文字列 ]")
        self.NewTextString = str(sys.stdin.readline().rstrip())  # 入力させる

        print("フォントサイズを入力 [ 数値 ]")
        try:
            # self.fntSize.append(int(sys.stdin.readline().rstrip()))
            self.addfntSize = [int(sys.stdin.readline().rstrip())] * len(self.NewTextString)
        except:
            return "Det"

        print("横書き [ 0 ] 縦書き [ 1 ] を入力 [ 数値 ]")
        try:
            layer[NumberLayer].UniqueProperty.WritingDirection = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("文字間隔 を入力 [ 数値 ]")
        try:
            layer[NumberLayer].UniqueProperty.TextSpacing = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("揃え位置を入力 上揃え [ 0 ] 中揃え [ 1 ] 右揃え [ 2 ] [ 数値 ]")
        try:
            layer[NumberLayer].UniqueProperty.AlignmentPosition = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("個別オブジェクトにするかしないかを入力 しない [ 0 ] する [ 1 ] ")
        try:
            layer[NumberLayer].UniqueProperty.IndividualObject = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        AddText = []

        for imakeImge in range(len(self.NewTextString)):

            print(str(imakeImge) + "文字目の処理")

            try:
                SetImg = Image.new(
                    "RGBA", (self.addfntSize[imakeImge], self.addfntSize[imakeImge]), (0, 0, 0, 0))
            except:
                return "Det"
            DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る

            fnt = ImageFont.truetype(
                'logotypejp_mp_b_1.1.ttf', self.addfntSize[imakeImge])  # ImageFontインスタンスを作る
            # fontを指定
            DrawSetImg.text((0, 0),
                            self.NewTextString[imakeImge], font=fnt)
            # print("座標" + str(0))
            InTextDrawSetImg = numpy.array(SetImg)
            AddText.append([InTextDrawSetImg, self.addfntSize[imakeImge]])
            # print(layer)

        # もし個別オブジェクトでない場合は配列の合成を行う
        if layer[NumberLayer].UniqueProperty.IndividualObject == 0:
            AddText = [[self.Textconcatenation(AddText, layer[NumberLayer].UniqueProperty)]]

        layer[NumberLayer].Document = AddText

        return layer

    def Textconcatenation(self, AddText, UniqueProperty):
        print("テキストの連結処理")

        AddText_concatenation = AddText[0][0]

        for ic, item_ic in enumerate(AddText):

            AdditionalBlank = numpy.zeros((AddText[ic][1], AddText[ic][1], 4))

            # 基本連結 #lenで取得できるのはあくまで[要素数]であって配列番号ではないことから、<=ではなく <になっている
            if int(ic) + 1 < int(len(AddText)) and UniqueProperty.WritingDirection == 0:
                AddText_concatenation = numpy.hstack((AddText_concatenation, AdditionalBlank))
                AddText_concatenation = numpy.hstack((AddText_concatenation, AddText[ic + 1][0]))

            if int(ic) + 1 < int(len(AddText)) and UniqueProperty.WritingDirection == 1:
                AddText_concatenation = numpy.vstack((AddText_concatenation, AdditionalBlank))
                AddText_concatenation = numpy.vstack((AddText_concatenation, AddText[ic + 1][0]))
        return AddText_concatenation


class TextElements:
    def __init__(self):
        self.TextSpacing = 0  # テキスト間隔 初期値 -で狭める、+で広げる
        self.WritingDirection = 0  # 書字方向 #初期値横書き
        self.AlignmentPosition = 1  # 揃え位置を図る奴 0が左 1が真ん中 2が右
        self.IndividualObject = 0  # 個別に管理するか
        # self.fntSize = []  # フォントサイズ 前との文字との間隔を表すため テキスト数-1にしろ
