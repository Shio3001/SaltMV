# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class SelectColor_Center:
    def __init__(self):
        self.RGBdata = [0, 0, 0]

    def RGB_select(self):

        print("色 : R を入力してください [0 ~ 255] [ 数値 ]")

        try:
            self.RGBdata[0] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("色 : G を入力してください [0 ~ 255] [ 数値 ]")

        try:
            self.RGBdata[1] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        print("色 : B を入力してください [0 ~ 255] [ 数値 ]")

        try:
            self.RGBdata[2] = int(sys.stdin.readline().rstrip())
        except:
            return "Det"

        return self.RGBdata
