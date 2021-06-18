# coding:utf-8
import sys
import os
import copy
import datetime


class TextReceivePoint:
    def __init__(self, data, media_id, effect_id, effect_uuid_key, mov_key, stack_add, int_type=None):
        self.data = data
        self.media_id = media_id
        self.effect_id = effect_id
        self.effect_uuid_key = effect_uuid_key
        self.mov_key = mov_key
        self.int_type = int_type
        self.stack_add = stack_add

    def text_func(self, text):
        old_text_data = self.data.all_data.get_key_frame_val_list(self.media_id, self.effect_id)

        if not text:
            return

        try:
            if self.int_type:
                text = int(text)
        except:
            return

        old_s = str(old_text_data[self.effect_uuid_key][self.mov_key])
        now_s = str(text)

        if old_s != now_s:
            self.stack_add(self.media_id, self.effect_id, old_text_data)
        self.data.all_data.edit_key_frame_val(self.media_id, self.effect_id, self.effect_uuid_key, self.mov_key, text)


class TextReceiveVariousFixed:
    def __init__(self, data, media_id, effect_id, various_fixed_key, stack_add):
        self.data = data
        self.media_id = media_id
        self.effect_id = effect_id
        self.various_fixed_key = various_fixed_key
        self.stack_add = stack_add
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
        self.undo_stack_now = 0

        #self.undo_stack_now = len(self.redo_undo_stack) - 1

    def stack_add_location_designation(self, number, media_id, effect_id, old_data):
        stack_data = {"media_id": media_id, "effect_id": effect_id, "old_data": old_data}
        self.redo_undo_stack[number] = stack_data

    def main(self):
        self.data.window_title_set("タイムライン設定")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()
        self.data.new_canvas("parameter")
        self.data.edit_canvas_size("parameter", x=1000, y=1000)
        self.data.edit_canvas_position("parameter", x=0, y=0)

        self.data.ui_management = self.data.operation["plugin"]["other"]["timeline_UI_management"].UIManagement(self.data)

        def stack_add(media_id, effect_id, old_data):
            stack_data = {"media_id": media_id, "effect_id": effect_id, "old_data": old_data}
            # "effect_id": effect_id, "point_key": point_key, "mov_key": mov_key,
            self.redo_undo_stack.append(stack_data)
            self.undo_stack_now = len(self.redo_undo_stack) - 1

            print("stack_add", stack_data, self.undo_stack_now)

        def __undo_redo_set(stack_data):

            print(stack_data)

            media_id = stack_data["media_id"]
            effect_id = stack_data["effect_id"]
            data = stack_data["old_data"]

            self.redo_undo_stack.append(stack_data)

            self.data.all_data.override_key_frame_val_list(media_id, effect_id, data)
            self.send.effect_element.effect_point_internal_id_point = data

            self.now = 0
            self.data.ui_management.set_old_elements_len()
            make(stack=False)
            self.data.ui_management.del_ignition(self.now)

        def undo_stack(event):
            self.undo_stack_now -= 1
            self.redo_stack_now = len(self.redo_undo_stack) - 1

            if self.undo_stack_now < 0:
                self.undo_stack_now = 0

            if self.undo_stack_now > len(self.redo_undo_stack) - 1:
                self.undo_stack_now = len(self.redo_undo_stack) - 1

            stack_data = self.redo_undo_stack[self.undo_stack_now + 1]

            __undo_redo_set(stack_data)

            print("undo")

        self.data.add_window_event("Command-Key-z", undo_stack)

        def redo_stack(event):
            self.redo_stack_now -= 1

            if self.redo_stack_now < 0:
                self.redo_stack_now = 0

            if self.redo_stack_now > len(self.redo_undo_stack) - 1:
                self.redo_stack_now = len(self.redo_undo_stack) - 1

            stack_data = self.redo_undo_stack[self.redo_stack_now]

            __undo_redo_set(stack_data)
            print("redo")

        self.data.add_window_event("Command-Shift-Key-Z", redo_stack)

        def make(stack=True):
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

                    left = TextReceivePoint(self.data, media_id, element.effect_id, left_key, pk_b, stack_add, int_type=True)

                    self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=False, column=self.now, text=pk_b, text_a=pv_b, text_b=None, text_a_return=left.text_func)
                    self.now += 1

            else:
                for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                    if pk_b in self.data.all_data.effect_point_default_keys:
                        continue

                    left = TextReceivePoint(self.data, media_id, element.effect_id, left_key, pk_b, stack_add, int_type=True)
                    right = TextReceivePoint(self.data, media_id, element.effect_id, right_key, pk_n, stack_add, int_type=True)
                    self.data.ui_management.new_parameter_ui(self.now, canvas_name="parameter", parts_name="parameter")
                    #print("pk_b, pv_b, pk_n, pv_n", pk_b, pv_b, pk_n, pv_n)
                    self.data.ui_management.ui_list[self.now].parameter_ui_set(motion=True, column=self.now, text=pk_b, text_a=pv_b, text_b=pv_n, text_a_return=left.text_func, text_b_return=right.text_func)
                    self.now += 1

            for vk, vv in zip(element.various_fixed.keys(), element.various_fixed.values()):

                text = TextReceiveVariousFixed(self.data, media_id, element.effect_id, vk, stack_add)
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
