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

    def main(self, thisobject, all_elements, operation_list):

        # try:
        print("どのエフェクトを選択するのか入力 [ 数値 ] [ 0 から ] [ 0 は座標などの基礎情報 ]")
        print("現在" + str(int(len(thisobject.effects)) + 1) + "コ確認")

        user_select = int(sys.stdin.readline().rstrip())

        if user_select > int(len(thisobject.effects)):
            print("それは存在しない")
            return thisobject

        print("どの中間点を選択するのか入力 [ 数値 ] [ 空白で新規作成 ]")
        user_select_point = str(sys.stdin.readline().rstrip())

        if user_select_point > int(len(thisobject.effects[user_select])) or int(len(user_select_point)) == 0:
            # 新規作成の場合、ひとつ前のやつから複製して形をコーピー、それを編集という形にすれば良い
            # 一つもない、っていうのはあり得ないはず
            print("存在しないので新規作成")
            print("作成する時間を入力")
            maketime = operation_list["CUI"]["timeselect"]["Center"].main(all_elements)

            thisobject = operation_list["set"]["input_point"]["Center"].several_setting(thisobject, user_select, maketime)

            # hisobject.effects[user_select].effectPoint[-1] =

        # except:
        #    print("数字以外いれんな " + str(sys.exc_info()))
