# coding:utf-8
import sys
import os
import copy
import datetime
import inspect
import time


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].TimeSearch.time_search
        self.now_f = 0
        self.now_media_id = ""
        self.send = None
        self.redo_undo_stack = []

    def main(self):
        self.data.window_title_set("パラメーターコントロール")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter_control")
        self.data.edit_canvas_size("parameter_control", x=220, y=1000)
        self.data.edit_canvas_position("parameter_control", x=0, y=0)

        self.data.ui_management = self.data.operation["plugin"]["other"]["timeline_UI_management"].UIManagement(self.data)

        # def make

        def color_edit(push_effect=None, push_color="#44ff44"):
            con_len = len(self.data.ui_management.ui_list)

            if not push_effect is None and push_effect < 0:
                return

            if not push_effect is None and push_effect > con_len - 1:
                return

            for now_exchange, now_UI in enumerate(self.data.ui_management.ui_list):
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

            send.effect_element = self.data.all_data.effect(send.media_id, key)
            self.data.all_data.callback_operation.event("element_lord", info=(send))

        def new_button_for_parameter_control():
            ui_id = self.data.all_data.elements.make_id("parameter_UI")
            button = self.data.new_parts("parameter_control", ui_id, parts_name="button")

            #print(button, "ボタンをインスタンス 化しました")
            return button

        shape_updown_destination = self.data.new_parts("parameter_control", "shape_updown_destination", parts_name="shape")  # 左側のやつ
        shape_updown_destination.edit_territory_size(x=220, y=5)
        shape_updown_destination.edit_territory_position(x=0, y=0)
        shape_updown_destination.edit_diagram_color("0", "#0000ff")
        shape_updown_destination.diagram_shape_view_status("0", 2)
        shape_updown_destination.territory_draw()

        def shape_updown_destination_view_True():
            shape_updown_destination.diagram_shape_view_status("0", 1)
            shape_updown_destination.territory_draw()

            self.data.window.update()
            # self.data.window.update()

        def shape_updown_destination_view_False():
            shape_updown_destination.diagram_shape_view_status("0", 2)
            shape_updown_destination.territory_draw()

            self.data.window.update()

            # self.data.window.update()

        def effect_updown_measurement(pos, box_pos, sta_point, con_len):

            layer_number = (pos - sta_point) // box_pos
            if layer_number < 0:
                layer_number = 0
            if layer_number > con_len:
                layer_number = copy.deepcopy(con_len)

            return layer_number

        def effect_updown_destination(A, B, box_pos, gap, sta_point):
            con_len = len(self.data.ui_management.ui_list)

            click_effect_point_destination = [0, 0]
            click_effect_point_destination[0] = effect_updown_measurement(A, box_pos, sta_point, con_len)
            click_effect_point_destination[1] = effect_updown_measurement(B, box_pos, sta_point, con_len)

            print("layer_number 判定 A / B", click_effect_point_destination)

            shape_updown_destination.edit_territory_position(y=click_effect_point_destination[1] * box_pos - gap + sta_point)

            if click_effect_point_destination[0] == click_effect_point_destination[1]:
                shape_updown_destination_view_False()
            else:
                shape_updown_destination_view_True()

            # shape_updown_destination.territory_draw()

        def effect_del(A, box_pos, gap, sta_point):
            self.send.stack_add_timelime_effect(add_type="effect_del", media_id=self.now_media_id)

            con_len = len(self.data.ui_management.ui_list)

            click_effect_point = effect_updown_measurement(A, box_pos, sta_point, con_len-1)

            old_key = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            #old_values = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            old_key_data = old_key[click_effect_point]
            #old_val_data = old_values[click_effect_point]

            self.data.ui_management.set_old_elements_len()
            #del self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group[old_key_data]
            self.data.all_data.del_effect_elements(self.now_media_id, old_key_data)

            new_key = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            new_val = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            zip_data = dict(zip(new_key, new_val))

            now_exchange = 0
            for k, e in zip(zip_data.keys(), zip_data.values()):
                now_send = copy.deepcopy(self.send)
                now_send.element_key = copy.deepcopy(k)
                now_send.push_effect = copy.deepcopy(now_exchange)
                self.data.ui_management.ui_list[now_exchange].parameter_ui_set(column=now_exchange, text=e.effect_name)
                self.data.ui_management.ui_list[now_exchange].button_parameter_control.get_set_option_data(copy.deepcopy(now_send), overwrite=True)
                self.data.ui_management.ui_list[now_exchange].button_parameter_control.diagram_draw("background")
                self.data.ui_management.ui_list[now_exchange].click_end(None)

                #print(now_exchange, e.effect_name)

                now_exchange += 1

            self.data.ui_management.del_ignition(con_len - 1)

            self.data.all_data.callback_operation.event("element_ui_all_del")

        def effect_updown(A, B, box_pos, gap, sta_point):

            #print("呼び出し先[callback]", inspect.stack()[1].filename, inspect.stack()[1].function)

            # print("呼ばれました")

            #A, B, box_pos, gap, sta_point = send

            con_len = len(self.data.ui_management.ui_list)

            click_effect_point = [0, 0]

            click_effect_point[0] = effect_updown_measurement(A, box_pos, sta_point, con_len-1)
            click_effect_point[1] = effect_updown_measurement(B, box_pos, sta_point, con_len)

            old_key = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            old_values = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            old_key_data = old_key[click_effect_point[0]]
            old_val_data = old_values[click_effect_point[0]]

            del self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group[old_key_data]

            new_key = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.keys())
            new_val = list(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group.values())

            if click_effect_point[1] > click_effect_point[0]:
                click_effect_point[1] -= 1

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

            self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[self.now_media_id][0].effect_group = copy.deepcopy(zip_data)
            self.send.effect_element = copy.deepcopy(zip_data)

            # self.data.ui_management.set_old_elements_len()
            now_exchange = 0
            for k, e in zip(zip_data.keys(), zip_data.values()):

                now_send = copy.deepcopy(self.send)
                now_send.element_key = copy.deepcopy(k)
                now_send.push_effect = copy.deepcopy(now_exchange)
                self.data.ui_management.ui_list[now_exchange].parameter_ui_set(column=now_exchange, text=e.effect_name)
                self.data.ui_management.ui_list[now_exchange].button_parameter_control.get_set_option_data(copy.deepcopy(now_send), overwrite=True)
                self.data.ui_management.ui_list[now_exchange].button_parameter_control.diagram_draw("background")
                self.data.ui_management.ui_list[now_exchange].click_stop = False

                #print(now_exchange, e.effect_name)

                now_exchange += 1

            color_edit(click_effect_point[1], push_color="#ff0000")

        def make(i, k, e):
            self.data.ui_management.new_parameter_ui(i, canvas_name="parameter_control", parts_name="parameter_control")
            now_send = copy.deepcopy(self.send)
            now_send.element_key = copy.deepcopy(k)
            now_send.push_effect = copy.deepcopy(i)

            print("effect_controller make i k e", k, e.effect_name)
            self.data.ui_management.ui_list[i].parameter_ui_set(column=i, text=e.effect_name)
            self.data.ui_management.ui_list[i].button_parameter_control.get_set_option_data(copy.deepcopy(now_send), overwrite=True)
            self.data.ui_management.ui_list[i].button_parameter_control.callback_operation.all_del_event()
            self.data.ui_management.ui_list[i].button_parameter_control.callback_operation.set_event("button", element_lord_ignition)
            self.data.ui_management.ui_list[i].effect_updown = effect_updown
            self.data.ui_management.ui_list[i].effect_updown_destination = effect_updown_destination
            self.data.ui_management.ui_list[i].effect_del = effect_del
            self.data.ui_management.ui_list[i].color_edit = color_edit
            self.data.ui_management.ui_list[i].shape_updown_destination_view_True = shape_updown_destination_view_True
            self.data.ui_management.ui_list[i].shape_updown_destination_view_False = shape_updown_destination_view_False

            # self.data.ui_management.ui_list[self.now].callback_operation.all_del_event()
            #self.data.ui_management.ui_list[self.now].button_parameter_control.callback_operation.set_event("effect_updown", effect_updown)
            #self.data.ui_management.ui_list[self.now].button_parameter_control.callback_operation.set_event("effect_updown_destination", effect_updown_destination)

            # ここが悪さしてる可能性あり
            #self.now += 1
        def media_lord(send=None, del_all=None):

            if not send is None:
                self.send = send

            if del_all:
                self.data.ui_management.set_old_elements_len()
                self.data.ui_management.del_ignition(0)

                self.send = None

            if self.send is None:
                return

            self.send.effect_group = self.data.all_data.media_object(self.send.media_id).effect_group
            self.send.effect_point_internal_id_time = self.data.all_data.media_object(self.send.media_id).effect_point_internal_id_time

            self.data.all_data.callback_operation.event("element_ui_all_del")

            elements_effect = self.send.effect_group
            elements_len = int(len(elements_effect.values()))
            self.now_media_id = copy.deepcopy(self.send.media_id)

            self.data.ui_management.set_old_elements_len()

            key_list = list(elements_effect.keys())
            val_list = list(elements_effect.values())
            list_len = len(elements_effect)

            for i in range(list_len):
                make(i, key_list[i], val_list[i])

            self.data.ui_management.del_ignition(list_len)
            self.data.window.update()
            # self.data.all_data.threading_lock.release()

        def automatic_opening(number):

            if number > len(self.send.effect_group):
                print("automatic_opening返却")
                return

            print("automatic_opening通過")

            op = self.data.ui_management.ui_list[number].button_parameter_control.get_set_option_data()
            element_lord_ignition(op)

            # self.data.ui_management.ui_list[number].button_parameter_control.callback_operation.event("button_click")

        self.data.all_data.callback_operation.set_event("media_lord", media_lord)
        self.data.all_data.callback_operation.set_event("automatic_opening", automatic_opening)
        self.data.all_data.callback_operation.set_event("new_button_for_parameter_control", new_button_for_parameter_control)

        self.data.window_size_set(x=220, y=360, lock_x=False)
        self.data.window.update()
        # self.data.all_data.callback_operation.set_event("element_del", element_del)

        # data.element_lord = element_lord


class CentralRole:
    pass
