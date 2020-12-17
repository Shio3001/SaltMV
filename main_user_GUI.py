# coding:utf-8
import sys
import numpy as np
import os
import copy
import tkinter as tk


class CentralRole:
    def __init__(self):
        pass

    def main(self, all_elements, elements, operation_list, app_name):

        root = tk.Tk()
        display = [root.winfo_screenwidth(), root.winfo_screenheight()]
        root.destroy()

        self.main_view = window_make((int(display[0] * 0.4), int(display[0] * 0.4)), "{0}".format(app_name))
        self.editor_view = window_make((int(display[0] * 0.55), int(display[1] * 0.85)), "タイムライン")
        self.main_view.view.mainloop()
        #editor_view = window_make(app_name)


class window_make:
    def __init__(self, display, app_name):
        self.view = tk.Tk()
        self.view.resizable(width=True, height=True)
        self.view.title(app_name)
        self.view.geometry("{0}x{1}".format(display[0], display[1]))
