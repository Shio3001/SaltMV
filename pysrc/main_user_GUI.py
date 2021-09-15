# coding:utf-8
import sys
import numpy as np
import os
import copy

GUI_main_name = "GUI_main"


class GUI:
    def __init__(self, edit_data_control, all_UI_control):
        self.edit_data_control = edit_data_control
        self.all_UI_control = all_UI_control

    def main(self):

        expansion_keys = self.edit_data_control.operation["plugin"]["expansion"].keys()
        expansion_list = {}

        UI_parts = self.edit_data_control.operation["plugin"]["GUI_UI"]
        UI_auxiliary = self.edit_data_control.operation["plugin"]["other"]["UI_data"]

        send_main = self.edit_data_control.operation["plugin"]["other"]["window_data"].SendWindowData(None, self.edit_data_control, UI_parts, UI_auxiliary, self.all_UI_control)
        expansion_list["main"] = self.edit_data_control.operation["plugin"]["expansion"][GUI_main_name].InitialValue(send_main).main()

        for key in list(expansion_keys):
            print(key)
            if key != GUI_main_name:
                send_sub = self.edit_data_control.operation["plugin"]["other"]["window_data"].SendWindowData(expansion_list["main"].window, self.edit_data_control, UI_parts, UI_auxiliary, self.all_UI_control)
                expansion_list[key] = self.edit_data_control.operation["plugin"]["expansion"][key].InitialValue(send_sub).main()

        self.edit_data_control.operation["log"].write("mainloop開始")
        expansion_list["main"].window.mainloop()
        self.edit_data_control.operation["log"].write("mainloop終了")

        print("GUI終了")
        return
