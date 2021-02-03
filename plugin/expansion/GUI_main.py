# coding:utf-8
import sys
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont


class InitialValue:
    def __init__(self, data):
        self.main_window = data
        self.operation = self.main_window.operation
        #self.all_elements = self.main_window.all_elements
        #self.elements = self.main_window.elements
        self.tk = self.main_window.tk

        self.UI_parts = self.main_window.UI_parts  # パーツひとつひとつのデータ
        # self.UI_operation = self.main_window.UI_operation  # パーツを整形するためのデータ

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
            self.main_window.window.destroy()

        def project_new():
            pass

        def project_open():
            pass

        def project_save():
            pass

        def project_overwrite_save():
            pass

        def preview():
            preview_screen = self.main_window.new_parts(parts_name="pillow_view")
            preview_screen.size_update("self.all_elements", [1, 2])

        main_menubar_list = [("ファイル", "終了", window_exit, "新規作成", project_new, "開く", project_open, "保存", project_save, "上書き", project_overwrite_save)]
        self.main_window.menubar_set(main_menubar_list)

        display_size = self.main_window.display_size_get()
        self.main_window.window_title_set("メインウインドウ")
        size = [640, 360]
        self.main_window.window_size_set(size)

        def window_size_change_event(self):
            pass

        self.main_window.window_event(processing=window_size_change_event, user_event="Motion")

        return self.main_window
