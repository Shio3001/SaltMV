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
        # self.parameter_button_ui_list = []
        self.now = 0
        self.now_f = 0

    def main(self):
        self.data.window_title_set("パラメーターコントロール")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter_control")
        self.data.edit_canvas_size("parameter_control", x=220, y=1000)
        self.data.edit_canvas_position("parameter_control", x=0, y=0)

        self.data.ui_management = self.data.operation["plugin"]["other"]["timeline_UI_management"].UIManagement(self.data)

        # def make

        def element_lord_ignition(send):
            # print(elements_effect, option_data)
            key = send.element_key

            if not key in send.effect_group.keys():
                # print("返送")
                return

            print("key", key)

            # send.effect_element = send.effect_group[key]
            send.effect_element = self.data.all_data.effect(send.media_id, key)

            self.data.all_data.callback_operation.event("element_lord", info=(send))

        def new_button_for_parameter_control():
            ui_id = self.data.all_data.elements.make_id("parameter_UI")
            button = self.data.new_parts("parameter_control", ui_id, parts_name="button")
            return button

        def make(k, e, send):
            # ui_id = self.data.all_data.elements.make_id("parameter_control_UI")

            # print("make", k, e)

            self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter_control", parts_name="parameter_control")
            self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=e.effect_name)

            send.element_key = copy.deepcopy(k)

            # option_data = {"element_key": k, "effect_point_internal_id_time": effect_point_internal_id_time, "now_f": now_f, "text_a_return": text_a_return, "text_a_return": text_b_return}
            self.data.ui_management.ui_list[self.now].button_parameter_control.set_option_data(copy.deepcopy(send), overwrite=True)
            self.data.ui_management.ui_list[self.now].button_parameter_control.callback_operation.set_event("button", element_lord_ignition)

            self.now += 1

        def media_lord(send):

            self.data.all_data.callback_operation.event("element_ui_all_del")

            elements_effect = send.effect_group
            self.now = 0

            elements_len = int(len(elements_effect.values()))
            self.data.all_data.threading_lock.acquire()

            self.data.ui_management.set_old_elements_len()

            print("あ", elements_effect)

            for k, e in zip(elements_effect.keys(), elements_effect.values()):
                make(k, e, send)

            # with self.data.all_data.ThreadPoolExecutor() as executor:
            #    [executor.submit(make(k, e, send)) for k, e in zip(elements_effect.keys(), elements_effect.values())]

            self.data.ui_management.del_ignition(self.now)
            self.data.window.update()
            self.data.all_data.threading_lock.release()

        self.data.all_data.callback_operation.set_event("media_lord", media_lord)
        self.data.all_data.callback_operation.set_event("new_button_for_parameter_control", new_button_for_parameter_control)

        self.data.window_size_set(x=220, y=360, lock_x=False)
        self.data.window.update()
        # self.data.all_data.callback_operation.set_event("element_del", element_del)

        # data.element_lord = element_lord


class CentralRole:
    pass
