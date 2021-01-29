# coding:utf-8
import sys
import numpy as np
import os
import copy

from pathlib import Path

import cv2
from PIL import Image, ImageDraw, ImageFilter
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import importlib
import datetime

import main_user_CUI  # GUI処分 CUI中継操作
import main_user_GUI

from auxiliary import directory_conversion as dircon
from auxiliary import effect_auxiliary
from auxiliary import log
# from auxiliary import program_aggregation as prg_aggregation

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
from data_input import input_plugin

from data_output import output_video_image
from data_output import current_location
from data_output import frame_process
from data_output import obj_substantial

from doc_save import make_save

import elements

# pyhton pluginテスト

start_time = datetime.datetime.now()

# 主な処理を連想配列にぶち込む ,連想配列を指定したらその処理持ってこれるようになりよ
operation_list = {"set": {}, "out": {}, "CUI": {}, "save": {}, "useful": {}, "plugin": {}}
operation_list["set"]["input_point"] = {"CentralRole": input_point.CentralRole()}  # 中間点を設定する
operation_list["set"]["input_video_image"] = {"CentralRole": input_video_image.CentralRole()}  # 動画・画像の読み込みを行う
operation_list["set"]["input_text"] = {"CentralRole": input_text.CentralRole()}  # テキストの読み込みを行う
operation_list["set"]["new_layer"] = {"CentralRole": new_layer.CentralRole()}
operation_list["set"]["input_plugin"] = {"CentralRole": input_plugin.CentralRole()}
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
operation_list["useful"]["dircon"] = {"CentralRole": dircon.CentralRole()}
operation_list["useful"]["effect_auxiliary"] = {"Calculation": effect_auxiliary.Calculation()}
# operation_list["useful"]["prg_aggregation"] = {"CentralRole": prg_aggregation.CentralRole()}

# usefulには補助的な計算ファイルを挿入する
# plugin > file

# plugin_path = "plugin"

# pathの指定方法は¥とかじゃなくて..でやれ

this_os = str(os.name)
if this_os == "nt":
    slash = "\\"
else:
    slash = "/"


operation_list["log"] = log.LogPrint(operation_list["useful"]["dircon"]["CentralRole"])

now_path = os.getcwd()
py_path = (os.path.abspath(__file__)).replace('main.py', '')
plugin_path = os.path.join(py_path.replace('main.py', ''), "plugin")

operation_list["log"].write(now_path)
operation_list["log"].write(py_path)
operation_list["log"].write(plugin_path)

plugin_inside = os.listdir(plugin_path)  # pluginfolder内のアイテムを全取得
plugin_folder = [p for p in plugin_inside if os.path.isdir(os.path.join(plugin_path, p))]  # Folderにしぼりこむ

for plugin_folder_name in plugin_folder:  # Folder分だけまわす

    pl_section_inside = os.listdir(os.path.join(plugin_path, plugin_folder_name))  # pluginfolder内のアイテムを全取得
    pl_section_inside_list = [f for f in pl_section_inside if os.path.isfile(os.path.join(plugin_path, plugin_folder_name, f))]

    operation_list["plugin"][str(plugin_folder_name)] = {}

    for file_name in pl_section_inside_list:
        if file_name[-3:] == ".py":
            # path = (plugin_folder_name + "." + file_name.replace('.py', '')).replace(plugin_path, '')
            # operation_list["log"].write("path {0}".format(path))
            #path = os.path.relpath(os.path.join(plugin_path, plugin_folder_name, file_name)).replace(".py", '').replace(slash, '.')

            # plugin_path_relative =
            file_path = os.path.join(plugin_path, plugin_folder_name, file_name)  # pluginの絶対パス
            path = os.path.relpath(file_path, py_path)

            operation_list["log"].write("read : {0}".format(file_path))
            operation_list["log"].write("read : {0}".format(path))

            #operation_list["log"].write(file_path, path, py_path)

            path_dot = path.replace('.py', '').replace(slash, '.')
            # operation_list["log"].write(path_dot)

            import_data = importlib.import_module(path_dot, py_path)
            operation_list["plugin"][str(plugin_folder_name)][str(file_name.replace('.py', ''))] = import_data
            operation_list["log"].write(operation_list)


operation_list["log"].write(operation_list)

app_name = "NankokuMovieMaker"


class CentralRole:
    def __init__(self):

        self.all_elements = elements.AllElements()  # 全てを司るもの

        self.responselist = ["終了", "問題なし", "問題あり"]  # main.pyに戻ってくる時の応答リスト

    def main(self):

        read_time = datetime.datetime.now() - start_time
        operation_list["log"].write("読込時間: {0}".format(read_time))

        if __name__ == "__main__":
            operation_list["log"].write("コマンドライン からの入力を確認")
            if len(sys.argv) == 1:
                main_user_CUI_CentralRole = main_user_CUI.CentralRole()
                self.main_CUI(main_user_CUI_CentralRole)

            elif sys.argv[1] == "CUI":
                main_user_CUI_CentralRole = main_user_CUI.CentralRole()  # ユーザー操作を司る
                self.main_CUI(main_user_CUI_CentralRole)

            elif sys.argv[1] == "GUI":
                main_user_GUI_CentralRole = main_user_GUI.CentralRole()  # ユーザー操作を司る
                self.main_GUI(main_user_GUI_CentralRole)

        else:
            main_user_GUI_CentralRole = main_user_GUI.CentralRole()  # ユーザー操作を司る
            self.main_GUI(main_user_GUI_CentralRole)

        return

    def main_CUI(self, main_user_CUI_CentralRole):

        user_next = " "

        while user_next != self.responselist[0]:
            self.all_elements, user_next = main_user_CUI_CentralRole.usernextselect(self.responselist, copy.deepcopy(self.all_elements), elements, operation_list)  # 次の選択を担うファイルへ送信
            operation_list["log"].write("")
            operation_list["log"].write("********************************")

            operation_list["log"].write("")
            operation_list["log"].write("現在の状態")
            operation_list["CUI"]["printwritelayer"]["CentralRole"].viaAll(self.all_elements)
            operation_list["log"].write("")

            operation_list["log"].write("********************************")
            operation_list["log"].write("")

        # sys.exit()

    def main_GUI(self, main_user_GUI_CentralRole):
        main_user_GUI_CentralRole.main(copy.deepcopy(self.all_elements), elements, operation_list, app_name)  # 次の選択を担うファイルへ送信


main_CentralRole = CentralRole()
main_CentralRole.main()

exit_time = datetime.datetime.now()

operation_time = exit_time - start_time
operation_list["log"].write("開始時間 {0} , 終了時間 : {1} , 操作時間: {2}".format(start_time, exit_time, operation_time))

del operation_list
del main_CentralRole

# os.system("rm -rf " + "tmp")
operation_list["log"].end()
operation_list["log"].write("main 終了")
sys.exit()
