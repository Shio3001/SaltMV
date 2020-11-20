# coding:utf-8
import sys
import numpy
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import SelectLayer
import PrintLayers
import MakeText
import SelectColor

from ImportFile import ImportMove
from ImportFile import ImportImage

from MakeText_Edit import EditData
from MakeText_Edit import MakeText_Edit_Main
from MakeText_Edit import MakeText_Edit_Size
from MakeText_Edit import MakeText_Edit_Color
from MakeText_Edit import MakeText_Calculation

# ここから各オブジェクトを追加するのを書く
# 一番えらい

# input = sys.stdin.readline


class MakeObject:
    def __init__(self):
        self.SetSelectLayer = SelectLayer.SelectLayer()
        self.Set_MakeText = MakeText.MakeTexts()

        self.EditData_Ope = None
        self.EditData_Info = None

        # self.Set_MakeEditText_EditData_Operation = EditData.EditDataElement_Operation()
        # self.Set_MakeEditText_EditData_Information = EditData.EditDataElement_Information()
        self.Set_MakeEditText_Main = MakeText_Edit_Main.MakeEditMain()
        self.Set_MakeEditText_Size = MakeText_Edit_Size.MakeEditSize()
        self.Set_MakeEditText_Color = MakeText_Edit_Color.MakeEditColor()
        self.Set_MakeEditText_Calculation = MakeText_Calculation.MakeText_Cal()

        self.NumberLayer = 0
        self.CHK = None
        self.EditMode = False  # 既存のものを編集(true)か新規作成か(false)

    def MakeObjectCenter(self, layer, EditSize):

        if int(len(layer)) == 0:  # レイヤーがなかった時に跳ね返す
            return "EXC"

        # CUI化で消滅
        self.NumberLayer = self.SetSelectLayer.Main(layer)
        if self.NumberLayer == "EXC":
            return "EXC"

        ObjectType = ""

        if layer[self.NumberLayer].ObjectType == "NotSet":
            self.EditMode = False
            print("[ 読み込み ]")

            print("種類を選択 [ 番号 ]")
            print("1:動画")
            print("2:")
            print("3:テキスト")
            print("4:")
            ObjectType = str(sys.stdin.readline().rstrip())
        else:
            self.EditMode = True
            ObjectType = layer[self.NumberLayer].ObjectType
            print("編集モード")

        if ObjectType == "1":
            self.CHK = ImportMove.ImportMove_Main().Move_Main(layer, self.NumberLayer)
            if self.CHK == "EXC":
                return "EXC"
            else:
                layer = self.CHK

            return layer

        if ObjectType == "2":
            self.CHK = ImportImage.ImportImage_Main().Image_Main(layer, self.NumberLayer)
            if self.CHK == "EXC":
                return "EXC"
            else:
                layer = self.CHK

            return layer

        if ObjectType == "3":
            print("テキストを入力")

            if EditSize[0] == 0 or EditSize[1] == 0:
                print("画面サイズが設定されていません,もしくは [ 0 ]に設定されています")
                return "EXC"

            layer[self.NumberLayer].ObjectType = "3"
            layer[self.NumberLayer].Property = [0, 100]

            self.EditData_Ope = EditData.EditDataElement_Operation(self.Set_MakeEditText_Main, self.Set_MakeEditText_Size, self.Set_MakeEditText_Color, self.Set_MakeEditText_Calculation)

            if len(layer) != 0:

                AsEditData_Info = None

                if self.EditMode == True:
                    self.CHK, AsEditData_Info = self.Set_MakeEditText_Main.EditTexts_Main(layer, EditSize, self.NumberLayer, SelectColor.SelectColor_Center(), self.EditData_Ope, self.EditData_Info)
                else:

                    self.CHK, AsEditData_Info = self.Set_MakeText.Main(layer, EditSize, self.NumberLayer,  EditData, self.EditData_Ope)
                    # self.CHK = EditData_Ope.Import_Main.Main(layer, EditSize, self.NumberLayer,  EditData, EditData_Ope)

                if self.CHK == "EXC":
                    print("問題あり")
                    return "EXC"
                else:
                    layer = self.CHK
                    self.EditData_Info = AsEditData_Info
                    return layer
            else:
                print("レイヤーがありません")
                return layer

        return "EXC"
