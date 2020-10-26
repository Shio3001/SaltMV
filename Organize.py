# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class ArrayOrganize:
    def PointOrganize(self, layer):
        print("Pointを時間順に差し替え")

        print(layer)

        sorted(layer, key=lambda x: x[2])

        print(layer)
        return layer
