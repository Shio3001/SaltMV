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

        def effect_updown(B):

            con_len = len(self.data.ui_management.ui_list)

            end_click_effect = B // 25

            if end_click_effect < 0:
                end_click_effect = 0

            if end_click_effect > con_len - 1:
                end_click_effect = con_len - 1

            textA = self.data.ui_management.ui_list[self.sta_click_effect].button_parameter_control.get_text("text")
            textB = self.data.ui_management.ui_list[end_click_effect].button_parameter_control.get_text("text")

            self.data.ui_management.ui_list[self.sta_click_effect].button_parameter_control.edit_diagram_text("text", textB)
            self.data.ui_management.ui_list[self.sta_click_effect].button_parameter_control.territory_draw()

            self.data.ui_management.ui_list[end_click_effect].button_parameter_control.edit_diagram_text("text", textA)
            self.data.ui_management.ui_list[end_click_effect].button_parameter_control.territory_draw()

        def click_start(event):
            self.background_mouse, _, _ = self.data.ui_management.ui_list[self.now].button_parameter_control.get_diagram_contact("background")
            self.sta_click_effect = self.background_mouse[1] // 25

        def click_position(event):
            self.background_now_mouse, _, _ = self.data.ui_management.ui_list[self.now].button_parameter_control.get_diagram_contact("background")
            effect_updown(self.background_now_mouse[1])

        def click_end(event):
            self.background_mouse, _, _ = self.data.ui_management.ui_list[self.now].button_parameter_control.get_diagram_contact("background", del_mouse=True)
            self.background_now_mouse, _, _ = self.data.ui_management.ui_list[self.now].button_parameter_control.get_diagram_contact("background", del_mouse=True)

        def make(k, e, send):
            self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter_control", parts_name="parameter_control")
            self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=e.effect_name)

            send.element_key = copy.deepcopy(k)

            self.data.ui_management.ui_list[self.now].button_parameter_control.callback_operation.all_del_event()
            self.data.ui_management.ui_list[self.now].button_parameter_control.set_option_data(copy.deepcopy(send), overwrite=True)
            self.data.ui_management.ui_list[self.now].button_parameter_control.callback_operation.set_event("button", element_lord_ignition)
            self.data.ui_management.ui_list[self.now].button_parameter_control.add_diagram_event("text", "Button-1", click_start)
            self.data.ui_management.ui_list[self.now].button_parameter_control.window_event_data["add"]("Motion", click_position)
            self.data.ui_management.ui_list[self.now].button_parameter_control.add_diagram_event("text", "ButtonRelease-1", click_end)

            # ここが悪さしてる可能性あり
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
