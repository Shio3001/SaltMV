# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class ImportMove_Main:
    def Move_Main(self, layer, NumberLayer):
        addNewMov = []
        print("動画ファイルを入力...")
        os.system("pwd")
        os.system("ls")
        inp_in = str(sys.stdin.readline().rstrip())
        NewObjct = cv2.VideoCapture(inp_in)

        while NewObjct.isOpened():
            ret, inputData = NewObjct.read()
            if ret == True:
                inputData = cv2.cvtColor(inputData, cv2.COLOR_RGB2RGBA)
                addNewMov.append(inputData)
                # 現在いるフレームを送信
                #cv2.imshow('input now', inputData)

                if cv2.waitKey(1):
                    pass  # ツウカ
                # break

            elif len(addNewMov) == NewObjct.get(cv2.CAP_PROP_FRAME_COUNT):
                layer[NumberLayer].Document = addNewMov
                print("読み込みに成功")

                layer[NumberLayer].UniqueProperty = [NewObjct.get(cv2.CAP_PROP_FRAME_WIDTH), NewObjct.get(cv2.CAP_PROP_FRAME_HEIGHT), NewObjct.get(cv2.CAP_PROP_FPS), NewObjct.get(cv2.CAP_PROP_FRAME_COUNT)]
                layer[NumberLayer].ObjectType = "1"
                layer[NumberLayer].Property = [0, layer[NumberLayer].UniqueProperty[3], 0]  # オブジェクト読み込み開始地点 # 終了地点 #動画内開始地点

                cv2.destroyAllWindows()
                # NewObjct.release()
                return layer

            else:
                print("ファイルが正常に入力できませんでした：終了")
                NewObjct.release()
                cv2.destroyAllWindows()
                return "EXC"
                # break
