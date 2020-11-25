# coding:utf-8
import sys
import numpy
import os
import copy


class PrintLayer:
    def __init__(self):
        pass

    def viaLayer(self, layer_group):
        for i, ielement in enumerate(layer_group):

            print("")
            print("レイヤー" + ": " + str(ielement.RetentionObject))
            print("レイヤーでの切り抜き" + ": " + str(ielement.layer_cutout))

            print("")

    def viaObject(self, layer_group):
        pass
