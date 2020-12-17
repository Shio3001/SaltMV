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


class CentralRole:
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

                if user_select > int(len(thisobject.effects)) - 1:
                    print("それは存在しない")
                    return thislayer
            except:
                user_select = -1

        print("中間点ではなく、各エフェクト固定設定を編集しますか？ [ y / n ]")
        user_select_Fixed = str(sys.stdin.readline().rstrip())

        if user_select_Fixed == "y":
            various_fixed = thislayer.retention_object[userselect_object].effects[user_select].various_fixed
            various_fixed = self.edit_Fixed(various_fixed, operation_list)
            thislayer.retention_object[userselect_object].effects[user_select].various_fixed = various_fixed
            return thislayer

        print("どの中間点を選択するのか入力 [ 数値 ] [ 空白で新規作成 ] [ 0 から ]")
        user_select_point = str(sys.stdin.readline().rstrip())

        # 文字が入力されているかつ、存在している範囲ということを検出

        print("開始・終了地点 : " + str(thisobject.staend_property))

        if not user_select_point:  # 文字が入力されていない場合
            print("新規作成 < not user_select_point >")
            thisobject = self.newpoint(thisobject, operation_list, user_select, all_elements)
            edit_select_point = int(len(thisobject.effects[user_select].effectPoint)) - 1
            thisobject.effects[user_select].effectPoint[edit_select_point] = self.editpoint(thisobject.effects[user_select].effectPoint[edit_select_point], operation_list)

        if user_select_point:  # 文字が入力されている場合
            if 0 <= int(user_select_point) <= int(len(thisobject.effects[user_select].effectPoint)) - 1:
                print("既存編集 < user_select_point >")
                thisobject.effects[user_select].effectPoint[int(user_select_point)] = self.editpoint(thisobject.effects[user_select].effectPoint[int(user_select_point)], operation_list)
            else:  # 文字が入力されているけど範囲内ではない場合
                print("新規作成 < user_select_point else >")
                thisobject = self.newpoint(thisobject, operation_list, user_select, all_elements)
                edit_select_point = int(len(thisobject.effects[user_select].effectPoint)) - 1
                thisobject.effects[user_select].effectPoint[edit_select_point] = self.editpoint(thisobject.effects[user_select].effectPoint[edit_select_point], operation_list)

        print("point設定 返却")
        thisobject.effects[user_select].effectPoint = sorted(thisobject.effects[user_select].effectPoint, key=lambda x: x["time"], reverse=False)

        print(thisobject.effects[user_select].effectPoint)

        thislayer.retention_object[userselect_object] = copy.deepcopy(thisobject)

        del thisobject

        return thislayer

    def newpoint(self, thisobject, operation_list, user_select, all_elements):
        print("存在しないので新規作成")
        print("作成する時間を入力")
        maketime = operation_list["CUI"]["timeselect"]["CentralRole"].main(all_elements.editor_info[2])
        thisobject = operation_list["set"]["input_point"]["CentralRole"].several_setting(thisobject, operation_list, user_select, maketime)

        return thisobject

    def edit_Fixed(self, various_fixed, operation_list):
        various_fixed = self.editpoint(various_fixed, operation_list)
        print(various_fixed)
        return various_fixed

    def editpoint(self, thisobject_effectPoint, operation_list):

        print("すでに作成済みのものを編集")
        print(thisobject_effectPoint)
        user_select = ["0", "0"]

        while user_select[0] != "exit":
            print("編集するものを入力 [ 文字列 ] [ 確定は : exit ]")
            user_select[0] = str(sys.stdin.readline().rstrip())

            if user_select[0] == "exit":
                break

            try:
                print("変更後の数値を入力 [ 数値 ]")
                user_select[1] = int(sys.stdin.readline().rstrip())
                thisobject_effectPoint = operation_list["set"]["input_point"]["CentralRole"].edit_setting(thisobject_effectPoint, user_select)
                print("変換処理終わり")
                print("")
            except:
                print("数値以外を入れないで")
                print("")

        return thisobject_effectPoint
