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
        self.GUI_UI = self.main_window.GUI_UI
        self.tk = self.main_window.tk

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

        pos = [0, 0]

        def test1(self):
            pos[0] += 10
            print(pos)

        def test2(self):
            print("mi")

        test = self.GUI_UI["button"].UI_set(text="てすと", position=pos, size=(100, 30), user_event="Button-2", processing=test1)
        test2 = self.GUI_UI["button"].UI_set(text="てすと2", position=(500, 200), size=(200, 30), user_event="Button-1", processing=test2)
        del test
        del test2

        #test = self.tk.Entry()
        #test.place(x=90, y=70, width=150, height=30)

        return self.main_window
