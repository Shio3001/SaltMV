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

    # def all_elements_data(self):
    #    self.all_elements = all_elements

    def main(self, all_elements, elements, internal_operation, app_name):

        #self.all_elements = all_elements

        #all_elements_data = AllElementsDATA(send_all_elements, internal_operation)

        expansion_keys = internal_operation["plugin"]["expansion"].keys()
        expansion_list = {}

        GUI_UI = internal_operation["plugin"]["GUI_UI"]

        internal_operation["edit_data"].set_get(data=all_elements)

        base_data = {"ope": internal_operation,
                     "el": elements,
                     "ui": GUI_UI,
                     "base_color": GUI_base_color,
                     "alpha_color": GUI_alpha_color
                     }

        send_main = internal_operation["plugin"]["other"]["window_data"].SendWindowData(None, base_data)
        expansion_list["main"] = internal_operation["plugin"]["expansion"][GUI_main_name].InitialValue(send_main).main()

        for key in list(expansion_keys):
            print(key)
            if key != GUI_main_name:
                send_sub = internal_operation["plugin"]["other"]["window_data"].SendWindowData(expansion_list["main"].window, base_data)
                expansion_list[key] = internal_operation["plugin"]["expansion"][key].InitialValue(send_sub).main()

        internal_operation["log"].write("mainloop開始")
        expansion_list["main"].window.mainloop()
        internal_operation["log"].write("mainloop終了")

        print("GUI終了")
        return


"""
class AllElementsDATA:
    def __init__(self, send_all_elements, internal_operation):
        self.all_elements = send_all_elements
        internal_operation["log"].write("all_elements GUI登録")
"""
