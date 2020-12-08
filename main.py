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

import directory_conversion as dircon

# set
from user_CUI.Visualization import printlayer
from user_CUI.Visualization import layerselect
from user_CUI.Visualization import seteditsize
from user_CUI.Visualization import timeselect

from user_CUI import usersetpoint  # CUI 操作に関するファイル GUI処分
from user_CUI import makeobject
# from info_userCUI.EditPointFile import edit_point  # CUI 操作に関するファイル GUI処分 set_pointで設定したものを編集するやつ
from data_input import input_point  # 内部処理
from data_input import input_video_image
from data_input import input_text
from data_input import new_layer

from data_output import output_video_image
from data_output import current_location
from data_output import frame_process

from doc_save import make_save

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

#主な処理を連想配列にぶち込む ,連想配列を指定したらその処理持ってこれるようになりよ
operation_list = {"set": {}, "out": {}, "CUI": {}, "save": {}, "other": {}}
operation_list["set"]["input_point"] = {"Center": input_point.Center()}  # 中間点を設定する
operation_list["set"]["input_video_image"] = {"Center": input_video_image.Center()}  # 動画・画像の読み込みを行う
operation_list["set"]["input_text"] = {"Center": input_text.Center()}  # テキストの読み込みを行う
operation_list["set"]["new_layer"] = {"Center": new_layer.Center()}

operation_list["out"]["output_video_image"] = {"Center": output_video_image.Center()}  # 動画と画像の場合の出力をまとめる
operation_list["out"]["frame_process"] = {"Center": frame_process.Center()}  # フレームごとの処理を書いておく

operation_list["out"]["current_location"] = {"Center": current_location.Center()}  # 中間点から現在の居場所を算出する

operation_list["save"]["make_save"] = {"Center": make_save.Center()}
operation_list["CUI"]["usersetpoint"] = {"Center": usersetpoint.Center()}
operation_list["CUI"]["printlayer"] = {"Center": printlayer.Center()}
operation_list["CUI"]["layerselect"] = {"Center": layerselect.Center()}
operation_list["CUI"]["seteditsize"] = {"Center": seteditsize.Center()}
operation_list["CUI"]["timeselect"] = {"Center": timeselect.Center()}
operation_list["CUI"]["makeobject"] = {"Center": makeobject.Center()}

operation_list["other"]["dircon"] = {"Center": dircon.Center()}


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
