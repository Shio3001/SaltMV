# coding:utf-8
import sys
import numpy
import os

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

# input = sys.stdin.readline
import PrintLayers
import MidPoint

from ExportFile import ExportText

layer_Printer = PrintLayers.PrintMain()

ExportFile_ExportText = ExportText.OutputText_Main()


class Export_Center:
    def __init__(self):
        self.PrintGet_Points = PrintLayers.PrintMain()
        self.Midpoint_Calculation = MidPoint.MidpointElements()

    def Main(self, layer, EditSize):
        print("動画の出力を開始")

        try:
            print("")
            print("")
            print("******************************************************")
            print("")
            print("")
            # print(layer[0].Point)
            print("")
            print("")
            # print(self.PrintGet_Points)
            print("")
            print("")
            print("******************************************************")
            print("")
            print("")
        except:
            print("layer取得不可")
            return "EXC"

        print("layer取得成功")

        print("動画出力名を入力...")
        os.system("pwd")
        os.system("ls")
        os.system("mkdir Output")
        GetOutputAhead = "Output/" + str(sys.stdin.readline().rstrip())

        size = (EditSize[0], EditSize[1])
        fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)

        Writer = cv2.VideoWriter(GetOutputAhead, fmt, EditSize[2], size)  # ライター作成

        PreviewFps = 1

        # layer2 = layer

        # print(layer[0].Point)

        layer_Printer.ReturnPrint(layer)

        for iExport in range(EditSize[3]):
            OutputData = self.ArrayedSet(iExport, EditSize, layer)

            # print(OutputData.shape)

            # EditSize ・・・ 動画の設定など
            # BaseMov ・・・出力用の真っ黒なファイル
            # layer ・・・ 動画編集情報

            # 現在いるフレームを送信
            cv2.imshow('OutputPreview', OutputData)

            OutputData = cv2.cvtColor(OutputData.astype('uint8'), cv2.COLOR_RGBA2RGB)
            Writer.write(OutputData)

            # opencvの出力周りはuint8じゃないとダメなみたい

            if cv2.waitKey(PreviewFps) & 0xFF == ord('q'):
                print("書き出し中・・・")
                # break

        # print(layer[0].Point)

        Writer.release()
        cv2.destroyAllWindows()

        print("OPENCV END")

        print("動画の出力が終了しました")

        return layer

    def ArrayedSet(self, NowFlame, EditSize, layer):
        for ilayerloop in range(len(layer)):  # レイヤーの数だけ処理を行う

            Ar_BeseMove = numpy.zeros((EditSize[1], EditSize[0], 4))  # numpyって指定する時縦横逆なんだな、めんどくさい
            # Ar_BeseMove = cv2.cvtColor(Ar_BeseMove, cv2.COLOR_RGB2RGBA)

            # ((次の地点-前の地点) / (次のフレーム時間 - 前のフレーム時間 * 現在のフレーム時間 - 前のフレーム時間)) + 前の地点

            AfterTreatmentPoint = self.Midpoint_Calculation.Main(ilayerloop, NowFlame, layer)
            # 今どのレイヤーを処理しているか、今のフレーム、レイヤーを送ってあげれば時間を返却してくれる優秀なやつだよ！

            if layer[ilayerloop].ObjectType == "3":  # テキスト選択の場合
                Ar_BeseMove = ExportFile_ExportText.OutputText(layer, ilayerloop, AfterTreatmentPoint, EditSize, Ar_BeseMove)

                # print("返却処理")

        return Ar_BeseMove
