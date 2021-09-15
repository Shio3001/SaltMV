# coding:utf-8
import sys
import os
import copy
import datetime


class TextReceivePoint:
    def __init__(self, data, media_id, effect_id, effect_uuid_key, mov_key, stack_add_timelime_effect, int_type=None):
        self.window_control = data
        self.media_id = media_id
        self.effect_id = effect_id
        self.effect_uuid_key = effect_uuid_key
        self.mov_key = mov_key
        self.int_type = int_type
        self.stack_add_timelime_effect = stack_add_timelime_effect

        self.window_control.edit_control_auxiliary.undo_stack_list = []

    def text_func(self, text):
        old_text_data = self.window_control.edit_control_auxiliary.get_key_frame_val(self.media_id, self.effect_id, self.effect_uuid_key, self.mov_key)

        if not text:
            return

        try:
            if self.int_type:
                text = int(text)
        except:
            return

        old_s = str(old_text_data)
        now_s = str(text)

        if old_s != now_s:
            self.stack_add_timelime_effect(media_id=self.media_id)

        self.window_control.edit_control_auxiliary.edit_key_frame_val(self.media_id, self.effect_id, self.effect_uuid_key, self.mov_key, text)


class TextReceiveVariousFixed:
    def __init__(self, data, media_id, effect_id, various_fixed_key, stack_add_timelime_effect):
        self.window_control = data
        self.media_id = media_id
        self.effect_id = effect_id
        self.various_fixed_key = various_fixed_key
        self.stack_add_timelime_effect = stack_add_timelime_effect
        # self.int_type = int_type

    def text_func(self, text):
        old_s = str(self.window_control.edit_control_auxiliary.edit_various_fixed(self.media_id, self.effect_id, self.various_fixed_key))
        now_s = str(text)

        if old_s != now_s:
            self.stack_add_timelime_effect(media_id=self.media_id)

        self.window_control.edit_control_auxiliary.edit_various_fixed(self.media_id, self.effect_id, self.various_fixed_key, text)


class InitialValue:
    def __init__(self, data):
        self.window_control = data
        self.operation = self.window_control.operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].TimeSearch.time_search
        self.now = 0
        self.push_f = 0
        # self.window_control.edit_control_auxiliary.undo_stack_list = []
        self.undo_stack_now = 0

        self.send = None

        # self.redo_stack_list = []
        # self.redo_stack_now = 0
        # self.undo_stack_now = len(self.window_control.edit_control_auxiliary.undo_stack_list) - 1

    def stack_add_location_designation(self, number, media_id, effect_id, old_data):
        stack_data = {"media_id": media_id, "effect_id": effect_id, "old_data": old_data}
        self.window_control.edit_control_auxiliary.undo_stack_list[number] = stack_data

    def main(self):
        self.window_control.window_title_set("タイムライン設定")
        self.window_control.callback_operation = self.window_control.operation["plugin"]["other"]["callback"].CallBack()
        self.window_control.new_canvas("parameter")
        self.window_control.edit_canvas_size("parameter", x=1000, y=1000)
        self.window_control.edit_canvas_position("parameter", x=0, y=0)

        self.window_control.ui_management = self.window_control.operation["plugin"]["other"]["timeline_UI_management"].UIManagement(self.window_control)

        def undo_stack(undo):
            self.window_control.edit_control_auxiliary.media_object_had_layer(undo.media_id, undo.target_media_data)
            self.send.effect_element.effect_point_internal_id_point = self.window_control.edit_control_auxiliary.get_key_frame_val_list(undo.media_id, undo.effect_id)

            self.now = 0
            self.window_control.ui_management.set_old_elements_len()
            make(stack=False)
            self.window_control.ui_management.del_ignition(self.now)

            # print("undo")

        def stack_add(media_id):
            self.window_control.operation["undo"].add_stack(media_id=media_id, effect_id=self.send.effect_element.effect_id, classification="parameter", add_type="mov", func=undo_stack)

        def make(stack=True):
            media_id, element, effect_point_internal_id_time = self.send.media_id, self.send.effect_element, self.send.effect_point_internal_id_time

            # element, effect_point_internal_id_time, media_id = self.send.effect_element, self.send.effect_point_internal_id_time, self.send.media_id

            # for i, e in enumerate(elements_effect.values()):
            before_point, next_point, left_key, right_key = self.time_search(self.push_f, element, effect_point_internal_id_time, key_get=True)
            #print("before_point, next_point", before_point, next_point)
            if next_point is None:
                for pk_b, pv_b in zip(before_point.keys(), before_point.values()):
                    if pk_b in self.window_control.edit_control_auxiliary.effect_point_default_keys:
                        continue
                    # #print("pk_b, pv_b", pk_b, pv_b)

                    left = TextReceivePoint(self.window_control, media_id, element.effect_id, left_key, pk_b, stack_add, int_type=True)

                    self.window_control.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    self.window_control.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=pk_b, text_a=pv_b, text_b=None, text_a_return=left.text_func)
                    self.now += 1

            else:
                for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                    if pk_b in self.window_control.edit_control_auxiliary.effect_point_default_keys:
                        continue

                    left = TextReceivePoint(self.window_control, media_id, element.effect_id, left_key, pk_b, stack_add, int_type=True)
                    right = TextReceivePoint(self.window_control, media_id, element.effect_id, right_key, pk_n, stack_add, int_type=True)
                    self.window_control.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    # #print("pk_b, pv_b, pk_n, pv_n", pk_b, pv_b, pk_n, pv_n)
                    self.window_control.ui_management.ui_list[self.now].parameter_ui_set(motion=True, column=self.now, text=pk_b, text_a=pv_b, text_b=pv_n, text_a_return=left.text_func, text_b_return=right.text_func)
                    self.now += 1

            for vk, vv in zip(element.various_fixed.keys(), element.various_fixed.values()):

                text = TextReceiveVariousFixed(self.window_control, media_id, element.effect_id, vk, stack_add)
                self.window_control.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                self.window_control.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=vk, text_a=vv, text_b=None, text_a_return=text.text_func, text_fixed=True)
                self.now += 1

        def element_lord(send):
            old_send_effect_id = "NoneEffectSend"

            self.send = send

            if not self.send is None:
                old_send_effect_id = copy.deepcopy(self.send.effect_element.effect_id)

            self.window_control.edit_control_auxiliary.undo_stack_list = []
            self.window_control.edit_control_auxiliary.undo_stack_list_number = 0
            # element, effect_point_internal_id_time, now_f, text_a_return, text_b_return = element_self.send
            element = self.send.effect_element
            self.window_control.window_title_set("タイムライン設定 {0}".format(element.effect_name))
            self.now = 0
            self.push_f = self.send.now_f

            self.window_control.ui_management.set_old_elements_len()
            make()

            #old_text_data = self.window_control.edit_control_auxiliary.get_key_frame_val_list(self.send.media_id, self.send.effect_element.effect_id)

            new_send_effect_id = copy.deepcopy(self.send.effect_element.effect_id)

            if new_send_effect_id != old_send_effect_id:
                stack_add(self.send.media_id)

            self.window_control.ui_management.del_ignition(self.now)
            self.window_control.window.update()

        def element_ui_all_del():
            self.now = 0
            self.window_control.ui_management.set_old_elements_len()
            self.window_control.ui_management.del_ignition(self.now)
            self.window_control.window_title_set("タイムライン設定")

        self.window_control.edit_control_auxiliary.callback_operation.set_event("element_ui_all_del", element_ui_all_del)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("element_lord", element_lord)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("element_del", self.window_control.ui_management.element_del)

        # data.element_lord = element_lord


class CentralRole:
    pass
