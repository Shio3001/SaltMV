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
        self.GetEditTextsMember = [None, None]
        # self.AddText = []

        # self.WritingDirection = 0  # 書字方向 #初期値横書き
        # self.TextSpacing  # 初期値 -で狭める、+で広げる
        # self.TextIndividualObject = True  # 文字毎に個別オブジェクト

    def Main(self, layer, EditSize, ilayerloop):
        # CUI化で消滅
        # fntSizeは定数 拡大縮小は基本pointのsizeからやること

        layer[ilayerloop].UniqueProperty = TextElements()
        layer[ilayerloop].Document = []

        TextSpacing = 0  # 仮設置 pointクラス化工事が終了した次第に削除するように

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
            # layer[ilayerloop].UniqueProperty.TextSpacing = int(sys.stdin.readline().rstrip())
            TextSpacing = int(sys.stdin.readline().rstrip())
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

        layer = self.Main_Control(layer, EditSize, ilayerloop)

        # layer[ilayerloop].Point[:].update({"TextSpacing": TextSpacing})
        # layer[ilayerloop].Point = map(lambda x: x.extend({"TextSpacing": TextSpacing}), layer[ilayerloop].Point)

        # print(type(layer[ilayerloop].Point[0]))
        # print(layer[ilayerloop].Point[0])

        for i, ic in enumerate(layer[ilayerloop].Point):
            layer[ilayerloop].Point[i] = {**layer[ilayerloop].Point[i], "TextSetting": {"TextSpace": TextSpacing}}

        return layer

    def Main_Control(self, layer, EditSize, ilayerloop):
        layer[ilayerloop].Document = [0] * int(len(self.NewTextString))

        layer[ilayerloop].UniqueProperty.NewTextString = self.NewTextString

        print(self.addfntSize)

        # for imakeImge, item_ic in enumerate(layer[ilayerloop].Document):
        # print("A" + str(len(layer[ilayerloop].Document)))
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

    def EditTexts_Main(self, layer, EditSize, ilayerloop):

        EditNewText = ""
        print("新しい文字列を入力 変更しないなら空白で [ 文字列 ]")

        try:
            EditNewText = int(sys.stdin.readline().rstrip())
            print(EditNewText)
        except:
            print("空白を検知")

        if int(len(EditNewText)) != 0:
            layer[ilayerloop].UniqueProperty.NewTextString = EditNewText

        print("文字列を取得")
        print(str(layer[ilayerloop].UniqueProperty.NewTextString))
        print("文字数" + str(int(len(layer[ilayerloop].UniqueProperty.NewTextString)) - 1))
        print("選択可能範囲" + " 0 から" + str(int(len(layer[ilayerloop].UniqueProperty.NewTextString))))

        EditTexts_fntSize = self.addfntSize

        # self.GetEditTextsMember = None

        for i in range(2):
            print("変更したいテキスト開始地点を入力[ 数値 ] (もしくは [ ALL ] 全て選択できます)")
            try:
                self.GetEditTextsMember[i] = str(sys.stdin.readline().rstrip())

                if "ALL" in self.GetEditTextsMember:
                    self.GetEditTextsMember = [0, int(len(layer[ilayerloop].UniqueProperty.NewTextString)) - 1]
                    break

            except:
                return "Det"

        # self.GetEditTextsMember = map(lambda x: int(x), self.GetEditTextsMember)

        EditTexts_Status = ""
        while EditTexts_Status != "Det":
            EditTexts_Status = self.EditTexts_Operation(layer, EditSize, ilayerloop, self.GetEditTextsMember, EditTexts_fntSize)
            if EditTexts_Status != "Det":
                layer = EditTexts_Status
                break

        return layer

    def EditTexts_Operation(self, layer, EditSize, ilayerloop, GetEditTextsMemberr, EditTexts_fntSize):
        print("次の動作を入力 [ 番号 ] もしくは [ 文字列 ]")
        NextChoiceList = {1: "exit", 2: "size"}
        print(NextChoiceList)

        AskNextAction = str(sys.stdin.readline().rstrip())
        if AskNextAction == NextChoiceList[1] or AskNextAction == "1":
            return layer

        if AskNextAction == NextChoiceList[2] or AskNextAction == "2":
            AskDi = self.EditTexts_Size(layer, EditSize, ilayerloop, GetEditTextsMemberr, EditTexts_fntSize)
            if AskDi == "Det":
                print("問題あり")
                return "Det"
            else:
                layer = AskDi

        return layer

    def EditTexts_Size(self, layer, EditSize, ilayerloop, GetEditTextsMember, EditTexts_fntSize):

        print("変更後のフォントサイズを入力 [数値]")
        print("現在:" + str(EditTexts_fntSize))
        EditTexts_AfterSize = int(sys.stdin.readline().rstrip())

        print("挿入方式 置き換え:[ 0 ] 加算:[ 1 ]")
        EditTexts_CalculationSize = int(sys.stdin.readline().rstrip())

        NumberOfCalculations = int(GetEditTextsMember[1]) - int(GetEditTextsMember[0]) + 1
        print("計算回数" + str(NumberOfCalculations))

        for i in range(NumberOfCalculations):

            iEdit = i + int(GetEditTextsMember[0])
            print(iEdit)

            if EditTexts_CalculationSize == 0:
                EditTexts_fntSize[iEdit] = EditTexts_AfterSize
            if EditTexts_CalculationSize == 1:
                EditTexts_fntSize[iEdit] += EditTexts_AfterSize

            self.addfntSize[iEdit] = EditTexts_fntSize[iEdit]

        print(EditTexts_fntSize)
        layer = self.Main_Control(layer, EditSize, ilayerloop)
        return layer

    def TextDrawingGeneration(self, Draw_addfntSize, imakeImge, NewTextString):

        try:
            SetImg = Image.new("RGBA", (Draw_addfntSize[imakeImge], Draw_addfntSize[imakeImge]), (0, 0, 0, 0))

        except:
            return "Det"
        DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る

        fnt = ImageFont.truetype('logotypejp_mp_b_1.1.ttf', Draw_addfntSize[imakeImge])  # ImageFontインスタンスを作る
        # fontを指定
        DrawSetImg.text((0, 0), NewTextString[imakeImge], font=fnt)
        InTextDrawSetImg = numpy.array(SetImg)
        return InTextDrawSetImg

    def Textconcatenation(self, Document, UniqueProperty):
        print("テキストの連結処理")

        AddText_concatenation = Document[0].TextInformation

        for ic, item_ic in enumerate(Document):

            if int(ic) + 1 < int(len(Document)):
                # 基本連結 #lenで取得できるのはあくまで[要素数]であって配列番号ではないことから、<=ではなく <になっている
                DifferenceSize = UniqueProperty.Maxfnt - Document[ic + 1].TextSize

                if UniqueProperty.WritingDirection == 0:
                    AdditionalBlank = numpy.zeros((UniqueProperty.Maxfnt, UniqueProperty.TextSpacing, 4))  # テキスト間の空白を入力
                    if DifferenceSize != 0:
                        AddDifference = numpy.zeros((DifferenceSize, Document[ic + 1].TextSize, 4))
                        Document[ic + 1].TextInformation = numpy.vstack((AddDifference, Document[ic + 1].TextInformation))  # 縦に連結

                    AddText_concatenation = numpy.hstack((AddText_concatenation, AdditionalBlank))
                    AddText_concatenation = numpy.hstack((AddText_concatenation, Document[ic + 1].TextInformation))

                if UniqueProperty.WritingDirection == 1:
                    AdditionalBlank = numpy.zeros((UniqueProperty.TextSpacing, UniqueProperty.Maxfnt, 4))  # テキスト間の空白を入力
                    if DifferenceSize != 0:
                        AddDifference = numpy.zeros((Document[ic + 1].TextSize, DifferenceSize, 4))
                        Document[ic + 1].TextInformation = numpy.hstack((Document[ic + 1].TextInformation, AddDifference))  # 横に連結

                    AddText_concatenation = numpy.vstack((AddText_concatenation, AdditionalBlank))
                    AddText_concatenation = numpy.vstack((AddText_concatenation, Document[ic + 1].TextInformation))
        return AddText_concatenation


class UniqueText:
    def __init__(self):
        self.TextInformation = []  # テキストの画像での情報(ただし配列)
        self.TextSize = 0  # テキストサイズ


class TextElements:  # (TEXT定数)
    def __init__(self):
        self.TextSpacing = 0  # テキスト間隔 初期値 -で狭める、+で広げる
        self.WritingDirection = 0  # 書字方向 #初期値横書き
        self.AlignmentPosition = [1, 1]  # 揃え位置を図る奴 0が左・上 1が真ん中 2が右・下
        self.IndividualObject = 0  # 個別に管理するか
        self.Maxfnt = 0  # 一番でかい文字サイズ
        self.NewTextString = ""  # 文字列
