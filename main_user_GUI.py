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

    def main(self, all_elements, elements, operation_list, app_name):
        main_window = tk.Tk()
        display = [main_window.winfo_screenwidth(), main_window.winfo_screenheight()]
        main_window_size = tuple(map(int, (display[0] * 0.4, display[0] * 0.4)))
        main_window = self.window_set(main_window, app_name, main_window_size)

        timeline_window_size = tuple(map(int, (display[0] * 0.55, display[1] * 0.8)))
        timeline_window = tk.Toplevel(main_window)
        timeline_window = self.window_set(timeline_window, "タイムライン", timeline_window_size)

        main_menubar = tk.Menu(main_window)
        main_menubar_file = tk.Menu(main_menubar)

        for bar in ("終了", "新規", "開く", "保存", "上書き"):
            main_menubar_file = self.menubar(main_menubar_file, bar)

        main_menubar.add_cascade(label="File", menu=main_menubar_file)

        main_window.config(menu=main_menubar)

        main_window.mainloop()

        print("GUI終了")

    def menubar(self, menubar_bar, menu_str):
        menubar_bar.add_command(label=menu_str)
        return menubar_bar

    def window_set(self, window, window_name, window_size):
        window.resizable(width=True, height=True)
        window.title(window_name)
        window.geometry("{0}x{1}".format(window_size[0], window_size[1]))
        return window
