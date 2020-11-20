# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class OutputMove_Main:
    def OutputMove(self, layer, ilayerloop, AfterTreatmentPoint, EditSize, Ar_BeseMove, NowFlame):

        Move_UniqueProperty = layer[ilayerloop].UniqueProperty
        Move_Property = layer[ilayerloop].Property
        NowPoint = [AfterTreatmentPoint["PointMain"]["x"], AfterTreatmentPoint["PointMain"]["y"]]  # X座標,Y座標(ほんとはいるべき場所)

        if layer[ilayerloop].ObjectType == "1":
            UseDocument = layer[ilayerloop].Document[NowFlame]

        if layer[ilayerloop].ObjectType == "2":
            UseDocument = layer[ilayerloop].Document

        UseDocument_Size_After = map(None, UseDocument)
        UseDocument_Move_After = map(None, UseDocument)

        ExpansionRate = [int(UseDocument.shape[1] * (AfterTreatmentPoint["PointMain"]["size"] * 0.01)), int(UseDocument.shape[0] * (AfterTreatmentPoint["PointMain"]["size"] * 0.01))]

        if 0 not in ExpansionRate:  # 拡大率が0でない時
            UseDocument_Size_After = cv2.resize(UseDocument, (ExpansionRate[0], ExpansionRate[1]), interpolation=cv2.INTER_LINEAR)

            #NowPoint = list(map(lambda x: x - (ExpansionRate / 2), NowPoint))

            for i in range(2):
                NowPoint[i] -= (ExpansionRate[i] / 2)

            # print(NowPoint)

            M = numpy.float32([[1, 0, NowPoint[0]], [0, 1, NowPoint[1]]])

            UseDocument_Move_After = cv2.warpAffine(UseDocument_Size_After, M, (EditSize[0], EditSize[1]))

            Ar_BeseMove_img = Image.fromarray((Ar_BeseMove).astype(numpy.uint8))  # RGBAnumpy -> PIL 変換

            UseDocument_Move_After_img = Image.fromarray((UseDocument_Move_After).astype(numpy.uint8))  # RGBAnumpy -> PIL 変換

            Ar_BeseMove_img.paste(UseDocument_Move_After_img, mask=UseDocument_Move_After_img)  # 通常合成

            # numpy返却 PIL -> RGBAnumpy
            Ar_BeseMove = numpy.array(Ar_BeseMove_img)

        return Ar_BeseMove
