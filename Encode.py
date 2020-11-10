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
                Ar_BeseMove = cv2.cvtColor(Ar_BeseMove, cv2.COLOR_RGB2RGBA)
                OutputData = self.ArrayedSet(
                    BaseMov.get(cv2.CAP_PROP_POS_FRAMES), EditSize, Ar_BeseMove, layer)

                if OutputData == "Det":
                    print("出力エラー")
                    return "Det"
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

        Writer.release()
        cv2.destroyAllWindows()
        print("OPENCV END")

        print("動画の出力が終了しました")

        return layer

    def ArrayedSet(self, NowFlame, EditSize, Ar_BeseMove, layer):

        #Ar_BeseMove2 = Ar_BeseMove

        # print("Classから出力用データを生成する")

        # try:

        for ilayerloop in range(len(layer)):  # レイヤーの数だけ処理を行う
            # print(str(ilayerloop) + "レイヤー処理")

            # Pointの数だけ処理を行います
            # for iPoint in range(len(layer[ilayerloop].Point)):

            PreviousPoint = 0

            # 現在の中間点がどこか検索します
            # itime = 中間点検索用
            for iPoint in range(int(round(len(layer[ilayerloop].Point)))):
                if layer[ilayerloop].Point[iPoint][0] >= NowFlame:
                    PreviousPoint = iPoint - 1
                    break

                # print("決定")
            AfterTreatmentPoint = numpy.full(
                int(len(layer[ilayerloop].Point[0])), None)  # 数値補間用

            # x y aを回しますが、timeのことを考慮しないといけないので + 1してください
            for Storage in range(int(len(layer[ilayerloop].Point[0]))-1):

                OldAdjustment = 0
                NextAdjustment = 0

                while layer[ilayerloop].Point[PreviousPoint + OldAdjustment][Storage + 1] is None and PreviousPoint + OldAdjustment != 0:

                    OldAdjustment -= 1
                    print("前の値がNoneだったので数値を変更します")

                while layer[ilayerloop].Point[PreviousPoint + NextAdjustment + 1][Storage + 1] is None:

                    NextAdjustment += 1
                    print("次の値がNoneだったので数値を変更します")

                OldPoint = layer[ilayerloop].Point[PreviousPoint +
                                                   OldAdjustment][Storage + 1]
                OldPointTime = layer[ilayerloop].Point[PreviousPoint +
                                                       OldAdjustment][0]

                NextPoint = layer[ilayerloop].Point[PreviousPoint +
                                                    1 + NextAdjustment][Storage + 1]
                NextPointTime = layer[ilayerloop].Point[PreviousPoint +
                                                        1 + NextAdjustment][0]

                # 中間点地点計算
                """
                OutSynthesis = (
                    ((NextPoint - OldPoint) / (NextPointTime - OldPointTime)) * (NowFlame - OldPointTime)) + OldPoint
                """

                FrameInterpolation = NextPoint - OldPoint  # 次の地点 - 前の地点
                TimeInterpolation = NextPointTime - OldPointTime  # 次の地点到達時間 - 前の地点到達時間
                AdditionalTime = NowFlame - OldPointTime  # 今の時間 - 前の地点到達時間

                OutSynthesis = ((
                    FrameInterpolation / TimeInterpolation) * AdditionalTime) + OldPoint

                AfterTreatmentPoint[Storage + 1] = OutSynthesis

                print("入力情報:" + "出力地点: " + str(OutSynthesis))

                print("移動一コマあたり:" + str(FrameInterpolation / TimeInterpolation))

                print("計算用:" + " 次地点-前地点: " + str(FrameInterpolation) + " 次時間-前時間: " +
                      str(TimeInterpolation) + " 今時間-前時間: " + str(AdditionalTime))

                print("現在地点:" + str(PreviousPoint) +
                      " 現在フレーム:" + str(NowFlame))

                print("次フレーム地点: " + str(NextPoint) + " 前フレーム地点: " + str(
                    OldPoint) + " , 次フレーム時間: " + str(NextPointTime) + " 前フレーム時間: " + str(OldPointTime))

                print("")

            # ((次の地点-前の地点) / (次のフレーム時間 - 前のフレーム時間 * 現在のフレーム時間 - 前のフレーム時間)) + 前の地点

            if layer[ilayerloop].Property[0] == "Text":

                print("テキストを検出")

                # テキストの数だけ処理
                # DocM = DocumentMove

                PreviousMoveAmount = [0, 0]  # 個別縮小がOFFの時、前の奴がどれだけ移動したかを記憶

                for DocM in range(int(len(layer[ilayerloop].Document))):
                    # print(len(layer[ilayerloop].Document))
                    UseDocument = layer[ilayerloop].Document[DocM]
                    UseDocument_Size_After = UseDocument
                    UseDocument_Move_After = UseDocument

                    TextSpaceCalculation = [
                        AfterTreatmentPoint[1], AfterTreatmentPoint[2]]

                    # 明日はこここをやれ
                    # ここから拡大縮小の件 Aviutでいう普通の[拡大縮小][フォントサイズの方ではない]

                    # print(AfterTreatmentPoint[4])
                    # print(UseDocument.shape[1])
                    # print(UseDocument.shape[0])

                    ExpansionRate = [int(UseDocument.shape[1] * (AfterTreatmentPoint[4] * 0.01)),
                                     int(UseDocument.shape[0] * (AfterTreatmentPoint[4] * 0.01))]
                    # 拡大率変更前の画像サイズとどれぐらい拡大縮小するかを計算する

                    # print(ExpansionRate)

                    if 0 in ExpansionRate:  # 拡大率に0が会ったら弾く
                        PreviousMoveAmount = [0, 0]

                    else:
                        UseDocument_Size_After = cv2.resize(
                            UseDocument, (ExpansionRate[0], ExpansionRate[1]), interpolation=cv2.INTER_LINEAR)

                        ResizeCoordinateCorrection = [
                            UseDocument_Size_After.shape[1], UseDocument_Size_After.shape[0]]  # リサイズ後画像サイズが打ち込まれている

                        # ここまで

                        if layer[ilayerloop].UniqueProperty[0] == 0:  # 文字が横書きの処理
                            TextSpaceCalculation[0] = TextSpaceCalculation[0] + (
                                DocM * (layer[ilayerloop].UniqueProperty[1] + layer[ilayerloop].UniqueProperty[2]))

                            PreviousMoveAmount = [PreviousMoveAmount[0] + (ResizeCoordinateCorrection[0]
                                                                           * 0.25), PreviousMoveAmount[1]]

                        if layer[ilayerloop].UniqueProperty[0] == 1:  # 文字が縦書きの処理
                            TextSpaceCalculation[1] = TextSpaceCalculation[1] + (
                                DocM * (layer[ilayerloop].UniqueProperty[1] + layer[ilayerloop].UniqueProperty[2]))

                            PreviousMoveAmount = [PreviousMoveAmount[0], PreviousMoveAmount[1] + (ResizeCoordinateCorrection[1] * 0.25)]

                        # ここから移動に関する処理

                        M = numpy.float32([[1, 0, TextSpaceCalculation[0] + PreviousMoveAmount[0]], [
                            0, 1, TextSpaceCalculation[1] + PreviousMoveAmount[1]]])

                        UseDocument_Move_After = cv2.warpAffine(
                            UseDocument_Size_After, M, (EditSize[0], EditSize[1]))
                            
                        
                        Ar_BeseMove_img = Image.fromarray(Ar_BeseMove) #変換
                        UseDocument_Move_After_img = Image.fromarray(UseDocument_Move_After) #変換
                            
                        Ar_BeseMove_img.paste(UseDocument_Move_After_img, mask=UseDocument_Move_After_img) #合成
                        
                        Ar_BeseMove = numpy.array(Ar_BeseMove_img) #numpy返却
                            
                        
        print("返却処理")

        return Ar_BeseMove
