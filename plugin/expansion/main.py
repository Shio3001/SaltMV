# coding:utf-8
import sys
import os
import copy

import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont


class InitialValue:
    def __init__(self, data):
        self.main_window = data
        self.basic_ope = data.base_data["操作"]
        self.all_elements = data.base_data["記録"]
        self.elements = data.base_data["基本"]

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
            user_select = "/Users/maruyama/Programs/test1222/1434.json"
            self.all_elements, self.save_location = self.basic_ope["save"]["make_save"]["CentralRole"].input(self.all_elements, self.elements, self.basic_ope, user_select)

            select_time = 100
            this_preview = self.basic_ope["out"]["output_video_image"]["CentralRole"].type_preview(
                copy.deepcopy(self.all_elements), self.basic_ope, select_time)

            this_preview = cv2.resize(this_preview, (320, 180))
            self.this_preview_tk = ImageTk.PhotoImage(image=Image.fromarray(this_preview), master=self.main_window.window)

            #preview_label = Label(self.main_window.window)
            # preview_label.configure(image=this_preview)
            #Label(self.main_window.window, image=this_preview).pack()

            canvas = self.main_window.tk.Canvas(self.main_window.window, width=320, height=180)
            canvas.pack()
            canvas.create_image(0, 0, anchor=self.main_window.tk.NW, image=self.this_preview_tk)
            # canvas.pack()

        main_menubar_list = [
            ("ファイル", [("終了", window_exit), ("新規", project_new), ("開く", project_open), ("保存", project_save), ("上書き", project_overwrite_save)]),
            ("ウインドウ", [("タイムライン", window_exit)]),
            ("環境設定", [("基本設定", window_exit)]),
            ("動作確認", [("プレビュー", preview)])
        ]

        display_size = self.main_window.display_size_get()
        self.main_window.window_title_set("メインウインドウ")
        size = [500, 500]
        self.main_window.window_size_set(size)
        self.main_window.menubar_set(main_menubar_list)

        return self.main_window


class CentralRole:
    pass
