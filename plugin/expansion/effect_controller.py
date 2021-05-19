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
        #self.parameter_button_ui_list = []
        self.now = 0
        self.now_f = 0

    def main(self):
        self.data.window_title_set("パラメーターコントロール")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter_control")
        self.data.edit_canvas_size("parameter_control", x=1000, y=1000)
        self.data.edit_canvas_position("parameter_control", x=0, y=0)

        self.data.ui_management = self.data.operation["plugin"]["other"]["timeline_UI_management"].UIManagement(self.data)

        # def make

        def new_button_for_parameter_control():
            ui_id = self.data.all_data.elements.make_id("parameter_UI")
            button = self.data.new_parts("parameter_control", ui_id, parts_name="button")
            return button

        def make(i, e):
            ui_id = self.data.all_data.elements.make_id("parameter_control_UI")
            self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter_control", UI_name="parameter_control")
            self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text="a")
            self.now += 1

        def media_lord(send):
            elements_effect, now_f = send
            self.now = 0

            elements_len = int(len(elements_effect.values()))
            self.data.all_data.threading_lock.acquire()
            self.data.ui_management.set_old_elements_len()
            with self.data.all_data.ThreadPoolExecutor() as executor:
                [executor.submit(make(i, e)) for i, e in enumerate(elements_effect.values())]
            self.data.ui_management.del_ignition(self.now)
            self.data.all_data.threading_lock.release()

        self.data.all_data.callback_operation.set_event("media_lord", media_lord)
        self.data.all_data.callback_operation.set_event("new_button_for_parameter_control", new_button_for_parameter_control)
        #self.data.all_data.callback_operation.set_event("element_del", element_del)

        # data.element_lord = element_lord


class CentralRole:
    pass
