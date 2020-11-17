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


class Encoder:
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
            return "Det"

        print("layer取得成功")

        print("動画出力名を入力...")
        os.system("pwd")
        os.system("ls")
        os.system("mkdir Output")
        GetOutputAhead = "Output/" + str(sys.stdin.readline().rstrip())

        size = (EditSize[0], EditSize[1])
        fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)

        os.system("mkdir Encode")

        # あとで移設
        print("*** ファイル削除 ***")

        os.system("rm -fv Encode/OutputBasePicture.png")
        os.system("rm -fv Encode/OutputBaseMov.mp4")

        print("*** ファイル削除 終了 ***")

        print("合成用動画ファイルを生成しています")
        OutputBasePicture = Image.new("RGB", (EditSize[0], EditSize[1]), (0, 0, 0))

        try:
            OutputBasePicture.save("Encode/OutputBasePicture.png")
        except:
            print("動画出力用ファイルの作成に失敗しました 画面サイズが設定されていない可能性があります")
            return "Det"

        # os.system("ffmpeg -loop 1 -i test.jpg -vcodec libx264 -pix_fmt yuv420p -t 3 -r 30 output.mp4")

        os.system("ffmpeg -loop 1 -i Encode/OutputBasePicture.png -vcodec libx264 -pix_fmt yuv420p -t " + str(EditSize[3] / EditSize[2])+" -r "+str(EditSize[2])+" Encode/OutputBaseMov.mp4")

        print("合成用動画ファイルを生成が終了しました")
        print("動画の出力を開始します")

        BaseMov = cv2.VideoCapture("Encode/OutputBaseMov.mp4")

        Writer = cv2.VideoWriter(GetOutputAhead, fmt, EditSize[2], size)  # ライター作成

        PreviewFps = 1

        #layer2 = layer

        # print(layer[0].Point)

        while BaseMov.isOpened():
            ret, Ar_BeseMove = BaseMov.read()
            if ret == True:

                Ar_BeseMove = cv2.cvtColor(Ar_BeseMove, cv2.COLOR_RGB2RGBA)
                OutputData = self.ArrayedSet(BaseMov.get(cv2.CAP_PROP_POS_FRAMES), EditSize, Ar_BeseMove, layer)

                # EditSize ・・・ 動画の設定など
                # BaseMov ・・・出力用の真っ黒なファイル
                # layer ・・・ 動画編集情報

                # 現在いるフレームを送信
                cv2.imshow('OutputPreview', OutputData)
                OutputData = cv2.cvtColor(OutputData, cv2.COLOR_RGBA2RGB)
                Writer.write(OutputData)
                if cv2.waitKey(PreviewFps) & 0xFF == ord('q'):
                    print("書き出し中・・・")
                    # break

            else:
                break

        # print(layer[0].Point)

        Writer.release()
        cv2.destroyAllWindows()

        print("OPENCV END")

        print("動画の出力が終了しました")

        return layer

    def ArrayedSet(self, NowFlame, EditSize, Ar_BeseMove, layer):
        for ilayerloop in range(len(layer)):  # レイヤーの数だけ処理を行う

            # print(str(ilayerloop) + "レイヤー処理")

            # Pointの数だけ処理を行います
            # for iPoint in range(len(layer[ilayerloop].Point)):

            # ((次の地点-前の地点) / (次のフレーム時間 - 前のフレーム時間 * 現在のフレーム時間 - 前のフレーム時間)) + 前の地点

            AfterTreatmentPoint = self.Midpoint_Calculation.Main(ilayerloop, NowFlame, layer)
            # 今どのレイヤーを処理しているか、今のフレーム、レイヤーを送ってあげれば時間を返却してくれる優秀なやつだよ！

            if layer[ilayerloop].ObjectType == "3":  # テキスト選択の場合
                # print("テキストを検出")

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

                # CentralCalculation = list(map(lambda x: -(x/2), CentralCalculation)) #lambdaで頑張ってやったけど結局いらんやん

                for DocM in range(int(len(layer[ilayerloop].Document))):  # 気が向いたらenumerateにしろ

                    UseDocument = layer[ilayerloop].Document[DocM].TextInformation

                    UseDocument_Size_After = map(None, UseDocument)
                    UseDocument_Move_After = map(None, UseDocument)

                    TextSpaceCalculation = [AfterTreatmentPoint["PointMain"]["x"], AfterTreatmentPoint["PointMain"]["y"]]  # X座標,Y座標(ほんとはいるべき場所)

                    ExpansionRate = [int(UseDocument.shape[1] * (AfterTreatmentPoint["PointMain"]["size"] * 0.01)), int(UseDocument.shape[0] * (AfterTreatmentPoint["PointMain"]["size"] * 0.01))]
                    # 拡大率変更後どのぐらいのサイズにするか計算

                    if 0 not in ExpansionRate:  # 拡大率が0でない時
                        UseDocument_Size_After = cv2.resize(UseDocument, (ExpansionRate[0], ExpansionRate[1]), interpolation=cv2.INTER_LINEAR)

                        ResizeCoordinateCorrection = [UseDocument_Size_After.shape[1], UseDocument_Size_After.shape[0]]  # リサイズ後画像サイズが打ち込まれている

                        SizeDifference = (layer[ilayerloop].UniqueProperty.Maxfnt * (AfterTreatmentPoint["PointMain"]["size"] * 0.01)) - ResizeCoordinateCorrection[1 - WHSelection]
                        TextSpacing = [0, 0]
                        TextLocation = [0, 0]

                        if IndividualObject == 1:
                            TextSpacing[WHSelection] = DocM * (layer[ilayerloop].UniqueProperty.TextSpacing + UseDocument.shape[1 - WHSelection])
                            # 何文字目かの処理＊( テキストの間隔 + 元のフォントサイズ )

                        for i in range(2):
                            TextLocation[i] = TextSpaceCalculation[i] + TextSpacing[i] + CentralCalculation[i]  # テキストの最終位置決定

                        TextLocation[1 - WHSelection] += SizeDifference

                        M = numpy.float32(
                            [[1, 0, TextLocation[0]], [0, 1, TextLocation[1]]])

                        UseDocument_Move_After = cv2.warpAffine(UseDocument_Size_After, M, (EditSize[0], EditSize[1]))

                        Ar_BeseMove_img = Image.fromarray(Ar_BeseMove)  # RGBAnumpy -> PIL 変換

                        UseDocument_Move_After_img = Image.fromarray((UseDocument_Move_After).astype(numpy.uint8))  # RGBAnumpy -> PIL 変換

                        Ar_BeseMove_img.paste(UseDocument_Move_After_img, mask=UseDocument_Move_After_img)  # 通常合成

                        # numpy返却 PIL -> RGBAnumpy
                        Ar_BeseMove = numpy.array(Ar_BeseMove_img)
        # print("返却処理")

        return Ar_BeseMove
