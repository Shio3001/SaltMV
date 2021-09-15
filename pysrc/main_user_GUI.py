# coding:utf-8
import sys
import numpy as np
import os
import copy

GUI_main_name = "GUI_main"


class GUI:
    def __init__(self, edit_control_auxiliary, UI_control):
        self.edit_control_auxiliary = edit_control_auxiliary
        self.UI_control = UI_control

    def main(self):

        expansion_keys = self.edit_control_auxiliary.operation["plugin"]["expansion"].keys()
        expansion_list = {}

        UI_parts = self.edit_control_auxiliary.operation["plugin"]["GUI_UI"]
        UI_auxiliary = self.edit_control_auxiliary.operation["plugin"]["other"]["UI_auxiliary"]

        send_main = self.edit_control_auxiliary.operation["plugin"]["other"]["window_auxiliary"].SendWindowData(None, self.edit_control_auxiliary, UI_parts, UI_auxiliary, self.UI_control)
        expansion_list["main"] = self.edit_control_auxiliary.operation["plugin"]["expansion"][GUI_main_name].InitialValue(send_main).main()

        for key in list(expansion_keys):
            print(key)
            if key != GUI_main_name:
                send_sub = self.edit_control_auxiliary.operation["plugin"]["other"]["window_auxiliary"].SendWindowData(expansion_list["main"].window, self.edit_control_auxiliary, UI_parts, UI_auxiliary, self.UI_control)
                expansion_list[key] = self.edit_control_auxiliary.operation["plugin"]["expansion"][key].InitialValue(send_sub).main()

        self.edit_control_auxiliary.operation["log"].write("mainloop開始")
        expansion_list["main"].window.mainloop()
        self.edit_control_auxiliary.operation["log"].write("mainloop終了")

        print("GUI終了")
        return
