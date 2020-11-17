# coding:utf-8
import sys
import numpy
import os

import copy


class MidpointElements:
    def Main(self, ilayerloop, NowFlame, layer):

        GetMidpoint = copy.deepcopy(layer[ilayerloop].Point)

        # ここから先にGetMidpointに関するなんかしらの副作用がある説あり、copy.deepcopyで無理やり封印してますが

        PreviousPoint = 0

        print(layer[ilayerloop].Point)

        # 現在の中間点がどこか検索します
        # itime = 中間点検索用
        for iPoint in range(int(round(len(GetMidpoint)))):
            if GetMidpoint[iPoint]["PointTime"] >= NowFlame:
                PreviousPoint = iPoint - 1
                break

            # print("決定")
        AfterTreatmentPoint = GetMidpoint[0]  # 数値補間用

        # 命名規則
        # PointTime

        # 周回番号 , key , keyで取得した内容物 , keyの集まり
        # PointGet_N , PointGet_key , PointGet_Element , PointGet_Key_data
        # PointContents_N , PointContents_key , PointContents_Element , PointContents_key_data

        PointTime = PreviousPoint  # PreviousPointは途中で数値が変更されるようになってるので分離しておきましょう

        # for PointTime in range(int(len(GetMidpoint))):  # Point(time)が何個あるか確認します

        for PointGet_N in range(int(len(GetMidpoint[PointTime])) - 1):  # x y a sizeを回しますが、timeのことを考慮しないといけないので 回転数は -1 ,指定する時は+ 1してください

            #print("aba" + str(PointGet_N))
            PointGet_Key_data = list(GetMidpoint[PointTime - 1].keys())  # エフェクト数全てのkeyを取得

            # print(PointGet_Key_data)
            PointGet_key = str(PointGet_Key_data[PointGet_N + 1])  # 連想配列にて適応するkey

            # print(PointGet_key)
            for PointContents_N in range(int(len(GetMidpoint[PointTime][PointGet_key]))):  # 要素数(小)だけ

                PointContents_key_data = list(GetMidpoint[PointTime][PointGet_key].keys())  # 最終的なkeyを取得
                PointContents_key = PointContents_key_data[PointContents_N]
                # print(PointContents_key)

                OldAdjustment = 0
                NextAdjustment = 0

                while GetMidpoint[PreviousPoint + OldAdjustment][PointGet_key] is None and PreviousPoint + OldAdjustment != 0:
                    OldAdjustment -= 1
                    print("前の値がNoneだったので数値を変更します")

                while GetMidpoint[PreviousPoint + NextAdjustment + 1][PointGet_key] is None:
                    NextAdjustment += 1
                    print("次の値がNoneだったので数値を変更します")

                OldPoint = GetMidpoint[PreviousPoint + OldAdjustment][PointGet_key][PointContents_key]
                OldPointTime = GetMidpoint[PreviousPoint + OldAdjustment]["PointTime"]

                NextPoint = GetMidpoint[PreviousPoint + 1 + NextAdjustment][PointGet_key][PointContents_key]
                NextPointTime = GetMidpoint[PreviousPoint + 1 + NextAdjustment]["PointTime"]

                FrameInterpolation = NextPoint - OldPoint  # 次の地点 - 前の地点
                TimeInterpolation = NextPointTime - OldPointTime  # 次の地点到達時間 - 前の地点到達時間
                AdditionalTime = NowFlame - OldPointTime  # 今の時間 - 前の地点到達時間

                OutSynthesis = ((FrameInterpolation / TimeInterpolation) * AdditionalTime) + OldPoint

                # print(OutSynthesis)

                AfterTreatmentPoint[PointGet_key][PointContents_key] = OutSynthesis

                """

                print("PointGet_key: " + str(PointGet_key) + " PointContents_key: " + str(PointContents_key))

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
