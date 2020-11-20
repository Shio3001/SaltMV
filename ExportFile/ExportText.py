# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

# print("テキストを検出")


class OutputText_Main:

    def OutputText(self, layer, ilayerloop, AfterTreatmentPoint, EditSize, Ar_BeseMove):
        # 文字間隔をもらう
        CharacterSpace = layer[ilayerloop].UniqueProperty.TextSpacing
        # 縦書きか横書きかの選択結果をもらってくる
        WHSelection = layer[ilayerloop].UniqueProperty.WritingDirection
        # 前揃えか中揃えか後ろ揃えかの選択結果をもらってくる
        AlignmentPos = layer[ilayerloop].UniqueProperty.AlignmentPosition
        # 個別オブジェクトか判断 0(false) or 1(true)
        IndividualObject = layer[ilayerloop].UniqueProperty.IndividualObject

        CentralCalculation = [0, 0]  # 上下左右中央の揃えよう、どれだけずらすかを格納

        DocMlet = int(len(layer[ilayerloop].Document))  # 要素の数

        TotalCharacter = [0, int(layer[ilayerloop].UniqueProperty.Maxfnt)]  # テキストの長さを計算するよ
        for i in range(int(len(layer[ilayerloop].Document))):
            TotalCharacter[0] += layer[ilayerloop].Document[i].TextSize

        if IndividualObject == 1:  # 個別オブジェクト時、テキストの総合的な長さを計算する
            CentralCalculation[WHSelection] = (CharacterSpace * (DocMlet - 1)) + TotalCharacter[0]  # 長い方
            CentralCalculation[1 - WHSelection] = TotalCharacter[1]  # 短い方

            for i in range(2):
                if AlignmentPos[i] == 0:  # 左・上寄せの時は何もしない
                    CentralCalculation[i] = 0
                if AlignmentPos[i] == 1:
                    CentralCalculation[i] /= -2  # 中寄せの時は半分引く
                if AlignmentPos[i] == 2:
                    CentralCalculation[i] *= 1  # 右寄せの時は丸々足す

                AlignmentPos[i] *= (AfterTreatmentPoint["PointMain"]["size"] * 0.01)

        # CentralCalculation = list(map(lambda x: -(x/2), CentralCalculation)) #lambdaで頑張ってやったけど結局いらんやん

        for DocM in range(int(len(layer[ilayerloop].Document))):  # 気が向いたらenumerateにしろ #テキストの数だけやる

            UseDocument = layer[ilayerloop].Document[DocM].TextInformation

            UseDocument_Size_After = map(None, UseDocument)
            UseDocument_Move_After = map(None, UseDocument)

            # print(UseDocument.shape)

            TextSpaceCalculation = [AfterTreatmentPoint["PointMain"]["x"], AfterTreatmentPoint["PointMain"]["y"]]  # X座標,Y座標(ほんとはいるべき場所)

            ExpansionRate = [int(UseDocument.shape[1] * (AfterTreatmentPoint["PointMain"]["size"] * 0.01)), int(UseDocument.shape[0] * (AfterTreatmentPoint["PointMain"]["size"] * 0.01))]
            # 拡大率変更後どのぐらいのサイズにするか計算

            if 0 not in ExpansionRate:  # 拡大率が0でない時
                UseDocument_Size_After = cv2.resize(UseDocument, (ExpansionRate[0], ExpansionRate[1]), interpolation=cv2.INTER_LINEAR)

                ResizeCoordinateCorrection = [UseDocument_Size_After.shape[1], UseDocument_Size_After.shape[0]]  # リサイズ後画像サイズが打ち込まれている

                SizeDifference = (layer[ilayerloop].UniqueProperty.Maxfnt * (AfterTreatmentPoint["PointMain"]["size"] * 0.01)) - ResizeCoordinateCorrection[1 - WHSelection]
                TextSpacing = [0, 0]
                TextLocation = [0, 0]

                if IndividualObject == 0:
                    for i in range(2):
                        if AlignmentPos[i] == 0:  # 左・上寄せの時は何もしない
                            CentralCalculation[i] = 0
                        if AlignmentPos[i] == 1:
                            CentralCalculation[i] = -1 * (ResizeCoordinateCorrection[i] / 2)  # 中寄せの時は半分引く
                        if AlignmentPos[i] == 2:
                            CentralCalculation[i] *= 1  # 右寄せの時は丸々足す

                if IndividualObject == 1:
                    TextSpacing[WHSelection] = DocM * (layer[ilayerloop].UniqueProperty.TextSpacing + UseDocument.shape[1 - WHSelection])
                    # 何文字目かの処理＊( テキストの間隔 + 元のフォントサイズ )

                for i in range(2):
                    TextLocation[i] = TextSpaceCalculation[i] + TextSpacing[i] + CentralCalculation[i]  # テキストの最終位置決定

                TextLocation[1 - WHSelection] += SizeDifference

                M = numpy.float32([[1, 0, TextLocation[0]], [0, 1, TextLocation[1]]])

                UseDocument_Move_After = cv2.warpAffine(UseDocument_Size_After, M, (EditSize[0], EditSize[1]))

                Ar_BeseMove_img = Image.fromarray((Ar_BeseMove).astype(numpy.uint8))  # RGBAnumpy -> PIL 変換

                UseDocument_Move_After_img = Image.fromarray((UseDocument_Move_After).astype(numpy.uint8))  # RGBAnumpy -> PIL 変換

                Ar_BeseMove_img.paste(UseDocument_Move_After_img, mask=UseDocument_Move_After_img)  # 通常合成

                # numpy返却 PIL -> RGBAnumpy
                Ar_BeseMove = numpy.array(Ar_BeseMove_img)

        return Ar_BeseMove
