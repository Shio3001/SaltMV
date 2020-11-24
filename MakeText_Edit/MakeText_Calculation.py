# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

# 一番えらくない 一番した


class MakeText_Cal:
    def Main_Control(self, layer, EditSize, ilayerloop, RGBdata, addfntSize, NewTextString):
        layer[ilayerloop].Document = [0] * int(len(NewTextString))

        layer[ilayerloop].UniqueProperty.NewTextString = NewTextString

        # for imakeImge, item_ic in enumerate(layer[ilayerloop].Document):
        # print("A" + str(len(layer[ilayerloop].Document)))
        for imakeImge, item_ic in enumerate(layer[ilayerloop].Document):
            # layer[ilayerloop].Document.append()
            layer[ilayerloop].Document[imakeImge] = UniqueText()
            layer[ilayerloop].Document[imakeImge].TextInformation = numpy.array(self.TextDrawingGeneration(addfntSize, imakeImge, NewTextString, RGBdata))
            layer[ilayerloop].Document[imakeImge].TextSize = addfntSize[imakeImge]

        layer[ilayerloop].UniqueProperty.Maxfnt = max(addfntSize)
        layer[ilayerloop].UniqueProperty.MaxfntIndex = addfntSize.index(max(addfntSize))
        # もし個別オブジェクトでない場合は配列の合成を行う

        if layer[ilayerloop].UniqueProperty.IndividualObject == 0:
            layer[ilayerloop].Document[0].TextInformation = numpy.array(self.Textconcatenation(layer[ilayerloop].Document, layer[ilayerloop].UniqueProperty))
            layer[ilayerloop].Document[0].TextSize = layer[ilayerloop].UniqueProperty.Maxfnt

            del layer[ilayerloop].Document[1:]

        return layer

    def TextDrawingGeneration(self, Draw_addfntSize, imakeImge, NewTextString, RGBdata):

        try:
            SetImg = Image.new("RGBA", (Draw_addfntSize[imakeImge], Draw_addfntSize[imakeImge]), (0, 0, 0, 0))

        except:
            return "EXC"
        DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る

        fnt = ImageFont.truetype('logotypejp_mp_b_1.1.ttf', Draw_addfntSize[imakeImge])  # ImageFontインスタンスを作る
        # fontを指定
        DrawSetImg.text((0, 0), NewTextString[imakeImge], tuple(reversed(RGBdata[imakeImge])), font=fnt)
        InTextDrawSetImg = numpy.array(SetImg)
        return InTextDrawSetImg

    def Textconcatenation(self, Document, UniqueProperty):
        print("テキストの連結処理")

        DifferenceSize0 = UniqueProperty.Maxfnt - Document[0].TextSize

        if UniqueProperty.WritingDirection == 0:
            if DifferenceSize0 != 0:
                AddDifference = numpy.zeros((DifferenceSize0, Document[0].TextSize, 4))
                Document[0].TextInformation = numpy.vstack((AddDifference, Document[0].TextInformation))  # 縦に連結

        if UniqueProperty.WritingDirection == 1:
            if DifferenceSize0 != 0:
                AddDifference = numpy.zeros((DifferenceSize0, Document[0].TextSize, 4))
                Document[0].TextInformation = numpy.hstack((Document[0].TextInformation, AddDifference))  # 縦に連結

        AddText_concatenation = Document[0].TextInformation

        for ic, item_ic in enumerate(Document):

            if int(ic) + 1 < int(len(Document)):
                # 基本連結 #lenで取得できるのはあくまで[要素数]であって配列番号ではないことから、<=ではなく <になっている
                DifferenceSize = UniqueProperty.Maxfnt - Document[ic + 1].TextSize
                if UniqueProperty.WritingDirection == 0:

                    if DifferenceSize != 0:
                        AddDifference = numpy.zeros((DifferenceSize, Document[ic + 1].TextSize, 4))
                        Document[ic + 1].TextInformation = numpy.vstack((AddDifference, Document[ic + 1].TextInformation))  # 縦に連結
                    if UniqueProperty.TextSpacing != 0:
                        AdditionalBlank = numpy.zeros((UniqueProperty.Maxfnt, UniqueProperty.TextSpacing, 4))  # テキスト間の空白を入力
                        AddText_concatenation = numpy.hstack((AddText_concatenation, AdditionalBlank))

                        print("連結処理")
                    AddText_concatenation = numpy.hstack((AddText_concatenation, Document[ic + 1].TextInformation))

                if UniqueProperty.WritingDirection == 1:

                    if DifferenceSize != 0:
                        AddDifference = numpy.zeros((Document[ic + 1].TextSize, DifferenceSize, 4))
                        Document[ic + 1].TextInformation = numpy.hstack((Document[ic + 1].TextInformation, AddDifference))  # 横に連結

                    if UniqueProperty.TextSpacing != 0:
                        AdditionalBlank = numpy.zeros((UniqueProperty.TextSpacing, UniqueProperty.Maxfnt, 4))  # テキスト間の空白を入力
                        AddText_concatenation = numpy.vstack((AddText_concatenation, AdditionalBlank))

                    AddText_concatenation = numpy.vstack((AddText_concatenation, Document[ic + 1].TextInformation))
        return AddText_concatenation


class UniqueText:
    def __init__(self):
        self.TextInformation = []  # テキストの画像での情報(ただし配列)
        self.TextSize = 0  # テキストサイズ
