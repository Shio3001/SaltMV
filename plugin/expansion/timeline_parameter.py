# coding:utf-8
import sys
import os
import copy
import time


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].TimeSearch.time_search
        self.parameter_ui_list = []

    def main(self):
        self.data.window_title_set("タイムライン設定")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter")
        self.data.edit_canvas_size("parameter", x=1000, y=1000)
        self.data.edit_canvas_position("parameter", x=0, y=0)

        def element_del(sta=0, end=None):
            if end is None:
                end = int(len(self.parameter_ui_list))

            print(sta, end)

            for i in range(sta, end):
                print(i)
                if not self.parameter_ui_list[i].te_name in self.parameter_ui_list[i].canvas_data.territory.keys():
                    continue

                self.parameter_ui_list[i].del_territory()
            del self.parameter_ui_list[sta:end]

        def new_parameter_ui(now):
            if now >= int(len(self.parameter_ui_list)):
                ui_id = self.data.all_data.elements.make_id("parameter_UI")
                self.parameter_ui_list.append([None, None])
                self.parameter_ui_list[now] = self.data.new_parts("parameter", ui_id, parts_name="parameter")

        def element_lord(send):
            elements_effect, now_f = send
            old_elements_len = int(len(self.parameter_ui_list))

            elements_len = int(len(elements_effect.values()))

            print("非同期処理")

            now = 0

            for i, e in enumerate(elements_effect.values()):
                print(i, e)
                before_point, next_point = self.time_search(now_f, e)

                if next_point is None:
                    for pk_b, pv_b in zip(before_point.keys(), before_point.values()):
                        if not "time" in before_point.keys() or pk_b == "time":
                            continue
                        new_parameter_ui(now)
                        self.parameter_ui_list[now].parameter_ui_set(motion=False, column=now, text=pk_b, text_a=pv_b, text_b=None)
                        now += 1

                else:
                    for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                        if not "time" in before_point.keys() or pk_b == "time":
                            continue
                        new_parameter_ui(now)
                        self.parameter_ui_list[now].parameter_ui_set(motion=True, column=now, text=pk_b, text_a=pv_b, text_b=pv_n)
                        now += 1

                for vk, vv in zip(e.various_fixed.keys(), e.various_fixed.values()):
                    new_parameter_ui(now)
                    self.parameter_ui_list[now].parameter_ui_set(motion=False, column=now, text=vk, text_a=vv, text_b=None)
                    now += 1

            now_elements_len = int(len(self.parameter_ui_list))

            if old_elements_len > now:
                len_difference = now
                element_del(sta=len_difference)

        self.data.all_data.callback_operation.set_event("media_lord", element_lord)
        self.data.all_data.callback_operation.set_event("element_del", element_del)

        # data.element_lord = element_lord


class CentralRole:
    pass
