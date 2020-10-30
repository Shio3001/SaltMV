# coding:utf-8

"""
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
"""

import PrintLayers


class ArrayOrganize:

    def __init__(self):
        self.PrintGet_Points = PrintLayers.PrintMain()

    def PointOrganize(self, layer):

        print("Pointを時間順に差し替え")

        # layer = sorted(, key=lambda x: x[2])

        for ilayer in range(len(layer)):
            layer[ilayer].Point = sorted(
                layer[ilayer].Point, key=lambda x: x[0], reverse=False)
            print("sort処理: " + str(ilayer) + " 処理回数: " + str(len(layer)))

        # self.PrintGet_Points.ReturnPrint(layer)
        #GetPoint = self.PrintGet_Points.GetPoint(layer, 0)
        #print("Point 処理後 " + str(GetPoint))

        return layer
