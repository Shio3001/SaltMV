# coding:utf-8
import sys
import os
import copy
import datetime


class TextReceivePoint:
    def __init__(self, data, media_id, effect_id, effect_uuid_key, mov_key, stack_add, undo_stack, redo_stack, int_type=None):
        self.data = data
        self.media_id = media_id
        self.effect_id = effect_id
        self.effect_uuid_key = effect_uuid_key
        self.mov_key = mov_key
        self.int_type = int_type
        self.stack_add, self.undo_stack, self.redo_stack = stack_add, undo_stack, redo_stack

    def text_func(self, text):
        old_text = self.data.all_data.get_key_frame_val(self.media_id, self.effect_id, self.effect_uuid_key, self.mov_key)
        self.stack_add(self.media_id, self.effect_id, self.effect_uuid_key, self.mov_key, old_text)

        try:
            if self.int_type:
                text = int(text)

        except:
            return

        self.data.all_data.edit_key_frame_val(self.media_id, self.effect_id, self.effect_uuid_key, self.mov_key, text)


class TextReceiveVariousFixed:
    def __init__(self, data, media_id, effect_id, various_fixed_key, stack_add, undo_stack, redo_stack,):
        self.data = data
        self.media_id = media_id
        self.effect_id = effect_id
        self.various_fixed_key = various_fixed_key
        self.stack_add, self.undo_stack, self.redo_stack = stack_add, undo_stack, redo_stack
        #self.int_type = int_type

    def text_func(self, text):
        old_text = self.data.all_data.get_key_frame_val(self.media_id, self.effect_id, self.effect_uuid_key, self.val_ke)

        self.stack_add(self.media_id, self.effect_id, self.effect_uuid_key, self.mov_key, old_text)
        self.data.all_data.edit_various_fixed(self.media_id, self.effect_id, self.various_fixed_key, text)


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].TimeSearch.time_search
        self.now = 0
        self.push_f = 0
        self.redo_undo_stack = []
        self.redo_undo_stack_now = 0

    def stack_add(self, media_id, effect_id, point_key, mov_key, old_data):
        stack_data = {"media_id": media_id, "effect_id": effect_id, "point_key": point_key, "mov_key": mov_key, "old_data": old_data}
        self.redo_undo_stack.append(stack_data)
        self.redo_undo_stack_now = len(self.redo_undo_stack) - 1

    def main(self):
        self.data.window_title_set("タイムライン設定")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter")
        self.data.edit_canvas_size("parameter", x=1000, y=1000)
        self.data.edit_canvas_position("parameter", x=0, y=0)

        self.data.ui_management = self.data.operation["plugin"]["other"]["timeline_UI_management"].UIManagement(self.data)

        def undo_stack(event):
            self.redo_undo_stack_now -= 1
            self.redo_undo_stack.append(self.redo_undo_stack[self.redo_undo_stack_now])

            stack_data = self.redo_undo_stack[self.redo_undo_stack_number]
            media_id = stack_data["media_id"]
            effect_id = stack_data["effect_id"]
            effect_uuid_key = stack_data["point_key"]
            mov_key = stack_data["mov_key"]
            text = stack_data["old_data"]
            self.data.all_data.edit_key_frame_val(media_id, effect_id, effect_uuid_key, mov_key, text)

            self.data.ui_management.set_old_elements_len()
            self.send.effect_point_internal_id_time = self.data.all_data.get_key_frame(media_id, effect_id)

            make()
            self.data.ui_management.del_ignition(self.now)

        self.data.add_window_event("Control-Key-x", undo_stack)

        def redo_stack():
            self.redo_undo_stack_now += 1
            self.redo_undo_stack.append(self.redo_undo_stack[self.redo_undo_stack_now])

            self.data.ui_management.set_old_elements_len()
            make()
            self.data.ui_management.del_ignition(self.now)

        def make():
            media_id, element, effect_point_internal_id_time = self.send.media_id, self.send.effect_element, self.send.effect_point_internal_id_time
            #element, effect_point_internal_id_time, media_id = self.send.effect_element, self.send.effect_point_internal_id_time, self.send.media_id

            # for i, e in enumerate(elements_effect.values()):
            before_point, next_point, left_key, right_key = self.time_search(self.push_f, element, effect_point_internal_id_time, key_get=True)
            print("before_point, next_point", before_point, next_point)
            if next_point is None:
                for pk_b, pv_b in zip(before_point.keys(), before_point.values()):
                    if pk_b in self.data.all_data.effect_point_default_keys:
                        continue
                    #print("pk_b, pv_b", pk_b, pv_b)
                    left = TextReceivePoint(self.data, media_id, element.effect_id, left_key, pk_b, self.stack_add, undo_stack, redo_stack, int_type=True)
                    self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=pk_b, text_a=pv_b, text_b=None, text_a_return=left.text_func)
                    self.now += 1

            else:
                for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                    if pk_b in self.data.all_data.effect_point_default_keys:
                        continue

                    left = TextReceivePoint(self.data, media_id, element.effect_id, left_key, pk_b, self.stack_add, undo_stack, redo_stack, int_type=True)
                    right = TextReceivePoint(self.data, media_id, element.effect_id, right_key, pk_n, self.stack_add, undo_stack, redo_stack, int_type=True)
                    self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    #print("pk_b, pv_b, pk_n, pv_n", pk_b, pv_b, pk_n, pv_n)
                    self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=True, column=self.now, text=pk_b, text_a=pv_b, text_b=pv_n, text_a_return=left.text_func, text_b_return=right.text_func)
                    self.now += 1

            for vk, vv in zip(element.various_fixed.keys(), element.various_fixed.values()):

                text = TextReceiveVariousFixed(self.data, media_id, element.effect_id, vk, self.stack_add, self.undo_stack, self.redo_stack)
                self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=vk, text_a=vv, text_b=None, text_a_return=text.text_func, text_fixed=True)
                self.now += 1

        def element_lord(send):
            self.send = send
            self.redo_undo_stack = []
            self.redo_undo_stack_number = 0
            #element, effect_point_internal_id_time, now_f, text_a_return, text_b_return = element_self.send
            element = self.send.effect_element
            self.data.window_title_set("タイムライン設定 {0}".format(element.effect_name))
            self.now = 0
            self.push_f = self.send.now_f

            self.data.ui_management.set_old_elements_len()
            make()
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
