# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import MakeText

print("=======================")
print("")
print("")
print("    動画いじれるやつ      ")
print("      Shio3001")
print("")
print("")
print("=======================")


class Center:  # 中心的な役割になる、はず
    def __init__(self):
        self.layer = []
        self.EditSize = [0, 0]

    def SetEditSize(self):
        print("動画の縦横サイズを入力してください[X,Y]")

        print("[ 横幅 ] を入力")

        try:
            self.EditSize[0] = round(int(input()))
        except:
            return "Det"

        print("[ 高さ ] を入力")

        try:
            self.EditSize[1] = round(int(input()))
        except:
            return "Det"

        print("入力終了 " + "横 : " +
              str(self.EditSize[0]) + " 高 : " + str(self.EditSize[1]))
        return "safe"

    def NextChoice(self):
        print("次の動作を入力")
        NextChoiceList = {1: "exit", 2: "NewLayer",
                          3: "SetEditeSize", 4: "CountLayer", 5: "EncodeMove"}
        print(NextChoiceList)

        AskNextAction = input()
        if AskNextAction == NextChoiceList[1] or AskNextAction == "1":
            return "exit"

        elif AskNextAction == NextChoiceList[2] or AskNextAction == "2":
            SetImg = Image.new(
                "RGBA", (self.EditSize[0], self.EditSize[1]), (0, 0, 0, 0))
            DrawSetImg = ImageDraw.Draw(SetImg)  # im上のImageDrawインスタンスを作る
            self.layer.append(DrawSetImg)

            print("レイヤー数:" + str(len(self.layer)))
            print(self.layer)

        elif AskNextAction == NextChoiceList[3] or AskNextAction == "3":
            AskDi = self.SetEditSize()
            if AskDi == "safe":
                print("入力に問題なし")
            elif AskDi == "Det":
                print("入力に問題あり")
            else:
                print("どうして？？？")

                return "exit"  # 終了

        elif AskNextAction == NextChoiceList[4] or AskNextAction == "4":
            print("レイヤー数:" + str(len(self.layer)))
            print(self.layer)

        elif AskNextAction == NextChoiceList[5] or AskNextAction == "5":
            print("動画エンコード")


Main_Center = Center()

ReturnDecision = ""
while ReturnDecision != "exit":
    ReturnDecision = Main_Center.NextChoice()  # この関数のところで"exit"returnしたら終了するようにしてる

print("終了")
print("ご利用ありがとうございました")
sys.exit()
