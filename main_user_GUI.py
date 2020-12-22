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

        expansion_keys = internal_operation["plugin"]["expansion"].keys()
        expansion_list = {}

        for key in list(expansion_keys):
            print(key)
            expansion_list[key] = internal_operation["plugin"]["expansion"][key].InitialValue(send_data(main_window)).main()

        main_window.mainloop()

        print("GUI終了")


class send_data:
    def __init__(self, main_window):
        self.tk = tk
        self.menubar_list = {}
        self.window_size = [100, 100]
        self.window_name = "tkinter"
        self.main_window = main_window

        if not self.main_window is None:
            self.window = tk.Toplevel(self.main_window)
        else:
            self.window = tk.Tk()

    def display_size_get(self):
        self.display_size = [self.window.winfo_screenwidth(), self.window.winfo_screenheight()]
        return self.display_size

    def window_size_set(self, send):
        if not send is None:
            self.window_size = send
        self.window.resizable(width=True, height=True)
        self.window.geometry("{0}x{1}".format(self.window_size[0], self.window_size[1]))

    def window_title_set(self, send):
        if not send is None:
            self.window_name = send
        self.window.title(self.window_name)

    def menubar_set(self, send):
        if not send is None:
            self.menubar_list = send

        window_menubar = tk.Menu(self.window)
        self.window.config(menu=window_menubar)
        for bar in self.menubar_list:
            window_menubar_bar = tk.Menu(window_menubar, tearoff=0)
            window_menubar.add_cascade(label=bar[0], menu=window_menubar_bar)
            for tab in bar[1]:
                window_menubar_bar.add_command(label=tab[0], command=tab[1])

    def main(self):
        def window_exit():
            self.window.destroy()
            print("終了")

        self.window.mainloop()
