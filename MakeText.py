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
        # self.AddText = []

        # self.WritingDirection = 0  # 書字方向 #初期値横書き
        # self.TextSpacing  # 初期値 -で狭める、+で広げる
        # self.TextIndividualObject = True  # 文字毎に個別オブジェクト

    def Main(self, layer, EditSize, ilayerloop):

        # fntSizeは定数 拡大縮小は基本pointのsizeからやること

        layer[ilayerloop].UniqueProperty = TextElements()
        layer[ilayerloop].Document = []

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
            layer[ilayerloop].UniqueProperty.WritingDirection = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("文字間隔 を入力 [ 数値 ]")
        try:
            layer[ilayerloop].UniqueProperty.TextSpacing = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("[左右]揃え位置を入力 左揃え [ 0 ] 中揃え [ 1 ] 右揃え [ 2 ] [ 数値 ]")
        try:
            layer[ilayerloop].UniqueProperty.AlignmentPosition[0] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("[上下]揃え位置を入力 上揃え [ 0 ] 中揃え [ 1 ] 下揃え [ 2 ] [ 数値 ]")
        try:
            layer[ilayerloop].UniqueProperty.AlignmentPosition[1] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("個別オブジェクトにするかしないかを入力 しない [ 0 ] する [ 1 ] ")
        try:
            layer[ilayerloop].UniqueProperty.IndividualObject = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        layer[ilayerloop].Document = [0] * int(len(self.NewTextString))

        # for imakeImge, item_ic in enumerate(layer[ilayerloop].Document):
        #print("A" + str(len(layer[ilayerloop].Document)))
        for imakeImge, item_ic in enumerate(layer[ilayerloop].Document):
            # layer[ilayerloop].Document.append()
            layer[ilayerloop].Document[imakeImge] = UniqueText()
            layer[ilayerloop].Document[imakeImge].TextInformation = self.TextDrawingGeneration(self.addfntSize, imakeImge, self.NewTextString)
            layer[ilayerloop].Document[imakeImge].TextSize = self.addfntSize[imakeImge]

        layer[ilayerloop].UniqueProperty.Maxfnt = max(self.addfntSize)

        # もし個別オブジェクトでない場合は配列の合成を行う

        if layer[ilayerloop].UniqueProperty.IndividualObject == 0:
            layer[ilayerloop].Document[0].TextInformation = self.Textconcatenation(layer[ilayerloop].Document, layer[ilayerloop].UniqueProperty)
            layer[ilayerloop].Document[0].TextSize = layer[ilayerloop].UniqueProperty.Maxfnt

            del layer[ilayerloop].Document[1:]
        return layer

    def TextDrawingGeneration(self, addfntSize, imakeImge, NewTextString):

        try:
            SetImg = Image.new("RGBA", (addfntSize[imakeImge], addfntSize[imakeImge]), (0, 0, 0, 0))

        except:
            return "Det"
        DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る

        fnt = ImageFont.truetype('logotypejp_mp_b_1.1.ttf', addfntSize[imakeImge])  # ImageFontインスタンスを作る
        # fontを指定
        DrawSetImg.text((0, 0), NewTextString[imakeImge], font=fnt)
        InTextDrawSetImg = numpy.array(SetImg)
        return InTextDrawSetImg

    def Textconcatenation(self, Document, UniqueProperty):
        print("テキストの連結処理")

        AddText_concatenation = Document[0].TextInformation

        for ic, item_ic in enumerate(Document):

            AdditionalBlank = numpy.zeros((Document[ic].TextSize, UniqueProperty.Maxfnt, 4))

            AddDifference = numpy.zeros((Document[ic].TextSize, UniqueProperty.Maxfnt - Document[ic].TextSize, 4))

            # 基本連結 #lenで取得できるのはあくまで[要素数]であって配列番号ではないことから、<=ではなく <になっている
            if int(ic) + 1 < int(len(Document)) and UniqueProperty.WritingDirection == 0:
                if int(len(AddDifference[0])) != 0:
                    AddText_concatenation = numpy.vstack((AdditionalBlank, AddDifference))
                AddText_concatenation = numpy.hstack((AddText_concatenation, AdditionalBlank))
                AddText_concatenation = numpy.hstack((AddText_concatenation, Document[ic + 1].TextInformation))

            if int(ic) + 1 < int(len(Document)) and UniqueProperty.WritingDirection == 1:
                if int(len(AddDifference[0])) != 0:
                    AddText_concatenation = numpy.hstack((AdditionalBlank, AddDifference))
                AddText_concatenation = numpy.vstack((AddText_concatenation, AdditionalBlank))
                AddText_concatenation = numpy.vstack((AddText_concatenation, Document[ic + 1].TextInformation))
        return AddText_concatenation


class UniqueText:
    def __init__(self):
        self.TextInformation = []
        self.TextSize = 0


class TextElements:
    def __init__(self):
        self.TextSpacing = 0  # テキスト間隔 初期値 -で狭める、+で広げる
        self.WritingDirection = 0  # 書字方向 #初期値横書き
        self.AlignmentPosition = [1, 1]  # 揃え位置を図る奴 0が左・上 1が真ん中 2が右・下
        self.IndividualObject = 0  # 個別に管理するか
        self.Maxfnt = 0
        # self.fntSize = []  # フォントサイズ 前との文字との間隔を表すため テキスト数-1にしろ
