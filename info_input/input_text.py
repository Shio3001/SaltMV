
# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class Center:
    def __init__(self):
        pass

    def main(self, inp_in, thislayer, thislayer_reobj_now):
        thislayer.retention_object[thislayer_reobj_now].document = inp_in
        return thislayer
