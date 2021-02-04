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
import log
from chord_tool import file_path
import edit_data_control


# pyhton pluginテスト

start_time = datetime.datetime.now()
all_data = edit_data_control.Storage()

# 主な処理を連想配列にぶち込む ,連想配列を指定したらその処理持ってこれるようになりよ

#operation = {"set": {}, "out": {}, "CUI": {}, "save": {}, "useful": {}, "plugin": {}}

# ファイル定義開始
operation = {}
operation["file_path"] = file_path.DirectoryPath()
operation["log"] = log.LogPrint(operation["file_path"])

# plugin読み込み


now_path = os.getcwd()
py_path = (os.path.abspath(__file__)).replace('main.py', '')
plugin_path = os.path.join(py_path.replace('main.py', ''), "plugin")

operation["log"].write(now_path)
operation["log"].write(py_path)
operation["log"].write(plugin_path)

plugin_inside = os.listdir(plugin_path)  # pluginfolder内のアイテムを全取得
plugin_folder = [p for p in plugin_inside if os.path.isdir(os.path.join(plugin_path, p))]  # Folderにしぼりこむ


operation["plugin"] = {}
for plugin_folder_name in plugin_folder:  # Folder分だけまわす

    pl_section_inside = os.listdir(os.path.join(plugin_path, plugin_folder_name))  # pluginfolder内のアイテムを全取得
    pl_section_inside_list = [f for f in pl_section_inside if os.path.isfile(os.path.join(plugin_path, plugin_folder_name, f))]

    operation["plugin"][str(plugin_folder_name)] = {}

    for file_name in pl_section_inside_list:
        if file_name[-3:] == ".py":
            file_path = os.path.join(plugin_path, plugin_folder_name, file_name)  # pluginの絶対パス
            path = os.path.relpath(file_path, py_path)
            path_dot = path.replace('.py', '').replace(all_data.slash, '.')
            import_data = importlib.import_module(path_dot, py_path)
            operation["plugin"][str(plugin_folder_name)][str(file_name.replace('.py', ''))] = import_data

# plugin読み込み終了

operation["log"].write(operation)
#app_name = "NankokuMovieMaker"

all_data.set_operation(operation)


class CentralRole:
    def __init__(self):
        pass

    def main(self):

        read_time = datetime.datetime.now() - start_time
        operation["log"].write("読込時間: {0}".format(read_time))

        if __name__ == "__main__":
            operation["log"].write("コマンドライン からの入力を確認")
            if len(sys.argv) == 1:
                self.main_CUI()

            elif sys.argv[1] == "CUI":
                self.main_CUI()

            elif sys.argv[1] == "GUI":
                self.main_GUI()

        else:
            self.main_GUI()

        return

    def main_CUI(self):
        main_user_CUI.CUI(all_data).main()  # 次の選択を担うファイルへ送信
        return

    def main_GUI(self):
        main_user_GUI.GUI(all_data).main()  # 次の選択を担うファイルへ送信
        return


main_CentralRole = CentralRole()
main_CentralRole.main()
operation["log"].stop(True)
exit_time = datetime.datetime.now()
operation_time = exit_time - start_time
operation["log"].write("開始時間 {0} , 終了時間 : {1} , 操作時間: {2}".format(start_time, exit_time, operation_time))
operation["log"].write("main 終了")
operation["log"].end()

del operation
del main_CentralRole

sys.exit()
