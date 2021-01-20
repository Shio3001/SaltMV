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
            """
            user_select = "../test1224/1120"
            self.all_elements, _ = self.basic_ope["save"]["make_save"]["CentralRole"].input(self.all_elements, self.elements, self.basic_ope, user_select)

            select_time = 550
            this_preview = self.basic_ope["out"]["output_video_image"]["CentralRole"].type_preview(
                copy.deepcopy(self.all_elements), self.basic_ope, select_time)

            this_preview = cv2.resize(this_preview, (640, 360))
            self.this_preview_tk = ImageTk.PhotoImage(image=Image.fromarray(this_preview), master=self.main_window.window)

            self.canvas = self.main_window.tk.Canvas(self.main_window.window, highlightthickness=0, width=640, height=360)
            self.canvas.place(x=0, y=0)
            self.canvas.pack()
            self.canvas.create_image(320, 180, image=self.this_preview_tk)

            """

            # あーキャンバス内での座標計算は左上だけど、物を配置するときにはものの中央で考えないといけないらしい
            # canvas.pack()

        main_menubar_list = [
            ("ファイル", [("終了", window_exit), ("新規", project_new), ("開く", project_open), ("保存", project_save), ("上書き", project_overwrite_save)]),
            ("ウインドウ", [("タイムライン", window_exit)]),
            ("環境設定", [("基本設定", window_exit)]),
            ("動作確認", [("プレビュー", preview)])
        ]

        display_size = self.main_window.display_size_get()
        self.main_window.window_title_set("メインウインドウ")
        size = [640, 360]
        self.main_window.window_size_set(size)
        self.main_window.menubar_set(main_menubar_list)

        test_button = self.main_window.new_parts(parts_name="button")

        def test1(event):
            test_button.edit_canvas_position(width_position=test_button.canvas_position[0] + 20)

        #test_button.edit_canvas_size(width_size=100, height_size=100)
        test_button.canvas_for_event(processing=test1, user_event="Button-1")

        test_box = self.main_window.new_parts(parts_name="textbox")

        return self.main_window
