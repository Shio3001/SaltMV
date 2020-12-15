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

from auxiliary import directory_conversion as dircon
from auxiliary import effect_auxiliary

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
from data_output import obj_substantial

from doc_save import make_save

import elements
import importlib

if __name__ == "__main__":
    print("コマンドライン からの入力を確認")

# 主な処理を連想配列にぶち込む ,連想配列を指定したらその処理持ってこれるようになりよ
operation_list = {"set": {}, "out": {}, "CUI": {}, "save": {}, "other": {}, "plugin": {}}
operation_list["set"]["input_point"] = {"CentralRole": input_point.CentralRole()}  # 中間点を設定する
operation_list["set"]["input_video_image"] = {"CentralRole": input_video_image.CentralRole()}  # 動画・画像の読み込みを行う
operation_list["set"]["input_text"] = {"CentralRole": input_text.CentralRole()}  # テキストの読み込みを行う
operation_list["set"]["new_layer"] = {"CentralRole": new_layer.CentralRole()}
operation_list["out"]["output_video_image"] = {"CentralRole": output_video_image.CentralRole()}  # 動画と画像の場合の出力をまとめる
operation_list["out"]["frame_process"] = {"CentralRole": frame_process.CentralRole()}  # フレームごとの処理を書いておく
operation_list["out"]["current_location"] = {"CentralRole": current_location.CentralRole()}  # 中間点から現在の居場所を算出する
operation_list["out"]["obj_substantial"] = {"CentralRole": obj_substantial.CentralRole()}  # 中間点から現在の居場所を算出する
operation_list["save"]["make_save"] = {"CentralRole": make_save.CentralRole()}
operation_list["CUI"]["usersetpoint"] = {"CentralRole": usersetpoint.CentralRole()}
operation_list["CUI"]["printlayer"] = {"CentralRole": printlayer.CentralRole()}
operation_list["CUI"]["layerselect"] = {"CentralRole": layerselect.CentralRole()}
operation_list["CUI"]["seteditsize"] = {"CentralRole": seteditsize.CentralRole()}
operation_list["CUI"]["timeselect"] = {"CentralRole": timeselect.CentralRole()}
operation_list["CUI"]["makeobject"] = {"CentralRole": makeobject.CentralRole()}
operation_list["other"]["dircon"] = {"CentralRole": dircon.CentralRole()}
operation_list["other"]["effect_auxiliary"] = {"Calculation": effect_auxiliary.Calculation()}
# otherには補助的な計算ファイルを挿入する
# plugin > file

plugin_path = operation_list["other"]["dircon"]["CentralRole"].main("plugin/")
plugin_file = os.listdir(plugin_path)  # ファイル・ディレクトリ取得
plugin_list = [f for f in plugin_file if os.path.isdir(os.path.join(plugin_path, f))]  # ディレクトリのみにする

for plugin_name in plugin_list:
    operation_list["plugin"][str(plugin_name)] = {}  # プラグインの下のファイルによる連想配列生成
    file_path = operation_list["other"]["dircon"]["CentralRole"].main("plugin/" + str(plugin_name) + "/")  # ファイル一覧
    print(file_path)

    file_list = list(map(str, os.listdir(file_path)))

    for file_name in file_list:
        if file_name[-3:] == ".py":
            path = plugin_path.replace('/', '.') + str(plugin_name) + "." + file_name.replace('.py', '')  # /を.に、.pyを消去する
            import_data = importlib.import_module(path)
            operation_list["plugin"][str(plugin_name)][str(file_name.replace('.py', ''))] = import_data


print(operation_list)


class CentralRole:
    def __init__(self):

        self.all_elements = elements.AllElements()  # 全てを司るもの

        self.main_user_CentralRole = main_user.CentralRole()  # ユーザー操作を司る

        self.responselist = ["終了", "問題なし", "問題あり"]  # main.pyに戻ってくる時の応答リスト

    def main(self):

        user_next = " "

        while user_next != self.responselist[0]:
            self.all_elements, user_next = self.main_user_CentralRole.usernextselect(self.responselist, copy.deepcopy(self.all_elements), elements, operation_list)  # 次の選択を担うファイルへ送信
            print("")
            print("********************************")

            print("")
            print("現在の状態")
            operation_list["CUI"]["printlayer"]["CentralRole"].viaAll(self.all_elements)
            print("")

            print("********************************")
            print("")

        # sys.exit()


main_CentralRole = CentralRole()
main_CentralRole.main()

sys.exit()

# まだ一回きりしか操作できないようになってる
# git確認4
