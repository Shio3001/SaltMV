# coding:utf-8
import sys
import os
import copy


from PIL import Image, ImageDraw, ImageFilter, ImageTk
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class InitialValue:
    def __init__(self, data):
        self.main_window = data
        self.main_ope = data.base_data["操作"]

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
            select_time = 100
            this_preview = self.main_window.internal_operation["out"]["output_video_image"]["CentralRole"].type_preview(
                copy.deepcopy(self.main_ope.all_elements), self.main_ope.self.internal_operation, select_time)

            canvas.create_image(20, 20, anchor="nw", image=this_preview)

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

        canvas = self.main_window.tk.Canvas(self.main_window.window, width=320, height=180)
        canvas.pack()

        return self.main_window


class CentralRole:
    pass
