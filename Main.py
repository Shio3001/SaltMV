# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import Organize
import Export
import EditSize
import SetPoints
import NewObject
import PrintLayers


# input = sys.stdin.readline().rstrip()

# layer[各レイヤー][レイヤ,メディアファイル,[POINT,POINT,POINT,POINT,POINT].....]


# layer
# 一次元目：各レイヤー
# 二次元目：レイヤー,メディアファイル,POINT
# 三次元目(POINTのみ):たくさんのPOINT
# 四次元目(POINTのみ):Time x y size

print("=======================")
print("")
print("")
print("   動画いじれるやつ")
print("      Shio3001")
print("    2020 10月制作開始")
print("    2020 11月版")
print("")
print("")
print("=======================")


class layerElements:
    # GUI
    def __init__(self):
        # self.DrawSetImg = DrawSetImg
        self.Document = []
        self.Point = []  # 時間,x,y,size  #時間[x,y,a,size][間隔など、いろいろ]こっちの方がいいのでは
        self.ObjectType = "NotSet"
        self.Property = [None, None]  # これが何を意味するか,開始地点,終了地点
        self.UniqueProperty = []  # それぞれ任意


class Center:  # 中心的な役割になる、はず
    # CUI化で消滅
    def __init__(self):
        self.layer = []
        self.EditSize = [0, 0, 0, 0]
        # self.Point = [0, 0, 0, 0, 0]  # Time , X , Y ,Z ,Size

    def NextChoice(self):
        print("次の動作を入力 [ 番号 ] もしくは [ 文字列 ]")
        NextChoiceList = {1: "exit", 2: "NewLayer", 3: "SetEditeSize", 4: "CountLayer", 5: "ExportMove",
                          6: "NewObject", 7: "SetPoints", 8: "EditPoints", 9: "OrganizePoints", 10: ""}
        print(NextChoiceList)

        AskNextAction = sys.stdin.readline().rstrip()
        if AskNextAction == NextChoiceList[1] or AskNextAction == "1":
            return "exit"

        if AskNextAction == NextChoiceList[2] or AskNextAction == "2":

            """
            SetImg = Image.new(
                "RGBA", (self.EditSize[0], self.EditSize[1]), (0, 0, 0, 0))
            DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る

            self.layer.append(layerElements([DrawSetImg]))

            """
            self.layer.append(layerElements())
            # self.layer.append([DrawSetImg, None, []])

            print("レイヤー数:" + str(len(self.layer)))
            layer_Printer.ReturnPrint(self.layer)

        if AskNextAction == NextChoiceList[3] or AskNextAction == "3":

            CHK = SetSuperSetEditSize.SetEditSize()
            if CHK == "EXC":
                print("入力に問題あり")

            else:
                self.EditSize = CHK
                print(self.EditSize)

        if AskNextAction == NextChoiceList[4] or AskNextAction == "4":
            print("レイヤー数:" + str(len(self.layer)))
            layer_Printer.ReturnPrint(self.layer)
            print("")

        if AskNextAction == NextChoiceList[5] or AskNextAction == "5":
            print("動画書き出し")

            CHK = MovImgsExport.Main(self.layer, self.EditSize)

            if CHK == "EXC":
                print("問題あり")
                return
            else:
                self.layer == CHK

        if AskNextAction == NextChoiceList[6] or AskNextAction == "6":
            print("オブジェクトの追加")

            CHK = New_MakeObject.MakeObjectCenter(self.layer, self.EditSize)
            if CHK == "EXC":
                print("問題あり")
                return
            else:
                self.layer = CHK

        if AskNextAction == NextChoiceList[7] or AskNextAction == "7":
            print("オブジェクトの移動・透明度変更などを行います [ 新規作成 ]")

            AddOREdit = 0
            CHK = Set_MakePoint.Main(self.layer, AddOREdit)
            if CHK == "EXC":
                print("問題あり")
                return
            else:
                self.layer = CHK

        if AskNextAction == NextChoiceList[8] or AskNextAction == "8":
            print("オブジェクトの移動・透明度変更などを行います [ 変更 ]")

            AddOREdit = 1
            CHK = Set_MakePoint.Main(self.layer, AddOREdit)
            if CHK == "EXC":
                print("問題あり")
                return
            else:
                self.layer = CHK

        if AskNextAction == NextChoiceList[9] or AskNextAction == "9":
            print("レイヤーの中にあるPoint設定を時間順に並び替えます")

            layer_Printer.ReturnPrint(self.layer)

            CHK, self.EditSize = ArrayOrganize.PointOrganize(self.layer, self.EditSize)

            if CHK == "EXC":
                print("問題あり")
                return
            else:

                self.layer = CHK
                layer_Printer.ReturnPrint(self.layer)


Main_Center = Center()
SetSuperSetEditSize = EditSize.SuperSetEditSize()
New_MakeObject = NewObject.MakeObject()
Set_MakePoint = SetPoints.MakePoints()
MovImgsExport = Export.Export_Center()
ArrayOrganize = Organize.ArrayOrganize()
layer_Printer = PrintLayers.PrintMain()

ReturnDecision = ""
while ReturnDecision != "exit":
    ReturnDecision = Main_Center.NextChoice()  # この関数のところで"exit"returnしたら終了するようにしてる

print("通常終了")
sys.exit()
