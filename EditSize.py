# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

#input = sys.stdin.readline
import PrintLayers


class SuperSetEditSize:
    def __init__(self):
        self.EditSize = [0, 0, 0, 0]

    def SetEditSize(self):
        print("動画の縦横サイズを入力してください[X,Y]")

        print("[ 横幅 ] を入力")

        try:
            self.EditSize[0] = round(int(sys.stdin.readline().rstrip()))
        except:
            return "EXC"

        print("[ 高さ ] を入力")

        try:
            self.EditSize[1] = round(int(sys.stdin.readline().rstrip()))
        except:
            return "EXC"

        print("[ fps ] を入力")
        try:
            self.EditSize[2] = round(int(sys.stdin.readline().rstrip()))
        except:
            return "EXC"

        print("[ 長さ ] を入力")
        try:
            self.EditSize[3] = round(int(sys.stdin.readline().rstrip()))
        except:
            return "EXC"

        print("入力終了 " + "横 : " +
              str(self.EditSize[0]) + " 高 : " + str(self.EditSize[1]) + " fps値 : " + str(self.EditSize[2]) + " 長さ : " + str(self.EditSize[3]))
        return self.EditSize
