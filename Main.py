# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import Encode
import EditSize

import SetPoints

import NewObject

#input = sys.stdin.readline().rstrip()

print("=======================")
print("")
print("")
print("   動画いじれるやつ")
print("      Shio3001")
print("    2020 10月制作")
print("")
print("")
print("=======================")


class Center:  # 中心的な役割になる、はず
    def __init__(self):
        self.layer = []
        self.EditSize = [0, 0]
        # self.Point = [0, 0, 0, 0, 0]  # Time , X , Y ,Z ,Size

    def NextChoice(self):
        print("次の動作を入力 [ 番号 ] もしくは [ 文字列 ]")
        NextChoiceList = {1: "exit", 2: "NewLayer",
                          3: "SetEditeSize", 4: "CountLayer", 5: "EncodeMove", 6: "NewObject", 7: "SetPoints", 8: "EditPoints"}
        print(NextChoiceList)

        AskNextAction = sys.stdin.readline().rstrip()
        if AskNextAction == NextChoiceList[1] or AskNextAction == "1":
            return "exit"

        elif AskNextAction == NextChoiceList[2] or AskNextAction == "2":
            SetImg = Image.new(
                "RGBA", (self.EditSize[0], self.EditSize[1]), (0, 0, 0, 0))
            DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る

            self.layer.append([DrawSetImg])

            print("レイヤー数:" + str(len(self.layer)))
            print(self.layer)

        elif AskNextAction == NextChoiceList[3] or AskNextAction == "3":

            AskDi = SetSuperSetEditSize.SetEditSize()
            if AskDi == "Det":
                print("入力に問題あり")

            else:
                self.EditSize = AskDi
                print(self.EditSize)

        elif AskNextAction == NextChoiceList[4] or AskNextAction == "4":
            print("レイヤー数:" + str(len(self.layer)))
            print(self.layer)

        elif AskNextAction == NextChoiceList[5] or AskNextAction == "5":
            print("動画エンコード")

        elif AskNextAction == NextChoiceList[6] or AskNextAction == "6":
            print("オブジェクトの追加")
            if len(self.layer) != 0:
                AskDi = New_MakeObject.MakeObjectCenter(self.layer)
                if AskDi == "Det":
                    print("問題あり")
                    return
                else:
                    self.layer == AskDi

            else:
                print("レイヤーがありません")
                return

        elif AskNextAction == NextChoiceList[7] or AskNextAction == "7":
            print("オブジェクトの移動・透明度変更などを行います [ 新規作成 ]")
            if len(self.layer) != 0:
                AddOREdit = 0
                AskDi = Set_MakePoint.Main(self.layer, AddOREdit)
                if AskDi == "Det":
                    print("問題あり")
                    return
                else:
                    self.layer == AskDi

            else:
                print("レイヤーがありません")
                return

        elif AskNextAction == NextChoiceList[8] or AskNextAction == "8":
            print("オブジェクトの移動・透明度変更などを行います [ 変更 ]")
            if len(self.layer) != 0:
                AddOREdit = 1
                AskDi = Set_MakePoint.Main(self.layer, AddOREdit)
                if AskDi == "Det":
                    print("問題あり")
                    return
                else:
                    self.layer == AskDi

            else:
                print("レイヤーがありません")
                return


Main_Center = Center()
SetSuperSetEditSize = EditSize.SuperSetEditSize()
New_MakeObject = NewObject.MakeObject()

Set_MakePoint = SetPoints.MakePoints()


ReturnDecision = ""
while ReturnDecision != "exit":
    ReturnDecision = Main_Center.NextChoice()  # この関数のところで"exit"returnしたら終了するようにしてる

print("通常終了")
sys.exit()
