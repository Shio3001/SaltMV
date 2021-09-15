# coding:utf-8
import sys
import os
import copy
import datetime
import inspect
import time


class InitialValue:
    def __init__(self, window_control):
        self.window_control = window_control
        self.operation = self.window_control.operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].TimeSearch.time_search
        self.now_f = 0
        self.now_media_id = ""
        self.send = None
        self.redo_undo_stack = []

    def main(self):
        self.window_control.window_title_set("パラメーターコントロール")
        self.window_control.callback_operation = self.window_control.operation["plugin"]["other"]["callback"].CallBack()
        self.window_control.new_canvas("parameter_control")
        self.window_control.edit_canvas_size("parameter_control", x=220, y=1000)
        self.window_control.edit_canvas_position("parameter_control", x=0, y=0)
        self.window_control.ui_management = self.window_control.operation["plugin"]["other"]["timeline_UI_management"].UIManagement(self.window_control)

        def color_edit(push_effect=None, push_color="#44ff44"):
            con_len = len(self.window_control.ui_management.ui_list)

            if not push_effect is None and push_effect < 0:
                push_effect = 0

            if not push_effect is None and push_effect > con_len - 1:
                push_effect = con_len - 1

            for now_exchange, now_UI in enumerate(self.window_control.ui_management.ui_list):
                if now_exchange == push_effect and not push_effect is None:
                    now_UI.button_parameter_control.edit_diagram_color("background", copy.deepcopy(push_color))
                    #print(now_exchange, push_effect, push_color)

                else:
                    now_UI.button_parameter_control.edit_diagram_color("background", "#44ff44")
                    #print(now_exchange, push_effect, "G")

                now_UI.button_parameter_control.diagram_draw("background")

        def element_lord_ignition(send):
            print("element_lord_ignition")
            # #print(elements_effect, option_data) #now_send.push_effect
            key = send.element_key

            if not key in send.effect_group.keys():
                return

            color_edit(send.push_effect, push_color="#ff0000")

            send.effect_element = self.window_control.edit_control_auxiliary.effect(send.media_id, key)
            self.window_control.edit_control_auxiliary.callback_operation.event("element_lord", info=(send))

        def new_button_for_parameter_control():
            ui_id = self.window_control.edit_control_auxiliary.elements.make_id("parameter_UI")
            button = self.window_control.new_parts("parameter_control", ui_id, parts_name="button")

            #print(button, "ボタンをインスタンス 化しました")
            return button

        shape_updown_destination = self.window_control.new_parts("parameter_control", "shape_updown_destination", parts_name="shape")  # 左側のやつ
        shape_updown_destination.edit_territory_size(x=220, y=5)
        shape_updown_destination.edit_territory_position(x=0, y=0)
        shape_updown_destination.edit_diagram_color("0", "#0000ff")
        shape_updown_destination.diagram_shape_view_status("0", 2)
        shape_updown_destination.territory_draw()

        def shape_updown_destination_view_True():
            shape_updown_destination.diagram_shape_view_status("0", 1)
            shape_updown_destination.territory_draw()

            self.window_control.window.update()
            # self.window_control.window.update()

        def shape_updown_destination_view_False():
            shape_updown_destination.diagram_shape_view_status("0", 2)
            shape_updown_destination.territory_draw()

            self.window_control.window.update()

            # self.window_control.window.update()

            # shape_updown_destination.territory_draw()

        def effect_del(A):
            self.send.stack_add_timelime_effect(add_type="effect_del", media_id=self.now_media_id)

            con_len = len(self.window_control.ui_management.ui_list)

            click_effect_point = A

            print("削除対象番号", click_effect_point)

            old_key = list(self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            #old_values = list(self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            old_key_data = old_key[click_effect_point]
            #old_val_data = old_values[click_effect_point]

            #del self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group[old_key_data]
            self.window_control.edit_control_auxiliary.del_effect_elements(self.now_media_id, old_key_data)

            self.window_control.ui_management.set_old_elements_len()

            new_effect_group = self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group
            #zip_data = dict(zip(new_key, new_val))

            now_exchange = 0
            for k, e in zip(new_effect_group.keys(), new_effect_group.values()):
                now_send = copy.deepcopy(self.send)
                now_send.element_key = copy.deepcopy(k)
                now_send.push_effect = copy.deepcopy(now_exchange)
                self.window_control.ui_management.ui_list[now_exchange].parameter_ui_set(column=now_exchange, text=e.effect_name)
                self.window_control.ui_management.ui_list[now_exchange].button_parameter_control.get_set_option_data(copy.deepcopy(now_send), overwrite=True)
                self.window_control.ui_management.ui_list[now_exchange].button_parameter_control.diagram_draw("background")
                self.window_control.ui_management.ui_list[now_exchange].now_exchange = now_exchange
                # self.window_control.ui_management.ui_list[now_exchange].click_end(None)

                #print(now_exchange, e.effect_name)

                now_exchange += 1

            self.window_control.ui_management.del_ignition(con_len - 1)

            self.window_control.edit_control_auxiliary.callback_operation.event("element_ui_all_del")

        def effect_updown(A, B):

            #print("呼び出し先[callback]", inspect.stack()[1].filename, inspect.stack()[1].function)

            # print("呼ばれました")

            #A, B, box_pos, gap, sta_point = send

            con_len = len(self.window_control.ui_management.ui_list)

            click_effect_point = [A, B]

            old_key = list(self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            old_values = list(self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            old_key_data = old_key[click_effect_point[0]]
            old_val_data = old_values[click_effect_point[0]]

            del self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group[old_key_data]

            new_key = list(self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            new_val = list(self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            if con_len == len(new_key):
                new_key.append(old_key_data)
                new_val.append(old_val_data)
                # print("パターンA")
            else:
                new_key.insert(click_effect_point[1], old_key_data)
                new_val.insert(click_effect_point[1], old_val_data)
                # print("パターンB")

            zip_data = dict(zip(new_key, new_val))

            #print(A, B, click_effect_point, "zipdata", zip_data)

            self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group = copy.deepcopy(zip_data)
            self.send.effect_element = copy.deepcopy(zip_data)

            # self.window_control.ui_management.set_old_elements_len()
            now_exchange = 0
            for k, e in zip(zip_data.keys(), zip_data.values()):

                now_send = copy.deepcopy(self.send)
                now_send.element_key = copy.deepcopy(k)
                now_send.push_effect = copy.deepcopy(now_exchange)
                self.window_control.ui_management.ui_list[now_exchange].parameter_ui_set(column=now_exchange, text=e.effect_name)
                self.window_control.ui_management.ui_list[now_exchange].button_parameter_control.get_set_option_data(copy.deepcopy(now_send), overwrite=True)
                self.window_control.ui_management.ui_list[now_exchange].button_parameter_control.diagram_draw("background")
                self.window_control.ui_management.ui_list[now_exchange].click_stop = False
                self.window_control.ui_management.ui_list[now_exchange].now_exchange = now_exchange

                #print(now_exchange, e.effect_name)

                now_exchange += 1

            color_edit(click_effect_point[1], push_color="#ff0000")

        def get_len_ui_list():
            return int(len(self.window_control.ui_management.ui_list))

        def make(i, k, e):
            self.window_control.ui_management.new_parameter_ui(i, canvas_name="parameter_control", parts_name="parameter_control")
            now_send = copy.deepcopy(self.send)
            now_send.element_key = copy.deepcopy(k)
            now_send.push_effect = copy.deepcopy(i)

            print("effect_controller make i k e", k, e.effect_name)
            self.window_control.ui_management.ui_list[i].parameter_ui_set(column=i, text=e.effect_name)
            self.window_control.ui_management.ui_list[i].button_parameter_control.get_set_option_data(copy.deepcopy(now_send), overwrite=True)
            self.window_control.ui_management.ui_list[i].button_parameter_control.callback_operation.all_del_event()
            self.window_control.ui_management.ui_list[i].button_parameter_control.callback_operation.set_event("button", element_lord_ignition)
            self.window_control.ui_management.ui_list[i].effect_updown = effect_updown
            self.window_control.ui_management.ui_list[i].effect_del = effect_del
            self.window_control.ui_management.ui_list[i].color_edit = color_edit
            self.window_control.ui_management.ui_list[i].shape_updown_destination_view_True = shape_updown_destination_view_True
            self.window_control.ui_management.ui_list[i].shape_updown_destination_view_False = shape_updown_destination_view_False
            self.window_control.ui_management.ui_list[i].get_len_ui_list = get_len_ui_list
            self.window_control.ui_management.ui_list[i].now_exchange = i

            # ここが悪さしてる可能性あり
            #self.now += 1
        def media_lord(send=None, del_all=None):

            if not send is None:
                self.send = send

            if del_all:
                self.window_control.ui_management.set_old_elements_len()
                self.window_control.ui_management.del_ignition(0)

                self.send = None

            if self.send is None:
                return

            self.send.effect_group = self.window_control.edit_control_auxiliary.media_object(self.send.media_id).effect_group
            self.send.effect_point_internal_id_time = self.window_control.edit_control_auxiliary.media_object(self.send.media_id).effect_point_internal_id_time

            self.window_control.edit_control_auxiliary.callback_operation.event("element_ui_all_del")

            elements_effect = self.send.effect_group
            elements_len = int(len(elements_effect.values()))
            self.now_media_id = copy.deepcopy(self.send.media_id)

            self.window_control.ui_management.set_old_elements_len()

            key_list = list(elements_effect.keys())
            val_list = list(elements_effect.values())
            list_len = len(elements_effect)

            for i in range(list_len):
                make(i, key_list[i], val_list[i])

            self.window_control.ui_management.del_ignition(list_len)
            self.window_control.window.update()
            # self.window_control.edit_control_auxiliary.threading_lock.release()

        def automatic_opening(number):

            if number > len(self.send.effect_group) - 1:
                print("automatic_opening返却")
                return

            print("automatic_opening通過")

            op = self.window_control.ui_management.ui_list[number].button_parameter_control.get_set_option_data()
            element_lord_ignition(op)

            # self.window_control.ui_management.ui_list[number].button_parameter_control.callback_operation.event("button_click")

        self.window_control.edit_control_auxiliary.callback_operation.set_event("media_lord", media_lord)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("automatic_opening", automatic_opening)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("new_button_for_parameter_control", new_button_for_parameter_control)

        self.window_control.window_size_set(x=220, y=360, lock_x=False)
        self.window_control.window.update()

        # data.element_lord = element_lord


class CentralRole:
    pass
