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


class Encoder:
    def __init__(self):
        self.PrintGet_Points = PrintLayers.PrintMain()

    def Main(self, layer, EditSize):
        print("動画の出力を開始")

        try:
            print("")
            print("")
            print("******************************************************")
            print("")
            print("")
            print(layer)
            print("")
            print("")
            print(self.PrintGet_Points)
            print("")
            print("")
            print("******************************************************")
            print("")
            print("")
        except:
            print("layer取得不可")
            return "Det"

        print("layer取得成功")

        print("動画出力名を入力...")
        os.system("pwd")
        os.system("ls")
        GetOutputAhead = str(sys.stdin.readline().rstrip())

        size = (EditSize[0], EditSize[1])
        fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)

        os.system("mkdir Encode")

        # あとで移設
        print("*** ファイル削除 ***")

        os.system("rm -fv Encode/OutputBasePicture.png")
        os.system("rm -fv Encode/OutputBaseMov.mp4")

        print("*** ファイル削除 終了 ***")

        print("合成用動画ファイルを生成しています")
        OutputBasePicture = Image.new(
            "RGB", (EditSize[0], EditSize[1]), (0, 0, 0))

        try:
            OutputBasePicture.save("Encode/OutputBasePicture.png")
        except:
            print("動画出力用ファイルの作成に失敗しました 画面サイズが設定されていない可能性があります")
            return "Det"

        # os.system("ffmpeg -loop 1 -i test.jpg -vcodec libx264 -pix_fmt yuv420p -t 3 -r 30 output.mp4")

        os.system("ffmpeg -loop 1 -i Encode/OutputBasePicture.png -vcodec libx264 -pix_fmt yuv420p -t " +
                  str(EditSize[3] / EditSize[2])+" -r "+str(EditSize[2])+" Encode/OutputBaseMov.mp4")

        print("合成用動画ファイルを生成が終了しました")
        print("動画の出力を開始します")

        BaseMov = cv2.VideoCapture("Encode/OutputBaseMov.mp4")

        Writer = cv2.VideoWriter(
            GetOutputAhead, fmt, EditSize[2], size)  # ライター作成

        PreviewFps = 1

        while BaseMov.isOpened():
            ret, Ar_BeseMove = BaseMov.read()
            if ret == True:
                cv2.cvtColor(Ar_BeseMove, cv2.COLOR_RGB2RGBA)
                OutputData = self.ArrayedSet(
                    BaseMov.get(cv2.CAP_PROP_POS_FRAMES), EditSize, Ar_BeseMove, layer)
                # EditSize ・・・ 動画の設定など
                # BaseMov ・・・出力用の真っ黒なファイル
                # layer ・・・ 動画編集情報

                # 現在いるフレームを送信
                cv2.imshow('OutputPreview', OutputData)
                cv2.cvtColor(OutputData, cv2.COLOR_RGBA2RGB)
                Writer.write(OutputData)
                if cv2.waitKey(PreviewFps) & 0xFF == ord('q'):
                    print("書き出し中・・・")
                    # break

            else:
                break

        Writer.release()
        cv2.destroyAllWindows()
        print("OPENCV END")

        print("動画の出力が終了しました")

        return layer

    def ArrayedSet(self, NowFlame, EditSize, Ar_BeseMove, layer):

        # print("Classから出力用データを生成する")

        # try:

        for ilayerloop in range(len(layer)):  # レイヤーの数だけ処理を行う
            # print(str(ilayerloop) + "レイヤー処理")

            PointNotTime = layer[ilayerloop].Point
            del PointNotTime[:][0]

            # Pointの数だけ処理を行います
            for iPoint in range(len(layer[ilayerloop].Point)):

                # x y aを回しますが、timeのことを考慮しないといけないので + 1してください
                for Storage in range(3):

                    if layer[ilayerloop].Point[iPoint][Storage + 1] != None:
                        # print(Storage + 1)

                        try:

                            PreviousPoint = 0

                            # 現在の中間点がどこか検索します
                            for itime in range(EditSize[3]):  # itime = 中間点検索用
                                if layer[ilayerloop].Point[iPoint][0] >= NowFlame:
                                    PreviousPoint = itime
                                    # print("")
                                    # print("現在の地点：変更")
                                    # print("")
                                    # print("現在の地点:" + str(PreviousPoint))
                                    break

                            NextPoint = layer[ilayerloop].Point[PreviousPoint + 1][Storage + 1]
                            OldPoint = layer[ilayerloop].Point[PreviousPoint][Storage + 1]

                            NextPointTime = layer[ilayerloop].Point[PreviousPoint + 1][0]
                            OldPointTime = layer[ilayerloop].Point[PreviousPoint][0]

                            # 中間点地点計算
                            OutSynthesis = (
                                (NextPoint - OldPoint) / (NextPointTime - OldPointTime) * (NowFlame - OldPointTime)) + OldPoint

                            print("入力情報:" + "出力地点: " + str(OutSynthesis))

                            print("現在地点:" + str(PreviousPoint) +
                                  " 現在フレーム:" + str(NowFlame))

                            print("前フレーム地点: " + str(NextPoint) + " 次フレーム地点: " + str(
                                OldPoint) + " , 次フレーム時間: " + str(NextPointTime) + " 前フレーム時間: " + str(OldPointTime))

                            print("")

                            # print("アバババ")

                        except:
                            print("動画の中間点指定に失敗しました")
                            return "Det"

                # ((次の地点-前の地点) / (次のフレーム時間 - 前のフレーム時間 * 現在のフレーム - 前のフレーム時間)) + 前の地点
            """
            for rs in range(3):
                Ar_BeseMove[:, :, rs] = Ar_BeseMove[:, :, rs] + (
                    img1_arMov[:, :, rs] - Ar_BeseMove[:, :, rs]) * (img1_arMov[:, :, 3] / 255)
            """

    # except:
        #    print("なんか無理だった")

        return Ar_BeseMove
