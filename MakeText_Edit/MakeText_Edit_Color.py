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
    def EditTexts_Colour(self, layer, EditSize, ilayerloop, GetEditTextsMember, StringCount, Set_SelectColor, EditData_Ope, EditData_Info):

        # print(EditData_Info)
        RGBdata = EditData_Info.RGBdata

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

        layer = EditData_Ope.Import_Cal.Main_Control(layer, EditSize, ilayerloop, RGBdata, EditData_Info.addfntSize, EditData_Info.NewTextString)

        EditData_Info.RGBdata = RGBdata
        return layer, EditData_Info
