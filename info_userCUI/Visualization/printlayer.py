# coding:utf-8
import sys
import numpy as np
import os
import copy


class Center:
    def __init__(self):
        pass

    def viaAll(self, all_elements):

        print("")
        print("画面サイズ情報 : " + str(all_elements.editor_info))

        for i, ielement in enumerate(all_elements.layer_group):  # レイヤー単位

            print("レイヤー" + ": " + str(ielement.retention_object))

            print("レイヤーでの切り抜き" + ": " + str(ielement.layer_cutout))

            print("")

            for j, jelement in enumerate(ielement.retention_object):  # オブジェクト単位
                print("開始・終了地点: "+str(jelement.staend_property))
                print("ファイル数: " + str(jelement.document.shape))
                print(jelement.point)

    def viaObject(self, all_elements):
        pass
