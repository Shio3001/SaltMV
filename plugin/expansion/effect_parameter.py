# coding:utf-8
import sys
import os
import copy
import datetime


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].TimeSearch.time_search
        self.now = 0
        self.push_f = 0

    def main(self):
        self.data.window_title_set("タイムライン設定")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter")
        self.data.edit_canvas_size("parameter", x=1000, y=1000)
        self.data.edit_canvas_position("parameter", x=0, y=0)

        self.data.ui_management = self.data.operation["plugin"]["other"]["timeline_UI_management"].UIManagement(self.data)

        def make(send):
            element, effect_point_internal_id_time = send.effect_element, send.effect_point_internal_id_time

            # for i, e in enumerate(elements_effect.values()):
            before_point, next_point = self.time_search(self.push_f, element, effect_point_internal_id_time)

            if next_point is None:
                for pk_b, pv_b in zip(before_point.keys(), before_point.values()):
                    if pk_b in self.data.all_data.effect_point_default_keys:
                        continue
                    self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=pk_b, text_a=pv_b, text_b=None)
                    self.now += 1

            else:
                for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                    if pk_b in self.data.all_data.effect_point_default_keys:
                        continue
                    self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=True, column=self.now, text=pk_b, text_a=pv_b, text_b=pv_n)
                    self.now += 1

            for vk, vv in zip(element.various_fixed.keys(), element.various_fixed.values()):
                self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=vk, text_a=vv, text_b=None)
                self.now += 1

        def element_lord(send):
            #element, effect_point_internal_id_time, now_f, text_a_return, text_b_return = element_send
            element = send.effect_element
            self.data.window_title_set("タイムライン設定 {0}".format(element.effect_name))
            self.now = 0
            self.push_f = send.now_f
            self.data.ui_management.set_old_elements_len()
            make(send)
            self.data.ui_management.del_ignition(self.now)
            self.data.window.update()

        def element_ui_all_del():
            self.now = 0
            self.data.ui_management.set_old_elements_len()
            self.data.ui_management.del_ignition(self.now)

            self.data.window_title_set("タイムライン設定")

        self.data.all_data.callback_operation.set_event("element_ui_all_del", element_ui_all_del)
        self.data.all_data.callback_operation.set_event("element_lord", element_lord)
        self.data.all_data.callback_operation.set_event("element_del", self.data.ui_management.element_del)

        # data.element_lord = element_lord


class CentralRole:
    pass
