# coding:utf-8
import sys
import numpy
import os


class PrintMain:
    def ReturnPrint(self, layer):
        for iprint in range(len(layer)):

            print("")

            #print(" " + str(layer[iprint].Document))

            for iprint_Point in range(len(layer[iprint].Point)):
                print("     " + str(layer[iprint].Point[iprint_Point]))

            print("     " + "オブジェクトタイプ " + str(layer[iprint].ObjectType))
            print("     " + "開始終了地点 " + str(layer[iprint].Property))
            print("     " + str(layer[iprint].UniqueProperty))

            print("")
