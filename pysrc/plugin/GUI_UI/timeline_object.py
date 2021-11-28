import sys
import copy
import datetime
import threading
import uuid
import time
import asyncio


class TimelineSendData:
    def __init__(self):
        self.timeline_nowtime_approval_False = None
        self.timeline_nowtime_approval_True = None
        self.stack_add_timelime_media = None
        self.stack_add_timelime_keyframe = None
        self.stack_add_timelime_effect = None

    def set_timeline_nowtime_approval_False(self, send):
        self.timeline_nowtime_approval_False = send  # 定義

    def set_timeline_nowtime_approval_True(self, send):
        self.timeline_nowtime_approval_True = send  # 定義

    def set_stack_add_timelime_media(self, send):
        self.stack_add_timelime_media = send

    def set_stack_add_timelime_keyframe(self, send):
        self.stack_add_timelime_keyframe = send

    def set_stack_add_timelime_effect(self, send):
        self.stack_add_timelime_effect = send


class KeyFrame:
    def __init__(self, UI_auxiliary, pxf, timeline_send_data, media_callback_operation, center_x, center_y, uu_id):
        self.UI_auxiliary = UI_auxiliary
        self.pxf = pxf
        self.timeline_send_data = timeline_send_data

        self.media_callback_operation = media_callback_operation
        self.keyframe_callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()

        self.uu_id = self.UI_auxiliary.edit_control_auxiliary.elements.make_id("keyframe") if uu_id is None else uu_id

        self.center_x = center_x
        self.center_y = center_y
        self.click_flag = False
        self.pos = 0
        self.key_stop_once = [0, 0]
        self.popup2 = None

        self.mouse_sta = [0, 0]
        self.mouse_touch_sta = [0, 0]
        self.diagram_join_sta = [0, 0]
        self.now_mouse = [0, 0]
        self.diagram_join = [0, 0]

        def draw_run(send):
            self.draw(send)

        def media_id_run(info=None):
            self.this_del(info=None)

        self.pxf.callback_operation.set_event("obj_sub_point", draw_run)
        self.media_callback_operation.set_event("tihs_del_{0}".format(self.uu_id), media_id_run)
        # print(" * * * * * * * * * * keyframe設定", self.UI_auxiliary.option_data["media_id"])

        _, self.size = self.UI_auxiliary.get_diagram_position_size("bar")
        self.UI_auxiliary.new_diagram(self.uu_id)
        self.UI_auxiliary.set_shape_rhombus(self.uu_id, self.size[1] / 2, 100, 100)  # ひし形

        self.UI_auxiliary.edit_control_auxiliary.add_key_frame(0, self.UI_auxiliary.option_data["media_id"], self.uu_id,overwrite=False)
        self.pxf.set_sub_point(self.uu_id)
        self.pxf.set_px_ratio_sub_point(self.uu_id, self.center_x)
        self.UI_auxiliary.edit_diagram_color(self.uu_id, "#000000")
        self.UI_auxiliary.edit_diagram_position(self.uu_id, y=self.center_y + self.size[1]/2)
        self.UI_auxiliary.diagram_draw(self.uu_id)

        self.UI_auxiliary.add_diagram_event(self.uu_id, "Button-1", self.click_start)
        self.UI_auxiliary.add_diagram_event(self.uu_id, "Motion", self.click_position)
        self.UI_auxiliary.add_diagram_event(self.uu_id, "ButtonRelease-1", self.click_end)

        self.UI_auxiliary.add_diagram_event(self.uu_id, "Button-2", self.right_click)
        self.UI_auxiliary.diagram_stack(self.uu_id, False)
        self.UI_auxiliary.diagram_stack(self.uu_id, True, "bar")

    def click_start(self, event=None):
        self.click_flag = True
        self.key_stop_once = self.timeline_send_data.stack_add_timelime_keyframe(stop_once=True, add_type="mov", media_id=self.UI_auxiliary.option_data["media_id"])
        self.mouse_sta, self.mouse_touch_sta, self.diagram_join_sta = self.UI_auxiliary.get_diagram_contact(self.uu_id)

        self.view_pos_sta = self.UI_auxiliary.edit_diagram_position(self.uu_id)[0]
        self.keyframe_callback_operation.event("sub_sta", info=self.pxf.get_event_data())

        self.UI_auxiliary.edit_diagram_color(self.uu_id, "#ff0000")

    def click_position(self, event):
        if not self.click_flag:
            return
        self.now_mouse, _, self.diagram_join = self.UI_auxiliary.get_diagram_contact(self.uu_id)

        now_mov_x = copy.deepcopy(self.now_mouse[0] - self.mouse_sta[0])

        pos = self.view_pos_sta + now_mov_x
        # print("sub_pos", self.pos)

        # if self.UI_auxiliary.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
        self.pxf.set_px_ratio_sub_point(self.uu_id, pos)

        self.keyframe_callback_operation.event("sub_mov", info=self.pxf.get_event_data())

    def click_end(self, event):

        if self.click_flag:
            self.key_stop_once[1](self.key_stop_once[0])

        self.click_flag = False
        self.mouse_sta, _, self.diagram_join_sta = self.UI_auxiliary.get_diagram_contact(self.uu_id, del_mouse=True)
        _, _, self.diagram_join = self.UI_auxiliary.get_diagram_contact(self.uu_id, del_mouse=True)
        self.keyframe_callback_operation.event("sub_end", info=self.pxf.get_event_data())

        # self.UI_auxiliary.stack_add("frame", (self.key_frame_time_old_data, self.UI_auxiliary.option_data["media_id"], key_frame_id))
        self.UI_auxiliary.edit_diagram_color(self.uu_id, "#000000")

    def this_del(self, info=True):  # このinfoはundostackに追加するかどうか

        if info:
            self.timeline_send_data.stack_add_timelime_keyframe(add_type="del", media_id=self.UI_auxiliary.option_data["media_id"])

        self.UI_auxiliary.edit_control_auxiliary.del_key_frame_point(self.UI_auxiliary.option_data["media_id"], self.uu_id)

        self.UI_auxiliary.del_diagram(self.uu_id)
        self.pxf.del_sub_point(self.uu_id)
        self.media_callback_operation.del_event("tihs_del_{0}".format(self.uu_id))  # mi
        self.pxf.callback_operation.del_event("obj_sub_point", func=self.draw)
        self.keyframe_callback_operation.all_del_event()

        # これはdata指定!!!!!!slef.じゃないよ！気をつけて!!!!!!!!1

        # ###print(self.callback_operation.all_get_event())

    def right_click(self, event):

        self.popup2 = self.UI_auxiliary.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.UI_auxiliary.window, popup=True)
        popup_list = [("中間点削除", self.this_del)]
        self.popup2.set(popup_list)

        mouse, _, _, xy = self.UI_auxiliary.window_event_data["contact"]()
        self.UI_auxiliary.popup_click_position, _, _ = self.UI_auxiliary.get_diagram_contact("bar")

        for i in range(2):
            mouse[i] += xy[i]

        self.popup2.show(mouse[0], mouse[1])

        # ###print("追加終了")

    def draw(self, send):
        sub_name, pos_px = send
        now = self.UI_auxiliary.edit_diagram_position(sub_name, x=pos_px)
        self.UI_auxiliary.diagram_draw(sub_name)
        self.UI_auxiliary.edit_control_auxiliary.move_key_frame(self.pxf.sub_point_f[self.uu_id], self.UI_auxiliary.option_data["media_id"], self.uu_id)

        print("sub_point_f", self.pxf.sub_point_f[self.uu_id], pos_px)


