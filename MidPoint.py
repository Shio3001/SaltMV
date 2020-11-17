# coding:utf-8
import sys
import numpy
import os


class MidpointElements:
    def Main(self, ilayerloop, NowFlame, layer):

        GetMidpoint = layer[ilayerloop].Point
        PreviousPoint = 0

        # 現在の中間点がどこか検索します
        # itime = 中間点検索用
        for iPoint in range(int(round(len(GetMidpoint)))):
            if GetMidpoint[iPoint]["PointTime"] >= NowFlame:
                PreviousPoint = iPoint - 1
                break

            # print("決定")
        AfterTreatmentPoint = numpy.full(int(len(GetMidpoint[0])), None)  # 数値補間用

        # 命名規則
        # PointTime

        # 周回番号 , key , keyで取得した内容物 , keyの集まり
        # PointGet_N , PointGet_key , PointGet_Element , PointGet_Key_data
        # PointContents_N , PointContents_key , PointContents_Element

        for PointTime in range(int(len(GetMidpoint))):  # Point(time)が何個あるか確認します

            print(GetMidpoint)
            print(334)
            print(PointTime)
            # print(int(len(GetMidpoint[int(PointTime)])))

            for PointGet_N in range(int(len(GetMidpoint[PointTime]))):  # x y a sizeを回しますが、timeのことを考慮しないといけないので 回転数は -1 ,指定する時は+ 1してください

                PointGet_Key_data = list(GetMidpoint[PointGet_N].keys())  # エフェクト数全てのkeyを取得
                PointGet_key = str(PointGet_Key_data[PointGet_N + 1])  # 連想配列にて適応するkey

                print(PointGet_Key_data)
                print(PointGet_key)
                print(len(GetMidpoint[PointTime][PointGet_key]))

                for PointContents_N in range(int(len(GetMidpoint[PointTime][PointGet_key]))):  # 要素数(小)だけ

                    print(list(GetMidpoint[PointTime][PointGet_key].keys()))

                    PointContents_key = GetMidpoint[PointTime][PointGet_key]
                    print(PointContents_key)

                    OldAdjustment = 0
                    NextAdjustment = 0

                    while GetMidpoint[PreviousPoint + OldAdjustment][PointGet_key] is None and PreviousPoint + OldAdjustment != 0:
                        OldAdjustment -= 1
                        print("前の値がNoneだったので数値を変更します")

                    while GetMidpoint[PreviousPoint + NextAdjustment + 1][PointGet_key] is None:
                        NextAdjustment += 1
                        print("次の値がNoneだったので数値を変更します")

                    OldPoint = GetMidpoint[PreviousPoint + OldAdjustment][PointGet_key]
                    OldPointTime = GetMidpoint[PreviousPoint + OldAdjustment]["PointTime"]

                    NextPoint = GetMidpoint[PreviousPoint + 1 + NextAdjustment][PointGet_key]
                    NextPointTime = GetMidpoint[PreviousPoint + 1 + NextAdjustment]["PointTime"]

                    # 中間点地点計算
                    """
                        OutSynthesis = (
                            ((NextPoint - OldPoint) / (NextPointTime - OldPointTime)) * (NowFlame - OldPointTime)) + OldPoint
                        """

                    FrameInterpolation = NextPoint - OldPoint  # 次の地点 - 前の地点
                    TimeInterpolation = NextPointTime - OldPointTime  # 次の地点到達時間 - 前の地点到達時間
                    AdditionalTime = NowFlame - OldPointTime  # 今の時間 - 前の地点到達時間

                    OutSynthesis = ((FrameInterpolation / TimeInterpolation) * AdditionalTime) + OldPoint

                    AfterTreatmentPoint[PointGet_key] = OutSynthesis

                    """
                        print("入力情報:" + "出力地点: " + str(OutSynthesis))

                        print("移動一コマあたり:" + str(FrameInterpolation / TimeInterpolation))

                        print("計算用:" + " 次地点-前地点: " + str(FrameInterpolation) + " 次時間-前時間: " +
                                str(TimeInterpolation) + " 今時間-前時間: " + str(AdditionalTime))

                        print("現在地点:" + str(PreviousPoint) +
                                " 現在フレーム:" + str(NowFlame))

                        print("次フレーム地点: " + str(NextPoint) + " 前フレーム地点: " + str(
                            OldPoint) + " , 次フレーム時間: " + str(NextPointTime) + " 前フレーム時間: " + str(OldPointTime))

                        print("")
                        """

        return AfterTreatmentPoint
