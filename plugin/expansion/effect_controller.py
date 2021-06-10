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

        self.now_media_id = ""

        self.send = None

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

        shape_updown_destination = self.data.new_parts("parameter_control", "shape_updown_destination", parts_name="shape")  # 左側のやつ
        shape_updown_destination.edit_territory_size(x=220, y=5)
        shape_updown_destination.edit_territory_position(x=0, y=0)
        shape_updown_destination.edit_diagram_color("0", "#0000ff")
        shape_updown_destination.territory_draw()

        def effect_updown_destination(send):
            A, B = send

            con_len = len(self.data.ui_management.ui_list)

            click_effect_point_destination = B // 25

            if click_effect_point_destination < 0:
                click_effect_point_destination = 0

            if click_effect_point_destination > con_len:
                click_effect_point_destination = copy.deepcopy(con_len)

            shape_updown_destination.edit_territory_position(y=click_effect_point_destination * 25 - 5)
            shape_updown_destination.territory_draw()

        def effect_updown(send):
            A, B = send

            con_len = len(self.data.ui_management.ui_list)

            click_effect_point = [0, 0]

            click_effect_point[0] = A // 25
            click_effect_point[1] = B // 25

            if click_effect_point[0] < 0:
                click_effect_point[0] = 0

            if click_effect_point[0] > con_len - 1:
                click_effect_point[0] = con_len - 1

            if click_effect_point[1] < 0:
                click_effect_point[1] = 0

            if click_effect_point[1] > con_len - 1:
                click_effect_point[1] = con_len - 1

            print(click_effect_point[0], click_effect_point[1])

            old_key = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            old_values = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            old_key_data = old_key[click_effect_point[0]]
            old_val_data = old_values[click_effect_point[0]]

            print(old_key_data, old_val_data)

            del self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group[old_key_data]

            new_key = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            new_val = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            new_key.insert(click_effect_point[1], old_key_data)
            new_val.insert(click_effect_point[1], old_val_data)

            zip_data = dict(zip(new_key, new_val))

            self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group = zip_data

            media_lord()

        def make(k, e):
            self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter_control", parts_name="parameter_control")
            self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=e.effect_name)

            self.send.element_key = copy.deepcopy(k)

            self.data.ui_management.ui_list[self.now].button_parameter_control.callback_operation.all_del_event()
            self.data.ui_management.ui_list[self.now].button_parameter_control.set_option_data(copy.deepcopy(self.send), overwrite=True)
            self.data.ui_management.ui_list[self.now].button_parameter_control.callback_operation.set_event("button", element_lord_ignition)
            self.data.ui_management.ui_list[self.now].callback_operation.set_event("effect_updown", effect_updown)
            self.data.ui_management.ui_list[self.now].callback_operation.set_event("effect_updown_destination", effect_updown_destination)

            # ここが悪さしてる可能性あり
            self.now += 1

        def media_lord(send=None):
            if not send is None:
                self.send = send

            self.data.all_data.callback_operation.event("element_ui_all_del")

            elements_effect = self.send.effect_group
            self.now = 0

            elements_len = int(len(elements_effect.values()))
            self.data.all_data.threading_lock.acquire()

            self.data.ui_management.set_old_elements_len()

            print("あ", elements_effect)

            self.now_media_id = copy.deepcopy(self.send.media_id)

            for k, e in zip(elements_effect.keys(), elements_effect.values()):
                make(k, e)

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
