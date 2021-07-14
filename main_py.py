# coding:utf-8
from pysrc.Internal_operation.rendering_py import rendering_point
from pysrc.Internal_operation.rendering_py import rendering_frame
from pysrc.Internal_operation.rendering_py import rendering_main
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

from pysrc import main_user_CUI  # GUI処分 CUI中継操作
from pysrc import main_user_GUI
from pysrc import log
from pysrc import error
from pysrc.chord_tool import file_path
from pysrc import edit_data_control
from pysrc import UI_control
from pysrc import undo
from pysrc.chord_tool import class_var_to_dict
from cppsrc.video import video_main
from pysrc import synthetic

from media_input.video_image import control


now_path = os.getcwd()
start_time = datetime.datetime.now()
all_data = edit_data_control.Storage(now_path)
all_UI_data = UI_control

operation = {}

operation["rendering_py"] = {}
operation["rendering_py"]["main"] = rendering_main.Rendering()
operation["rendering_py"]["frame"] = rendering_frame.Rendering()
operation["rendering_py"]["point"] = rendering_point.PointAnalysis()

operation["video_image"] = control.Control_Video_Image()

operation["cppsrc"] = {}
operation["cppsrc"]["video_main"] = video_main

operation["class_dict"] = class_var_to_dict.ClassVarToDict().get
operation["file_path"] = file_path.DirectoryPath()
operation["log"] = log.LogPrint(operation["file_path"])
operation["log"].stop(True)
operation["log"].write("ログ起動")
operation["error"] = error.ErrorAction(operation["log"])

this_name = str(os.path.basename(__file__))
py_path = (os.path.abspath(__file__)).replace(this_name, '')

for i in range(2):
    file_type = ""
    file_py_cpp = ""
    plugin_dict_name = ""
    if i == 0: #python
        file_py_cpp = "pysrc"
        file_type = ".py"
        plugin_dict_name = "plugin"
    if i == 1: #cpp
        file_py_cpp = "cppsrc"
        file_type = ".so" 
        plugin_dict_name = "cpp_plugin"

    plugin_path = os.path.join(py_path.replace(this_name, ''), file_py_cpp,"plugin")
    operation["log"].write(now_path)
    operation["log"].write(py_path)
    operation["log"].write(plugin_path)

    plugin_inside = os.listdir(plugin_path)  # pluginfolder内のアイテムを全取得
    plugin_folder = [p for p in plugin_inside if os.path.isdir(os.path.join(plugin_path, p))]  # Folderにしぼりこむ

    operation[plugin_dict_name] = {}
    for plugin_folder_name in plugin_folder:  # Folder分だけまわす

        pl_section_inside = os.listdir(os.path.join(plugin_path, plugin_folder_name))  # pluginfolder内のアイテムを全取得
        pl_section_inside_list = [f for f in pl_section_inside if os.path.isfile(os.path.join(plugin_path, plugin_folder_name, f))]

        operation[plugin_dict_name][str(plugin_folder_name)] = {}

        for file_name in pl_section_inside_list:  # ファイルごとの処理
            file_path = os.path.join(plugin_path, plugin_folder_name, file_name)  # pluginの絶対パス
            path = os.path.relpath(file_path, py_path)
            path_dot = path.replace(file_type, '').replace(all_data.slash, '.')
            
            file_bool = file_name[-1*int(len(file_type)):] == file_type

            if not file_bool:
                continue
            print("plugin lord : {0}".format(file_name))
            import_data = importlib.import_module(path_dot, py_path)

            if str(plugin_folder_name) == "synthetic":
                import_data = import_data.Synthetic()

            final_name = str(file_name.replace(file_type, ''))
            operation[plugin_dict_name][str(plugin_folder_name)][final_name] = import_data

operation["synthetic"] = synthetic.SyntheticControl()


# plugin読み込み終了

def set_operation():
    operation["log"].write(operation)
    operation["synthetic"].set_operation(operation)
    all_data.set_operation(operation)
    operation["rendering_py"]["main"].set(operation,all_data.scene)

set_operation()
operation["undo"] = undo.UndoStack(all_data)

#all_data.main_path = now_path
print(all_data.main_path)


class CentralRole:
    def __init__(self):
        pass

    def main(self):

        read_time = datetime.datetime.now() - start_time
        operation["log"].write("読込時間: {0}".format(read_time))

        self.main_GUI()

        """

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
        """

        return

    def main_CUI(self):
        main_user_CUI.CUI(all_data).main()  # 次の選択を担うファイルへ送信
        return

    def main_GUI(self):
        main_user_GUI.GUI(all_data, all_UI_data).main()  # 次の選択を担うファイルへ送信
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
