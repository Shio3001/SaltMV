# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def __init__(self):
        pass

    def viaAll(self, all_elements):

        print("")
        print("画面サイズ情報 : " + str(all_elements.editor_info))

        for i, ielement in enumerate(all_elements.layer_group):

            print("レイヤー" + ": " + str(ielement.RetentionObject))
            print("レイヤーでの切り抜き" + ": " + str(ielement.layer_cutout))

            print("")

    def viaObject(self, all_elements):
        pass
