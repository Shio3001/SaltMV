# coding:utf-8
import sys
import numpy as np
import os
import copy


class Center:
    def __init__(self):
        pass

    def viaAll(self, all_elements):

        # try:

        print("")
        print("画面サイズ情報 : " + str(all_elements.editor_info))

        print("レイヤー数: " + str(len(all_elements.layer_group)))

        for i, ielement in enumerate(all_elements.layer_group):  # レイヤー単位

            print(len(all_elements.layer_group[0].retention_object))

            print("レイヤー内オブジェクト数" + ": " + str(len(ielement.retention_object)))

            print("レイヤーでの切り抜き" + ": " + str(ielement.layer_cutout))

            print("")

            for j, jelement in enumerate(ielement.retention_object):  # オブジェクト単位
                print("開始・終了地点: "+str(jelement.staend_property))
                print("ファイル数: " + str(np.array(jelement.document).shape))
                # print(jelement.point)

                for k, kelement in enumerate(jelement.effects):  # エフェクト単位
                    print("エフェクト名: " + str(kelement.effectname))
                    print("エフェクト中間点: " + str(kelement.effectPoint))
                    print("処理: " + str(kelement.procedurelist))
                    print("")

        # except:
        #    print(str(sys.exc_info()))

    def viaObject(self, all_elements):
        pass
