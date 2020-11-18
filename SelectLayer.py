# coding:utf-8
import sys


#import numpy
#import os

#input = sys.stdin.readline
import PrintLayers


class SelectLayer:

    def __init__(self):
        #self.GetPrint = PrintLayers.PrintMain()

        self.layer_Printer = PrintLayers.PrintMain()

    def Main(self, layer):

        self.layer_Printer.ReturnPrint(layer)
        print("レイヤーを選択")

        print("番号 [ 0 から ] ")

        try:
            NumberLayer = int(sys.stdin.readline().rstrip())
            print(layer[NumberLayer])
            return NumberLayer

        except:
            print("レイヤーの取得ができませんでした")
            return "Det"

    def Point(self, layer, NumberLayer):

        self.layer_Printer.ReturnPrint(layer)
        print("変更する中間点を選択")
        print("番号 [ 0 から ] ")

        try:
            NumberPoint = int(sys.stdin.readline().rstrip())
            print(layer[NumberLayer].Point[NumberPoint])
            return NumberPoint

        except:
            print("中間点の取得ができませんでした")
            return "Det"
