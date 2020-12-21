# coding:utf-8
import sys
import numpy as np
import os
import copy
import tkinter as tk

from PIL import Image, ImageDraw, ImageFilter, ImageTk
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class CentralRole:
    def __init__(self):
        pass

    def main(self, all_elements, elements, internal_operation, app_name):
        main_window = tk.Tk()
        display = [main_window.winfo_screenwidth(), main_window.winfo_screenheight()]
        main_window_size = tuple(map(int, (display[0] * 0.4, display[0] * 0.4)))

        def window_exit():
            main_window.destroy()

        def project_new():
            pass

        def project_open():
            pass

        def project_save():
            pass

        def project_overwrite_save():
            pass

        main_menubar_list = [
            ("ファイル", [("終了", window_exit), ("新規", project_new), ("開く", project_open), ("保存", project_save), ("上書き", project_overwrite_save)]),
            ("ウインドウ", [("タイムライン", window_exit)]),
            ("環境設定", [("基本設定", window_exit)])
        ]

        # main_menubar_list = [("ファイル", (["終了", self.exit], ["新規", self.new_project], ["開く", self.open], ["保存", self.save], ["上書き", self.overwrite_save])), ("a", (["i", self.exit]))]
        main_window = self.window_set(main_window, app_name, main_window_size, main_menubar_list)

        expansion_list = internal_operation["plugin"]["expansion"].values()

        for expansion in expansion_list:
            expansion().InitialValue(data(main_window))

        timeline_menubar_list = [
            ("ウインドウ", [("閉じる", exit)])
        ]

        timeline_window_size = tuple(map(int, (display[0] * 0.55, display[1] * 0.8)))
        timeline_window = tk.Toplevel(main_window)
        # timeline_menubar_list = [("タイムライン", (["閉じる", self.exit]))]
        timeline_window = self.window_set(timeline_window, "タイムライン", timeline_window_size, timeline_menubar_list)

        main_window.mainloop()

        print("GUI終了")


class data:
    def __init__(self, main_window):
        self.tk = tk
        self.window = tk.Toplevel(main_window)
        self.menubar_list = {}
        self.window_size = [100, 100]
        self.window_name = "tkinter"
        self.GUI_operation = window_operation_data()


class window_operation_data:
    def display_size_get(self):
        self.display_size = [self.window.winfo_screenwidth(), self.window.winfo_screenheight()]
        return self.display_size

    def window_set(self):
        self.window.resizable(width=True, height=True)
        self.window.title(self.window_name)
        self.window.geometry("{0}x{1}".format(self.window_size[0], self.window_size[1]))

        return self.window

    def window_size_set(self, window):
        return self.window

    def menubar_set(self, window, menubar_list):
        window_menubar = tk.Menu(window)
        self.window.config(menu=window_menubar)
        for bar in menubar_list:
            window_menubar_bar = tk.Menu(window_menubar, tearoff=0)
            window_menubar.add_cascade(label=bar[0], menu=window_menubar_bar)

            for tab in bar[1]:
                window_menubar_bar.add_command(label=tab[0], command=tab[1])

        return self.window
