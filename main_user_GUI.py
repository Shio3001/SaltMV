# coding:utf-8
import sys
import numpy as np
import os
import copy
import tkinter as tk


class CentralRole:
    def __init__(self):
        pass

    def main(self, all_elements, elements, internal_operation, app_name):
        expansion_keys = internal_operation["plugin"]["expansion"].keys()
        expansion_list = {}

        base_data = {"操作": internal_operation, "記録": all_elements, "基本": elements}
        send_main = SendData(None, base_data)
        expansion_list["main"] = internal_operation["plugin"]["expansion"]["main"].InitialValue(send_main).main()

        for key in list(expansion_keys):
            print(key)
            if key != "main":
                send_sub = SendData(expansion_list["main"].window, base_data)
                expansion_list[key] = internal_operation["plugin"]["expansion"][key].InitialValue(send_sub).main()

        expansion_list["main"].window.mainloop()

        print("GUI終了")


class SendData:
    def __init__(self, main_window, base_data):
        self.tk = tk
        self.menubar_list = {}
        self.window_size = [100, 100]
        self.window_name = "tkinter"
        self.main_window = main_window
        self.base_data = base_data

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
