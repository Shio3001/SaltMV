# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


#import EditData

# 三番目にえらい


class MakeEditColor:
    def EditTexts_Colour(self, layer, EditSize, ilayerloop, GetEditTextsMember, StringCount, Set_SelectColor, Set_MakeEditText_EditData):

        RGBdata = Set_MakeEditText_EditData.EditDataElement().RGBdata

        AskDi = Set_SelectColor.RGB_select()

        if AskDi == "Det":
            return "Det"
        else:
            NumberOfCalculations = int(GetEditTextsMember[1]) - int(GetEditTextsMember[0]) + 1
            print("計算回数" + str(NumberOfCalculations))

            for i in range(NumberOfCalculations):
                iEdit = i + int(GetEditTextsMember[0])
                print(iEdit)
                RGBdata[iEdit] = AskDi

        layer = Set_MakeEditText_EditData.EditDataElement().Import_Cal().Main_Control(layer, EditSize, ilayerloop, RGBdata, Set_MakeEditText_EditData.EditDataElement().addfntSize, Set_MakeEditText_EditData.EditDataElement().NewTextString)
        return layer
