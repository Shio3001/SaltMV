# coding:utf-8
import sys
import numpy as np
import os
import copy

GUI_main_name = "GUI_main"
GUI_base_color = "#1a1a1a"
GUI_alpha_color = "#000000"


class CentralRole:
    def __init__(self):
        pass

    def main(self, all_elements, elements, internal_operation, app_name):

        expansion_keys = internal_operation["plugin"]["expansion"].keys()
        expansion_list = {}

        GUI_UI = internal_operation["plugin"]["GUI_UI"]

        base_data = [internal_operation, all_elements, elements, GUI_UI, GUI_base_color, GUI_alpha_color]

        send_main = internal_operation["plugin"]["other"]["window_data"].SendWindowData(None, base_data)
        expansion_list["main"] = internal_operation["plugin"]["expansion"][GUI_main_name].InitialValue(send_main).main()

        for key in list(expansion_keys):
            print(key)
            if key != GUI_main_name:
                send_sub = internal_operation["plugin"]["other"]["window_data"].SendWindowData(expansion_list["main"].window, base_data)
                expansion_list[key] = internal_operation["plugin"]["expansion"][key].InitialValue(send_sub).main()

        print("mainloop開始")
        expansion_list["main"].window.mainloop()
        print("mainloop終了")

        print("GUI終了")
        return
