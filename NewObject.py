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

        addNewMov = []

        if ObjectType == "1":
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
                    return layer

                else:
                    print("ファイルが正常に入力できませんでした：終了")
                    NewObjct.release()
                    cv2.destroyAllWindows()
                    return "Det"
                    # break

        return "Det"
