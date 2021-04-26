# coding:utf-8
import sys
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        #self.all_elements = self.data.all_elements
        #self.elements = self.data.elements
        self.tk = self.data.tk

        self.UI_parts = self.data.UI_parts  # パーツひとつひとつのデータ
        # self.UI_operation = self.data.UI_operation  # パーツを整形するためのデータ

    def main(self):
        self.operation["log"].write("メイン画面起動")

        """
        def get_edit():
            return self.all_elements  # データおくる

        def set_edit(send_all_elements):
            self.all_elements = send_all_elements  # データもら
            return
        """

        def window_exit():
            self.data.window.destroy()

        def project_new():
            pass

        def project_open():
            self.data.all_data.file_input(self.data.all_data.input_debug("open"))
            # self.data.all_data.add_layer_elements()

        def project_save():
            self.data.all_data.file_output(self.data.all_data.input_debug("close"))

        def project_overwrite_save():
            pass

        def preview():
            preview_screen = self.data.new_parts(parts_name="pillow_view")
            preview_screen.size_update("self.all_elements", [1, 2])

        def rendering():
            scene_elements = self.data.all_data.scene()
            #scene_elements.user_select_range = [0, 100]
            self.operation["rendering"]["main"].video_output(self.operation,  scene_elements, "../log/test.mp4")

        main_menubar_list = [("ファイル", "終了", window_exit, "新規作成", project_new, "開く", project_open, "保存", project_save, "上書き", project_overwrite_save, "書き出し", rendering)]
        self.data.menubar_set(main_menubar_list)

        display_size = self.data.display_size_get()
        self.data.window_title_set("メインウインドウ")
        size = [640, 360]
        self.data.window_size_set(size)

        # def window_size_change_event(self):
        #    pass

        #self.data.window_event(processing=window_size_change_event, user_event="Motion")

        return self.data

        # self.data.all_data.add_layer_elements()
