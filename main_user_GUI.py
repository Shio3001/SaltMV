# coding:utf-8
import sys
import numpy as np
import os
import copy

GUI_main_name = "GUI_main"


class GUI:
    def __init__(self, all_data):
        self.all_data = all_data

    def main(self):
        expansion_keys = self.all_data.operation["plugin"]["expansion"].keys()
        expansion_list = {}

        UI_parts = self.all_data.operation["plugin"]["GUI_UI"]
        UI_auxiliary = self.all_data.operation["plugin"]["other"]["UI_data"]

        send_main = self.all_data.operation["plugin"]["other"]["window_data"].SendWindowData(None, self.all_data, UI_parts, UI_auxiliary)
        expansion_list["main"] = self.all_data.operation["plugin"]["expansion"][GUI_main_name].InitialValue(send_main).main()

        for key in list(expansion_keys):
            print(key)
            if key != GUI_main_name:
                send_sub = self.all_data.operation["plugin"]["other"]["window_data"].SendWindowData(expansion_list["main"].window, self.all_data, UI_parts, UI_auxiliary)
                expansion_list[key] = self.all_data.operation["plugin"]["expansion"][key].InitialValue(send_sub).main()

        self.all_data.operation["log"].write("mainloop開始")
        expansion_list["main"].window.mainloop()
        self.all_data.operation["log"].write("mainloop終了")

        print("GUI終了")
        return
