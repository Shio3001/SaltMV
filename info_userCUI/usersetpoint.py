# coding:utf-8
import sys
import numpy
import os
import copy

# GUI処分ファイル

# オブジェクトが送られてくる
# オブジェクトの中のどこのエフェクトを選択するかをきく
# そのエフェクトの何番目の中間点を選択するかきく(newでもいい)
#  各種の変更数値を確認
# 変更 ←これは分割させる


class Center:
    def __init__(self):
        pass

    def main(self, thislayer, all_elements, operation_list, userselect_object):

        thisobject = thislayer.retention_object[userselect_object]

        print(thisobject.effects)
        # try:
        user_select = -1

        while user_select == -1:

            print("どのエフェクトを選択するのか入力 [ 数値 ] [ 0 から ] [ 0 は座標などの基礎情報 ]")
            print("現在" + str(int(len(thisobject.effects))) + "コ確認")

            try:
                user_select = int(sys.stdin.readline().rstrip())

                if user_select > int(len(thisobject.effects)):
                    print("それは存在しない")
                    return thisobject
            except:
                user_select = -1

        print("どの中間点を選択するのか入力 [ 数値 ] [ 空白で新規作成 ]")
        user_select_point = str(sys.stdin.readline().rstrip())

        # 文字が入力されているかつ、存在している範囲ということを検出

        if user_select_point == False:
            print("新規作成")
            # 新規作成の場合、ひとつ前のやつから複製して形をコーピー、それを編集という形にすれば良い
            # 一つもない、っていうのはあり得ないはず
            thisobject = self.newpoint(thisobject, operation_list, user_select, all_elements)

        else:
            if int(user_select_point) <= int(len(thisobject.effects[user_select].effectPoint)):
                pass

            else:
                thisobject = self.newpoint(thisobject, operation_list, user_select, all_elements)

            # except:
            #    print("数字以外いれんな " + str(sys.exc_info()))

        thisobject.effects[user_select].effectPoint = sorted(thisobject.effects[user_select].effectPoint, key=lambda x: x["time"], reverse=False)

        return thisobject

    def newpoint(self, thisobject, operation_list, user_select, all_elements):
        print("存在しないので新規作成")
        print("作成する時間を入力")
        maketime = operation_list["CUI"]["timeselect"]["Center"].main(all_elements)
        thisobject = operation_list["set"]["input_point"]["Center"].several_setting(thisobject, operation_list, user_select, maketime)

        return thisobject

    def editpoint(self):
        pass
