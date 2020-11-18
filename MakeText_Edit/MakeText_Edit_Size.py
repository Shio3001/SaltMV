# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

# 三番目にえらい
#import MakeText_Calculation

#import EditData


class MakeEditSize:
    def EditTexts_Size(self, layer, EditSize, ilayerloop, GetEditTextsMember, EditTexts_fntSize, Set_MakeEditText_EditData):

        addfntSize = Set_MakeEditText_EditData.EditDataElement().addfntSize

        print("変更後のフォントサイズを入力 [数値]")
        print("現在:" + str(EditTexts_fntSize))
        EditTexts_AfterSize = int(sys.stdin.readline().rstrip())

        print("挿入方式 置き換え:[ 0 ] 加算:[ 1 ]")
        EditTexts_CalculationSize = int(sys.stdin.readline().rstrip())

        NumberOfCalculations = int(GetEditTextsMember[1]) - int(GetEditTextsMember[0]) + 1
        print("計算回数" + str(NumberOfCalculations))

        for i in range(NumberOfCalculations):

            iEdit = i + int(GetEditTextsMember[0])
            print(iEdit)

            if EditTexts_CalculationSize == 0:
                EditTexts_fntSize[iEdit] = EditTexts_AfterSize
            if EditTexts_CalculationSize == 1:
                EditTexts_fntSize[iEdit] += EditTexts_AfterSize

            addfntSize[iEdit] = EditTexts_fntSize[iEdit]

        print(EditTexts_fntSize)
        layer = Set_MakeEditText_EditData.EditDataElement().Import_Cal.Main_Control(layer, EditSize, ilayerloop, Set_MakeEditText_EditData.EditDataElement().RGBdata, addfntSize, Set_MakeEditText_EditData.EditDataElement().NewTextString)
        return layer
