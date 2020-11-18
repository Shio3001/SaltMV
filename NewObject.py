# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import SelectLayer
import PrintLayers
import MakeText
import SelectColor

from MakeText_Edit import EditData
from MakeText_Edit import MakeText_Edit_Main
from MakeText_Edit import MakeText_Edit_Size
from MakeText_Edit import MakeText_Edit_Color
from MakeText_Edit import MakeText_Calculation

# ここから各オブジェクトを追加するのを書く
# 一番えらい

#input = sys.stdin.readline


class MakeObject:
    def __init__(self):
        self.SetSelectLayer = SelectLayer.SelectLayer()
        self.Set_MakeText = MakeText.MakeTexts()

        self.Set_MakeEditText_EditData = EditData.EditDataElement()
        self.Set_MakeEditText_Main = MakeText_Edit_Main.MakeEditMain()
        self.Set_MakeEditText_Size = MakeText_Edit_Size.MakeEditSize()
        self.Set_MakeEditText_Color = MakeText_Edit_Color.MakeEditColor()
        self.Set_MakeEditText_Calculation = MakeText_Calculation.MakeText_Cal()

        self.NumberLayer = 0
        self.AskDi = None
        self.EditMode = False  # 既存のものを編集(true)か新規作成か(false)

    def MakeObjectCenter(self, layer, EditSize):
        # CUI化で消滅
        self.NumberLayer = self.SetSelectLayer.Main(layer)
        if self.NumberLayer == "Det":
            return "Det"

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
            addNewMov = []
            print("動画ファイルを入力...")
            os.system("pwd")
            os.system("ls")
            inp_in = str(sys.stdin.readline().rstrip())
            NewObjct = cv2.VideoCapture(inp_in)

            while NewObjct.isOpened():
                ret, inputData = NewObjct.read()
                if ret == True:
                    cv2.cvtColor(inputData, cv2.COLOR_RGB2RGBA)

                    addNewMov.append(inputData)

                    # 現在いるフレームを送信
                    cv2.imshow('input now', inputData)

                    if cv2.waitKey(1):
                        print("読み込み")

                    # break

                elif len(addNewMov) == NewObjct.get(cv2.CAP_PROP_FRAME_COUNT):
                    layer[self.NumberLayer].Document = addNewMov
                    NewObjct.release()
                    cv2.destroyAllWindows()
                    print("読み込みに成功")

                    layer[self.NumberLayer].ObjectType = "1"
                    layer[self.NumberLayer].Property = [0, 100]

                    return layer

                else:
                    print("ファイルが正常に入力できませんでした：終了")
                    NewObjct.release()
                    cv2.destroyAllWindows()
                    return "Det"
                    # break

        if ObjectType == "3":
            print("テキストを入力")

            if EditSize[0] == 0 or EditSize[1] == 0:
                print("画面サイズが設定されていません,もしくは [ 0 ]に設定されています")
                return "Det"

            layer[self.NumberLayer].ObjectType = "3"
            layer[self.NumberLayer].Property = [0, 100]

            EditData.EditDataElement().SetImport_Text(self.Set_MakeEditText_Main, self.Set_MakeEditText_Size, self.Set_MakeEditText_Color, self.Set_MakeEditText_Calculation)

            if len(layer) != 0:

                if self.EditMode == True:
                    self.AskDi = self.Set_MakeEditText_Main.EditTexts_Main(layer, EditSize, self.NumberLayer, SelectColor.SelectColor_Center(), self.Set_MakeEditText_EditData)
                else:
                    self.AskDi = self.Set_MakeText.Main(layer, EditSize, self.NumberLayer)

                if self.AskDi == "Det":
                    print("問題あり")
                    return "Det"
                else:
                    layer = self.AskDi
                    return layer
            else:
                print("レイヤーがありません")
                return layer

        return "Det"
