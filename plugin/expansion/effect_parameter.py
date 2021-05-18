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
        self.parameter_ui_list = []
        self.now = 0
        self.now_f = 0

    def main(self):
        self.data.window_title_set("タイムライン設定")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter")
        self.data.edit_canvas_size("parameter", x=1000, y=1000)
        self.data.edit_canvas_position("parameter", x=0, y=0)

        def make(i, e):
            # for i, e in enumerate(elements_effect.values()):
            print(i, e)
            before_point, next_point = self.time_search(self.now_f, e)

            if next_point is None:
                for pk_b, pv_b in zip(before_point.keys(), before_point.values()):
                    if not "time" in before_point.keys() or pk_b == "time":
                        continue
                    new_parameter_ui(self.now)
                    self.parameter_ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=pk_b, text_a=pv_b, text_b=None)
                    self.now += 1

            else:
                for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                    if not "time" in before_point.keys() or pk_b == "time":
                        continue
                    new_parameter_ui(self.now)
                    self.parameter_ui_list[self.now].parameter_ui_set(motion=True, column=self.now, text=pk_b, text_a=pv_b, text_b=pv_n)
                    self.now += 1

            for vk, vv in zip(e.various_fixed.keys(), e.various_fixed.values()):
                new_parameter_ui(self.now)
                self.parameter_ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=vk, text_a=vv, text_b=None)
                self.now += 1

        def element_lord(i, e):

            self.now = 0
            old_elements_len = int(len(self.parameter_ui_list))
            make(i, e)
            now_elements_len = int(len(self.parameter_ui_list))

            if old_elements_len > self.now:
                len_difference = self.now
                element_del(sta=len_difference)

            self.data.window.update()

            self.data.all_data.threading_lock.release()

        self.data.all_data.callback_operation.set_event("media_lord", element_lord)
        self.data.all_data.callback_operation.set_event("element_del", element_del)

        # data.element_lord = element_lord


class CentralRole:
    pass
