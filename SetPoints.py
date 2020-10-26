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
#input = sys.stdin.readline


class MakePoints:
    def __init__(self):
        self.SetSelectLayer = SelectLayer.SelectLayer()

    def Main(self, layer, AddOREdit):
        self.AddPoint = [0, 0, 0, 0]  # time(フレーム) , x , y ,透明度
        NumberLayer = self.SetSelectLayer.Main(layer)

        NumberPoint = None

        if AddOREdit == 1:
            NumberPoint = self.SetSelectLayer.Point(layer, NumberLayer)

        if NumberLayer == "Det" or NumberPoint == "Det":
            return "Det"

        print("")
        print("起点・中間点・終点の追加入力の開始")

        print("")
        print("設定する時間の入力 [ 数値 ]")

        try:
            self.AddPoint[0] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("")
        print("座標：Xの入力 [ 数値 ]")
        try:
            self.AddPoint[1] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("")
        print("座標：Yの入力 [ 数値 ]")
        try:
            self.AddPoint[2] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("")
        print("透明度 [ 数値 ]")
        try:
            self.AddPoint[3] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        if AddOREdit == 0:
            print(layer[NumberLayer][2])
            layer[NumberLayer][2].append(self.AddPoint)
            print(layer[NumberLayer][2])

        elif AddOREdit == 1:
            layer[NumberLayer][2][NumberPoint] = self.AddPoint

        return layer