class parts:
    def __init__(self, UI_auxiliary):
        self.UI_auxiliary = UI_auxiliary
        self.pxf = self.UI_auxiliary.plus_px_frame_data(direction=0, debug_name="obj")
        self.timeline_send_data = TimelineSendData()
        self.value = 0
        self.click_flag = False
        self.popup_click_flag = False
        self.popup_click_position = [0, 0]
        self.callback_operation = self.UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()
        self.media_object_parameter_bool = True
        self.mov_lock = False
        self.now_f_click_start_for_parameter_control = 0
        self.click_move_stack_flag = False
        self.click_start_sta_layer = ""
        self.click_start_end_layer = ""

        self.UI_auxiliary.new_diagram("bar")
        self.UI_auxiliary.edit_diagram_size("bar", x=100, y=20)
        self.UI_auxiliary.edit_diagram_position("bar", x=100, y=0)
        self.UI_auxiliary.edit_diagram_color("bar", "#00ff00")

        self.UI_auxiliary.edit_diagram_width("bar", 2, outline="#ffffff")

        self.UI_auxiliary.territory_draw()
        self.UI_auxiliary.territory_stack(False)

        self.UI_auxiliary.add_diagram_event("bar", "Button-2", self.right_click)
        self.UI_auxiliary.window_event_data["add"]("Key", self.click_effect_shortcut)
        self.UI_auxiliary.add_diagram_event("bar", "Button-1", self.click_start)
        self.UI_auxiliary.window_event_data["add"]("Motion", self.click_position)
        self.UI_auxiliary.add_diagram_event("bar", "ButtonRelease-1", self.click_end)

        def draw_run(info):
            self.draw(info)

        self.pxf.callback_operation.set_event("draw_func", draw_run)

        self.del_flag = False

    # def after_setup(self):

    def draw(self, info):
        px_pos, px_size = info

        print("draw")

        self.UI_auxiliary.edit_diagram_position("bar", x=px_pos)
        self.UI_auxiliary.edit_diagram_size("bar", x=px_size)
        self.UI_auxiliary.territory_draw()
        self.UI_auxiliary.edit_control_auxiliary.move_key_frame(self.pxf.ratio_f[0], self.UI_auxiliary.option_data["media_id"], "default_sta")
        self.UI_auxiliary.edit_control_auxiliary.move_key_frame(self.pxf.ratio_f[0] + self.pxf.ratio_f[1], self.UI_auxiliary.option_data["media_id"], "default_end")

    def edit_layer(self, layer_number):
        layer_pos = layer_number * self.UI_auxiliary.edit_diagram_size("bar")[1]
        self.UI_auxiliary.edit_diagram_position("bar", y=layer_pos)
        pos, size = self.UI_auxiliary.get_diagram_position_size("bar")

        for k in self.pxf.sub_point_f.keys():
            self.UI_auxiliary.edit_diagram_position(k, y=layer_pos + size[1]/2)
            self.UI_auxiliary.diagram_draw(k)

    def make_KeyFrame(self, uu_id=None, pos_f=None):
        bar_pos = self.UI_auxiliary.edit_diagram_position("bar")

        center_x = copy.deepcopy(self.popup_click_position[0]) if pos_f is None else self.pxf.f_to_px(pos_f)
        center_y = copy.deepcopy(bar_pos[1])
        new_key_frame = KeyFrame(self.UI_auxiliary, self.pxf, self.timeline_send_data, self.callback_operation, center_x, center_y, uu_id=uu_id)
        # new_key_frame.key_frame_ui_setup()
        new_key_frame.keyframe_callback_operation.set_event("sub_sta", self.timeline_send_data.timeline_nowtime_approval_False)
        new_key_frame.keyframe_callback_operation.set_event("sub_end", self.timeline_send_data.timeline_nowtime_approval_True)

        return new_key_frame

    def media_object_del(self, stack=True):
        self.UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("media_lord", 0)(del_all=True)

        if stack:
            # old_data = self.UI_auxiliary.edit_control_auxiliary.media_object_had_layer(self.UI_auxiliary.option_data["media_id"])
            self.timeline_send_data.stack_add_timelime_media(add_type="del", media_id=self.UI_auxiliary.option_data["media_id"])
            # self.UI_auxiliary.stack_add_timelime_media(add_type="del", media_id=self.UI_auxiliary.option_data["media_id"])

        self.callback_operation.event("end", info=self.pxf.get_event_data())
        self.callback_operation.event("del", self.UI_auxiliary.option_data["media_id"])

        self.del_flag = True

    def right_click(self, event):
        self.UI_auxiliary.edit_diagram_color("bar", "#0000ff")

        if not self.popup_click_flag:
            self.set_right_click_pop()

        self.popup_click_flag = True

        mouse, _, _, xy = self.UI_auxiliary.window_event_data["contact"]()
        self.popup_click_position, _, _ = self.UI_auxiliary.get_diagram_contact("bar")

        for i in range(2):
            mouse[i] += xy[i]

        same_value = self.pxf.get_same_value(self.pxf.px_to_f(self.popup_click_position[0]))

        if not same_value is None:
            self.popup.edit_bool_twice("中間点追加", False)

        if self.pxf.ratio_f[1] <= 1:
            self.popup.edit_bool_twice("分割", False)
            self.popup.edit_bool_twice("中間点追加", False)

        self.popup.show(mouse[0], mouse[1])
        self.popup.edit_bool_twice("中間点追加", True)
        self.popup.edit_bool_twice("分割", True)

        if self.del_flag:
            return

        self.UI_auxiliary.edit_diagram_color("bar", "#00ff00")

    def add_key_frame(self):
        self.timeline_send_data.stack_add_timelime_keyframe(add_type="add", media_id=self.UI_auxiliary.option_data["media_id"])
        # self.key_frame_time_old_data = self.UI_auxiliary.edit_control_auxiliary.get_key_frame(self.UI_auxiliary.option_data["media_id"])

        new_key_frame = self.make_KeyFrame()
        self.UI_auxiliary.edit_control_auxiliary.add_key_frame(self.pxf.sub_point_f[new_key_frame.uu_id], self.UI_auxiliary.option_data["media_id"], new_key_frame.uu_id)

        # ckey_frame_id = new_key_frame.uu_id
        # self.UI_auxiliary.stack_add("frame", (self.key_frame_time_old_data, self.UI_auxiliary.option_data["media_id"], key_frame_id))

        # self.UI_auxiliary.stack_add("frame", (self.key_frame_time_old_data,self.UI_auxiliary.option_data["media_id"]))

    def set_right_click_pop(self):

        self.popup = self.UI_auxiliary.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.UI_auxiliary.window, popup=True)

        effect_dict = self.UI_auxiliary.operation["plugin"]["effect"]

        effect_user_list = ["エフェクト"]

        for k in effect_dict.keys():
            effect_get = EffectGet(self.UI_auxiliary.edit_control_auxiliary, self.UI_auxiliary.option_data["media_id"], k, self.timeline_send_data.stack_add_timelime_effect)
            effect_user_list.append(k)
            effect_user_list.append(effect_get.add_element)

        synthetic_dict = self.UI_auxiliary.operation["plugin"]["synthetic"]

        synthetic_user_list = ["合成方式"]

        for k in synthetic_dict.keys():
            synthetic_get = SyntheticGet(self.UI_auxiliary.edit_control_auxiliary, self.UI_auxiliary.option_data["media_id"], k)
            synthetic_user_list.append(k)
            synthetic_user_list.append(synthetic_get.edit_synthetic)

        popup_list = [effect_user_list, synthetic_user_list, ("分割", self.media_object_separate), ("削除", self.media_object_del), ("中間点追加", self.add_key_frame)]
        self.popup.set(popup_list)

    def media_object_separate(self):
        frame = self.pxf.px_to_f(self.popup_click_position[0])

        # self.callback_operation.event("tihs_del_{0}".format(k))

        # click_f_pos = self.pxf.px_to_f(frame)
        self.callback_operation.event("separate", info=(self.UI_auxiliary.option_data["media_id"], frame))

    def send_parameter_control(self):
        send_data = ParameterSendData()
        send_data.now_f = self.now_f_click_start_for_parameter_control
        send_data.media_id = self.UI_auxiliary.option_data["media_id"]
        send_data.stack_add_timelime_effect = self.timeline_send_data.stack_add_timelime_effect
        self.UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("media_lord", 0)(send_data)

    def click_effect_shortcut(self, event):
        key = event.keysym
        print("click_effect_shortcut", key)

        if not self.click_flag:
            return

        shortcut_key = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        if not key in shortcut_key:
            return

        key_number = shortcut_key.index(key)
        print(key, key_number)

        send_data = ParameterSendData()
        send_data.now_f = self.now_f_click_start_for_parameter_control
        send_data.media_id = self.UI_auxiliary.option_data["media_id"]
        send_data.stack_add_timelime_effect = self.timeline_send_data.stack_add_timelime_effect
        self.UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("media_lord", 0)(send_data)
        self.UI_auxiliary.edit_control_auxiliary.callback_operation.event("automatic_opening", info=key_number)

    def click_start(self, event):

        print("click_start")

        self.click_start_sta_layer = self.UI_auxiliary.edit_control_auxiliary.get_now_layer_id(self.UI_auxiliary.option_data["media_id"])

        if self.mov_lock:
            return

        self.obj_stop_once = self.timeline_send_data.stack_add_timelime_media(stop_once=True, add_type="mov", media_id=self.UI_auxiliary.option_data["media_id"])

        self.click_move_stack_flag = False
        self.click_flag = True
        self.mouse_sta, self.mouse_touch_sta, self.diagram_join_sta = self.UI_auxiliary.get_diagram_contact("bar")
        self.view_pos_sta = self.UI_auxiliary.edit_diagram_position("bar")[0]
        self.view_size_sta = self.UI_auxiliary.edit_diagram_size("bar")[0]

        self.UI_auxiliary.edit_diagram_color("bar", "#ff0000")

        self.callback_operation.event("sta", info=self.pxf.get_event_data())

        self.now_f_click_start_for_parameter_control = self.pxf.px_to_f(self.mouse_sta[0])

        # self.UI_auxiliary.temp_pos_size = [None, None]

        # set_parameter_permit(False)
        # ###print("非同期開始")

        # send_self.UI_auxiliary.text_a_return = text_a_return
        # send_self.UI_auxiliary.text_b_return = text_b_return

        # func = self.UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("media_lord")[0]
        # thread_1 = self.UI_auxiliary.edit_control_auxiliary.threading.Thread(target=func, args=(send_data,))
        # thread_1.start()

        self.send_parameter_control()

        # self.UI_auxiliary.click_start_old_media_data = self.UI_auxiliary.edit_control_auxiliary.media_object_had_layer(self.UI_auxiliary.option_data["media_id"])

        # ###print("非同期")

    def click_position(self, event):

        if not self.click_flag or self.mov_lock:
            return

        now_mouse, _, self.diagram_join = self.UI_auxiliary.get_diagram_contact("bar")
        now_mov_x = copy.deepcopy(now_mouse[0] - self.mouse_sta[0])
        now_mov_y = copy.deepcopy(now_mouse[1] - self.mouse_sta[1])

        if now_mov_x != 0:
            self.click_move_stack_flag = True

        # print("now_mouse", now_mouse[0])

        if self.mouse_touch_sta[0][0]:  # 左側移動

            pos = self.view_pos_sta + now_mov_x
            size = self.view_size_sta - now_mov_x

            sub_extremity = self.pxf.get_extremity_px()

            # - self.pxf.f_to_px(1)

            """
            if not sub_extremity is None and sub_extremity[0] <= pos:
                # print("検知 A")
                old_pos = copy.deepcopy(pos)
                pos = sub_extremity[0] - 1
                size += old_pos - pos
            """

            if size < self.pxf.f_to_px(1):
                old_size = copy.deepcopy(size)
                size = self.pxf.f_to_px(1)
                pos += old_size - size

            self.pxf.set_px_ratio(position=pos, size=size, left_move=True)

        elif self.mouse_touch_sta[0][1]:  # 右側移動

            pos = self.view_pos_sta
            size = self.view_size_sta+now_mov_x

            sub_extremity = self.pxf.get_extremity_px()

            if size < self.pxf.f_to_px(1):
                size = self.pxf.f_to_px(1)

            self.pxf.set_px_ratio(position=pos, size=size, right_move=True)

        elif self.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
            pos = self.view_pos_sta + now_mov_x
            size = self.view_size_sta

            # print("now_mov_x", now_mov_x, self.UI_auxiliary.click_move_stack_flag)

            self.pxf.set_px_ratio(position=pos, size=size, sub_mov=True, main_mov=False)
            self.callback_operation.event("updown", info=(self.mouse_sta[1], now_mouse[1],  self.UI_auxiliary.option_data["media_id"], self.edit_layer))

        self.callback_operation.event("mov", info=self.pxf.get_event_data())

    def click_end(self, event):
        self.click_start_end_layer = self.UI_auxiliary.edit_control_auxiliary.get_now_layer_id(self.UI_auxiliary.option_data["media_id"])

        if self.click_start_sta_layer != self.click_start_end_layer:
            self.click_move_stack_flag = True

        # print(self.UI_auxiliary.sta_layer, self.UI_auxiliary.end_layer, self.UI_auxiliary.click_move_stack_flag)

        if self.click_flag and self.click_move_stack_flag:
            self.obj_stop_once[1](self.obj_stop_once[0])

        self.click_flag = False
        self.mouse_sta, _, self.diagram_join_sta = self.UI_auxiliary.get_diagram_contact("bar", del_mouse=True)
        _, _, self.diagram_join = self.UI_auxiliary.get_diagram_contact("bar", del_mouse=True)

        self.UI_auxiliary.edit_diagram_color("bar", "#00ff00")
        self.callback_operation.event("end", info=self.pxf.get_event_data())


class SyntheticGet:
    def __init__(self, edit_control_auxiliary, media_id, synthetic_key):
        self.edit_control_auxiliary = edit_control_auxiliary
        self.media_id = media_id
        self.synthetic_key = synthetic_key

    def edit_synthetic(self):
        self.edit_control_auxiliary.edit_effect_synthetic(self.media_id, self.synthetic_key)


class EffectGet:
    def __init__(self, edit_control_auxiliary, media_id, effect_key, stack_add_timelime_effect):
        self.edit_control_auxiliary = edit_control_auxiliary
        self.effect_key = effect_key
        self.media_id = media_id
        self.stack_add_timelime_effect = stack_add_timelime_effect

    def add_element(self):
        self.stack_add_timelime_effect(add_type="effect_add", media_id=self.media_id)
        self.edit_control_auxiliary.add_effect_elements(self.media_id, self.effect_key)


class ParameterSendData:
    def __init__(self):
        pass
