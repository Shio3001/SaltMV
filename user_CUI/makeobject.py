# coding:utf-8
import sys
import numpy as np
import os
import copy


class CentralRole:
    def main(self, all_elements, elements, thislayer, operation_list, responselist):

        # 次のオブジェクトの開始地点と、今のオブジェクトの終了地点を引いて、0以下であればかぶっている判定にしてあげれば勝ち

        print("オブジェクト生成")

        userselect_layer_object_num = int(len(thislayer.retention_object))
        # 指定したレイヤーに何個オブジェクトがあるか確認
        thislayer_reobj_now = 0

        if userselect_layer_object_num != 0:
            print("このレイヤーにはすでにオブジェクトが" + str(userselect_layer_object_num) + "コ存在しています")
            print("既存のオブジェクトを変更する場合は、オブジェクト番号を入力 [ 1から ][ 数値 ] [ 新規作成は空白 ]")

            try:
                thislayer_reobj_now = int(sys.stdin.readline().rstrip()) - 1
                print("対象オブジェクト: " + str(thislayer_reobj_now + 1))
                print(thislayer.retention_object[thislayer_reobj_now])
            except:  # エラーを起こしたら存在しない扱い、新規作成へと誘導
                print(str(sys.exc_info()))
                thislayer, thislayer_reobj_now = self.new_obj(thislayer, operation_list, all_elements, elements)
        else:
            thislayer, thislayer_reobj_now = self.new_obj(thislayer, operation_list, all_elements, elements)

        edit_object_response = responselist[1]
        # object_selectlist = {0: "返却", 1: "動画", 2: "画像", 3: "テキスト", 4: "図形", 5: "エフェクト"}
        object_selectlist = np.array([["0", "返却", self.nothing],
                                      ["1", "動画", self.video],
                                      ["2", "画像", self.image],
                                      ["3", "テキスト", self.text],
                                      ["4", "図形", self.shape],
                                      ["5", "エフェクト", self.effect]])
        # object_selectlist_keys=list(object_selectlist.keys())

        while edit_object_response != responselist[0]:
            print("種類を選択 [ 数値 ][ 文字列 ]")
            print(object_selectlist)
            object_user_select = str(sys.stdin.readline().rstrip())

            use_index = np.where(object_selectlist == object_user_select)  # 居場所は二次元配列で返されるので
            if not use_index[0] is None:
                thislayer, edit_object_response = object_selectlist[use_index[0][0]][2](thislayer, thislayer_reobj_now, responselist, operation_list, elements)
            # 連想配列もどきの取得部分↑

            # 開始地点で整理する
        thislayer.retention_object = sorted(thislayer.retention_object, key=lambda x: x.staend_property[0], reverse=False)

        operation_list["CUI"]["printlayer"]["CentralRole"].viaAll(all_elements)

        return thislayer

    def nothing(self, thislayer, thislayer_reobj_now, responselist, operation_list, elements):
        return thislayer, responselist[0]

    def video(self, thislayer, thislayer_reobj_now, responselist, operation_list, elements):
        print("動画ファイルを入力...")
        os.system("pwd")
        os.system("ls")
        inp_in = str(sys.stdin.readline().rstrip())
        thislayer, edit_object_response = operation_list["set"]["input_video_image"]["CentralRole"].video_image(thislayer, thislayer_reobj_now, responselist, operation_list, elements, inp_in, "video")

        if thislayer.retention_object[thislayer_reobj_now].staend_property[0] == None:
            thislayer.retention_object[thislayer_reobj_now].staend_property[0] = 0

        if thislayer.retention_object[thislayer_reobj_now].staend_property[1] == None:
            thislayer.retention_object[thislayer_reobj_now].staend_property[1] = thislayer.retention_object[thislayer_reobj_now].staend_property[0] + thislayer.retention_object[thislayer_reobj_now].unique_property["count"]

        return thislayer, edit_object_response

    def image(self, thislayer, thislayer_reobj_now, responselist, operation_list, elements):
        print("画像ファイルを入力...")
        os.system("pwd")
        os.system("ls")
        inp_in = str(sys.stdin.readline().rstrip())
        thislayer, edit_object_response = operation_list["set"]["input_video_image"]["CentralRole"].video_image(thislayer, thislayer_reobj_now, responselist, operation_list, elements, inp_in, "image")

        return thislayer, edit_object_response

    def text(self, thislayer, thislayer_reobj_now, responselist, operation_list, elements):
        print("テキストを生成")
        print("生成したいテキストを入力")
        print("制御文字 : [ サイズ変更 : <s100> ] [ 色の変更 : <R255G255B255> ] [ 隙間を生成 : <px0py0>")
        inp_in = str(sys.stdin.readline().rstrip())
        thislayer = operation_list["set"]["input_text"]["CentralRole"].main(inp_in, thislayer, thislayer_reobj_now, elements, operation_list)

        return thislayer, responselist[0]

    def shape(self, thislayer, thislayer_reobj_now, responselist, operation_list, elements):
        return thislayer, responselist[0]

    def effect(self, thislayer, thislayer_reobj_now, responselist, operation_list, elements):
        print("エフェクトを選択")
        print(list(operation_list["plugin"]["effect"].keys()))
        inp_plugin = str(sys.stdin.readline().rstrip())
        if not inp_plugin in operation_list["plugin"]["effect"].keys():
            print("返却")
            return thislayer, responselist[1]

        thislayer = operation_list["set"]["input_plugin"]["CentralRole"].main(thislayer, elements, operation_list, inp_plugin)
        return thislayer, responselist[0]

    def new_obj(self, thislayer, operation_list, all_elements, elements):
        userselect_time = [0, 0]
        print("開始する時間を入力")
        userselect_time[0] = operation_list["CUI"]["timeselect"]["CentralRole"].main(all_elements.editor_info[2])

        print("終了する時間を入力")
        userselect_time[1] = operation_list["CUI"]["timeselect"]["CentralRole"].main(all_elements.editor_info[2])

        userselect_time.sort()

        print(thislayer.retention_object)
        thislayer = operation_list["set"]["input_point"]["CentralRole"].Initial_setting(thislayer, elements, userselect_time)
        thislayer_reobj_now = int(len(thislayer.retention_object)) - 1
        # 操作すオブジェクトを最新のものにする

        return thislayer, thislayer_reobj_now
