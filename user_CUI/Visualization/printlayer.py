# coding:utf-8
import sys
import numpy as np
import os
import copy


class CentralRole:
    def __init__(self):
        pass

    def viaAll(self, all_elements):

        try:

            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            print("")
            print("画面サイズ情報 : " + str(all_elements.editor_info))

            print("レイヤー数: " + str(len(all_elements.layer_group)))

            print("")

            for i, ielement in enumerate(all_elements.layer_group):  # レイヤー単位

                print("レイヤー内オブジェクト数" + ": " + str(len(ielement.retention_object)))
                print("レイヤーでの切り抜き" + ": " + str(ielement.layer_cutout))
                print("")

                for j, jelement in enumerate(ielement.retention_object):  # オブジェクト単位
                    print("開始・終了地点: "+str(jelement.staend_property))
                    print("ファイル:   " + str(jelement.document))
                    # print(jelement.point)

                    print("")

                    for k, kelement in enumerate(jelement.effects):  # エフェクト単位
                        print("エフェクト名: " + str(kelement.effectname))
                        print("エフェクト中間点: " + str(kelement.effectPoint))
                        print("処理: " + str(kelement.procedurelist))

            print("")
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        except:
            print(str(sys.exc_info()))
            print("問題があるみたいです コードにめんどくさいミスがある可能性があります")

            print("終了しますか？ [ 0 : 終了 ] [ 1 : 続行 ]")
            print("保存していない編集データは破棄されます")
            user_select = str(sys.stdin.readline().rstrip())
            if user_select == "0":
                sys.exit()

            else:
                print("続行")

    def viaObject(self, all_elements):
        pass
