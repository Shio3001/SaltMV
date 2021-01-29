# coding:utf-8
import sys
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont


class InitialValue:
    def __init__(self, data):
        self.main_window = data
        self.basic_ope = self.main_window.operation
        self.all_elements = self.main_window.all_elements
        self.elements = self.main_window.elements
        self.tk = self.main_window.tk

        self.GUI_UI_parts = self.main_window.GUI_UI_parts  # パーツひとつひとつのデータ
        # self.UI_operation = self.main_window.UI_operation  # パーツを整形するためのデータ

    def main(self):

        self.basic_ope["log"].write("メイン画面起動")

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
            pass

            # あーキャンバス内での座標計算は左上だけど、物を配置するときにはものの中央で考えないといけないらしい
            # canvas.pack()

        main_menubar_list = [("ファイル", "終了", window_exit, "新規作成", project_new, "開く", project_open, "保存", project_save, "上書き", project_overwrite_save)]
        self.main_window.menubar_set(main_menubar_list)

        display_size = self.main_window.display_size_get()
        self.main_window.window_title_set("メインウインドウ")
        size = [640, 360]
        self.main_window.window_size_set(size)

        test_button = self.main_window.new_parts(parts_name="button")

        def test1(event):
            test_button.edit_canvas_position(width_position=test_button.canvas_position[0] + 20)

        #test_button.edit_canvas_size(width_size=100, height_size=100)
        test_button.canvas_event_del(test_button.user_event)

        test_button.canvas_for_event(processing=test1, user_event="Button-1")

        test_box = self.main_window.new_parts(parts_name="textbox")

        return self.main_window
