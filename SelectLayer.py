# coding:utf-8
import sys
import numpy
import os

#input = sys.stdin.readline


class SelectLayer:

    def Main(self, layer):
        print("オブジェクトを入れるレイヤーを選択")
        print(layer)

        print("番号 [ 0 から ] ")

        try:
            NumberLayer = int(sys.stdin.readline().rstrip())
            print(layer[NumberLayer][0])
            return NumberLayer

        except:
            print("レイヤーの取得ができませんでした")
            return "Det"

    def Point(self, layer, NumberLayer):
        print("変更する中間点を選択")
        print(layer)

        print("番号 [ 1 から ] ")

        try:
            NumberPoint = int(sys.stdin.readline().rstrip())
            print(layer[NumberLayer][NumberPoint])
            return NumberPoint

        except:
            print("中間点の取得ができませんでした")
            return "Det"
