# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import main_user_CUI as main_user  # GUI処分 CUI中継操作

# set
from info_userCUI.Visualization import printlayer
from info_userCUI.Visualization import layerselect
from info_userCUI.Visualization import seteditsize
from info_userCUI.Visualization import timeselect

from info_userCUI import usersetpoint  # CUI 操作に関するファイル GUI処分
from info_userCUI import makeobject
# from info_userCUI.EditPointFile import edit_point  # CUI 操作に関するファイル GUI処分 set_pointで設定したものを編集するやつ
from info_input import input_point  # 内部処理
from info_input import input_video_image
from info_input import input_text
# setend

# out

# outend

# 統括ファイル
# from info_toset import info_toset_rally as set_rally  # 設定などを行う(内部)
# from info_userCUI import info_userCUI_rally as userCUI_rally  # 設定などを行う(CUI)
# from info_toout import info_toout_rally as out_rally  # 書き出す


import elements

# GUI処分ファイル・・・GUIにした時に削除するファイル
# CUI中継・・・CUIでの操作を担う部分
#
# 返却時には layer , 状態 でやりとりを行うようにする事
#
# 管理,設定(入力)と生成(出力)は完全分離しろ
#
# CHK_ ・・・保留
# EXC ・・・状態を表す


if __name__ == "__main__":
    print("コマンドライン からの入力を確認")

# 各種ファイルを設定 一度きりやしベタがき
# set_rally_Center = set_rally.Center(main_point)  # 情報入力関連をまとめてやってくれる
# userCUI_rally_Center = userCUI_rally.Center(set_point, edit_point, printlayer, layerselect, seteditsize, timeselect)  # CUI入力関連登録

#主な処理を連想配列にぶち込む ,連想配列を指定したらその処理持ってこれるようになりよ
operation_list = {"set": {}, "out": {}, "CUI": {}}
operation_list["set"]["input_point"] = {"Center": input_point.Center()}
operation_list["set"]["input_video_image"] = {"Center": input_video_image.Center()}
operation_list["set"]["input_text"] = {"Center": input_text.Center()}
# operation_list["out"]["main_point"] = main_point

operation_list["CUI"]["usersetpoint"] = {"Center": usersetpoint.Center()}
#operation_list["CUI"]["edit_point"] = {"Center": edit_point.Center()}
operation_list["CUI"]["printlayer"] = {"Center": printlayer.Center()}
operation_list["CUI"]["layerselect"] = {"Center": layerselect.Center()}
operation_list["CUI"]["seteditsize"] = {"Center": seteditsize.Center()}
operation_list["CUI"]["timeselect"] = {"Center": timeselect.Center()}
operation_list["CUI"]["makeobject"] = {"Center": makeobject.Center()}


print(operation_list)


# out_rally_Center = out_rally.Center()  # 情報出力関連をまとめてやってくれる


class Center:
    def __init__(self):

        self.all_elements = elements.AllElements()  # 全てを司るもの

        self.main_user_Center = main_user.Center()  # ユーザー操作を司る

        self.responselist = ["終了", "問題なし", "問題あり"]  # main.pyに戻ってくる時の応答リスト

    def main(self):

        user_next = " "

        while user_next != self.responselist[0]:
            self.all_elements, user_next = self.main_user_Center.usernextselect(self.responselist, copy.deepcopy(self.all_elements), elements, operation_list)  # 次の選択を担うファイルへ送信
            print("")
            print("********************************")

            print("")
            print("現在の状態")
            operation_list["CUI"]["printlayer"]["Center"].viaAll(self.all_elements)
            print("")

            print("********************************")
            print("")

        # sys.exit()


main_Center = Center()
main_Center.main()

sys.exit()

# まだ一回きりしか操作できないようになってる
# git確認4