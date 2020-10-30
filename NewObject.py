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
# ここから各オブジェクトを追加するのを書く

#input = sys.stdin.readline


class MakeObject:
    def __init__(self):
        self.SetSelectLayer = SelectLayer.SelectLayer()
        print("")
        self.NumberLayer = 0

    def MakeObjectCenter(self, layer):

        self.NumberLayer = self.SetSelectLayer.Main(layer)
        if self.NumberLayer == "Det":
            return "Det"

        print("[ 読み込み ]")

        print("種類を選択 [ 番号 ]")
        print("1:動画")
        print("2:")
        print("3:")
        print("4:")
        ObjectType = str(sys.stdin.readline().rstrip())

        if ObjectType == "1":
            print("動画ファイルを入力...")
            os.system("pwd")
            os.system("ls")
            inp_in = str(sys.stdin.readline().rstrip())
            try:
                NewObjct = cv2.VideoCapture(inp_in)

                ret, Moves = NewObjct.read()

                if ret == False:
                    return "Det"
                elif ret == True:
                    layer[self.NumberLayer].Document = Moves
                    print("読み込みに成功")
                    return layer

            except:
                print("ファイルを正常に読み込めませんでした")
                return "Det"
