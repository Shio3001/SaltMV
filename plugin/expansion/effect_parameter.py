# coding:utf-8
import sys
import os
import copy
import datetime


class TextReceivePoint:
    def __init__(self, data, media_id, effect_id, effect_uuid_key, val_key, int_type=None):
        self.data = data
        self.media_id = media_id
        self.effect_id = effect_id
        self.effect_uuid_key = effect_uuid_key
        self.val_key = val_key
        self.int_type = int_type

    def text_func(self, text):
        if self.int_type:
            text = int(text)

        self.data.all_data.edit_key_frame_val(self.media_id, self.effect_id, self.effect_uuid_key, self.val_key, text)
    #obj_id, effect_id, various_fixed_key, various_fixed_val

    #send.media_id, element.effect_id, left_key, pk_b, int(text)
    #send.media_id, element.effect_id, right_key, pk_n, int(text)


class TextReceiveVariousFixed:
    def __init__(self, data, media_id, effect_id, various_fixed_key):
        self.data = data
        self.media_id = media_id
        self.effect_id = effect_id
        self.various_fixed_key = various_fixed_key
        #self.int_type = int_type

    def text_func(self, text):
        self.data.all_data.edit_various_fixed(self.media_id, self.effect_id, self.various_fixed_key, text)


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
            before_point, next_point, left_key, right_key = self.time_search(self.push_f, element, effect_point_internal_id_time, key_get=True)
            print("before_point, next_point", before_point, next_point)
            if next_point is None:
                for pk_b, pv_b in zip(before_point.keys(), before_point.values()):
                    if pk_b in self.data.all_data.effect_point_default_keys:
                        continue
                    #print("pk_b, pv_b", pk_b, pv_b)
                    left = TextReceivePoint(self.data, send.media_id, element.effect_id, left_key, pk_b, int_type=True)
                    self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=pk_b, text_a=pv_b, text_b=None, text_a_return=left.text_func)
                    self.now += 1

            else:
                for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                    if pk_b in self.data.all_data.effect_point_default_keys:
                        continue

                    left = TextReceivePoint(self.data, send.media_id, element.effect_id, left_key, pk_b, int_type=True)
                    right = TextReceivePoint(self.data, send.media_id, element.effect_id, right_key, pk_n, int_type=True)
                    self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    #print("pk_b, pv_b, pk_n, pv_n", pk_b, pv_b, pk_n, pv_n)
                    self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=True, column=self.now, text=pk_b, text_a=pv_b, text_b=pv_n, text_a_return=left.text_func, text_b_return=right.text_func)
                    self.now += 1

            for vk, vv in zip(element.various_fixed.keys(), element.various_fixed.values()):

                text = TextReceiveVariousFixed(self.data, send.media_id, element.effect_id, vk)
                self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=vk, text_a=vv, text_b=None, text_a_return=text.text_func, text_fixed=True)
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
