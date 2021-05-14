# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].TimeSearch.time_search
        self.parameter_ui_list = {}

    def main(self):
        self.data.window_title_set("タイムライン設定")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter")
        self.data.edit_canvas_size("parameter", x=1000, y=1000)

        def element_lord(send):
            elements, now_f = send

            for e in elements.values():

                print("A")

                for p in self.parameter_ui_list.values():
                    p.del_territory()
                self.parameter_ui_list = {}

                ui_id = self.data.all_data.elements.make_id("parameter")
                before_point, next_point = self.time_search(now_f, e)

                if next_point is None:
                    for pk_b, pv_b in zip(before_point.keys(), before_point.values()):
                        if "time" in before_point.keys() and not pk_b == "time":
                            self.parameter_ui_list[ui_id] = self.data.new_parts("parameter", ui_id, parts_name="parameter")
                            print("new", self.parameter_ui_list[ui_id], ui_id, self.parameter_ui_list[ui_id].parameter_ui_set)
                            self.parameter_ui_list[ui_id].parameter_ui_set(motion=False, column=0, text=pk_b, text_a=pv_b, text_b=None)

                else:
                    print(before_point, next_point)
                    for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                        if "time" in before_point.keys() and not pk_b == "time":
                            #print(pk_b, pv_b, pk_n, pv_n)
                            self.parameter_ui_list[ui_id] = self.data.new_parts("parameter", ui_id, parts_name="parameter")
                            self.parameter_ui_list[ui_id].parameter_ui_set(motion=True, column=0, text=pk_b, text_a=pv_b, text_b=pv_n)

                for vk, vv in zip(e.various_fixed.keys(), e.various_fixed.values()):
                    ui_id_various_fixed = ui_id + "various_fixed"
                    print(vk, vv)
                    self.parameter_ui_list[ui_id_various_fixed] = self.data.new_parts("parameter", ui_id_various_fixed, parts_name="parameter")
                    self.parameter_ui_list[ui_id_various_fixed].parameter_ui_set(motion=False, column=0, text=vk, text_a=vv, text_b=None)

                print("B", self.parameter_ui_list)

        self.data.all_data.callback_operation.set_event("media_lord", element_lord)

        #data.element_lord = element_lord


class CentralRole:
    pass
