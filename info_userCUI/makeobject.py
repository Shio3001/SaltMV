# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def main(self, all_elements, elements, thislayer, operation_list, responselist, selectlist):

        # 次のオブジェクトの開始地点と、今のオブジェクトの終了地点を引いて、0以下であればかぶっている判定にしてあげれば勝ち

        userselect_layer_object_num = int(len(thislayer.retention_object))
        # 指定したレイヤーに何個オブジェクトがあるか確認
        thislayer_reobj_now = 0

        if userselect_layer_object_num != 0:
            print("このレイヤーにはすでにオブジェクトが" + str(userselect_layer_object_num) + "コ存在しています")
            print("既存のオブジェクトを変更する場合は、オブジェクト番号を入力 [ 1から ][ 数値 ]")

            try:
                thislayer_reobj_now = int(sys.stdin.readline().rstrip()) - 1
                print("対象オブジェクト: " + str(thislayer_reobj_now + 1))
                print(thislayer.retention_object[thislayer_reobj_now])
            except:  # エラーを起こしたら存在しない扱い、新規作成へと誘導
                print(str(sys.exc_info()))
                thislayer, thislayer_reobj_now = self.new_obj(thislayer, operation_list, all_elements, elements)
        else:
            thislayer, thislayer_reobj_now = self.new_obj(thislayer, operation_list, all_elements, elements)

        edit_object_response = ""
        object_selectlist = {0: "返却", 1: "動画", 2: "画像", 3: "テキスト", 4: "図形", 5: "エフェクト"}
        object_selectlist_keys = list(selectlist.keys())

        while edit_object_response != responselist[0]:
            print("種類を選択 [ 数値 ][ 文字列 ]")
            print(object_selectlist)
            object_user_select = str(sys.stdin.readline().rstrip())

            if object_user_select == object_selectlist[0] or object_user_select == str(object_selectlist_keys[0]):
                break

            if object_user_select == object_selectlist[1] or object_user_select == str(object_selectlist_keys[1]):

                print("動画ファイルを入力...")
                os.system("pwd")
                os.system("ls")
                inp_in = str(sys.stdin.readline().rstrip())
                thislayer, edit_object_response = operation_list["set"]["input_video_image"]["Center"].video(thislayer, thislayer_reobj_now, responselist, inp_in)

                if thislayer.retention_object[thislayer_reobj_now].staend_property[0] == None:
                    thislayer.retention_object[thislayer_reobj_now].staend_property[0] = 0

                if thislayer.retention_object[thislayer_reobj_now].staend_property[1] == None:
                    thislayer.retention_object[thislayer_reobj_now].staend_property[1] = thislayer.retention_object[thislayer_reobj_now].staend_property[0] + thislayer.retention_object[thislayer_reobj_now].unique_property["count"]

            if object_user_select == object_selectlist[2] or object_user_select == str(object_selectlist_keys[2]):
                print("画像ファイルを入力...")
                os.system("pwd")
                os.system("ls")
                inp_in = str(sys.stdin.readline().rstrip())
                thislayer, edit_object_response = operation_list["set"]["input_video_image"]["Center"].image(thislayer, thislayer_reobj_now, responselist, inp_in)

            if object_user_select == object_selectlist[3] or object_user_select == str(object_selectlist_keys[3]):
                print("テキストを生成")
                print("生成したいテキストを入力")
                print("制御文字 : [ サイズ変更 : <s100> ] [ 色の変更 : <R255G255B255> ] [ 隙間を生成 : <px0py0>")
                inp_in = str(sys.stdin.readline().rstrip())
                operation_list["set"]["input_text"]["Center"].main(inp_in, thislayer, thislayer_reobj_now)

            if object_user_select == object_selectlist[4] or object_user_select == str(object_selectlist_keys[4]):
                pass

            if object_user_select == object_selectlist[5] or object_user_select == str(object_selectlist_keys[5]):
                pass

            # 開始地点で整理する
        thislayer.retention_object = sorted(thislayer.retention_object, key=lambda x: x.staend_property[0], reverse=False)

        operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)

        return thislayer

    def new_obj(self, thislayer, operation_list, all_elements, elements):
        userselect_time = [0, 0]
        print("開始する時間を入力")
        userselect_time[0] = operation_list["CUI"]["timeselect"]["Center"].main(all_elements)

        print("終了する時間を入力")
        userselect_time[1] = operation_list["CUI"]["timeselect"]["Center"].main(all_elements)

        userselect_time.sort()

        print(thislayer.retention_object)
        thislayer = operation_list["set"]["input_point"]["Center"].Initial_setting(thislayer, elements, userselect_time)
        thislayer_reobj_now = int(len(thislayer.retention_object)) - 1
        # 操作すオブジェクトを最新のものにする

        return thislayer, thislayer_reobj_now
