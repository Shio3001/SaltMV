import sys
import copy
import datetime
import threading
import uuid
import time
import asyncio


class TimelineSendData:
    def __init__(self):
        pass

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
    def __init__(self, UI_auxiliary, size, center_x, center_y, uu_id):
        # print(" * * * * * * * * * * keyframe設定", UI_auxiliary.option_data["media_id"])
        self.uu_id = UI_auxiliary.edit_control_auxiliary.elements.make_id("keyframe") if uu_id is None else uu_id

        UI_auxiliary.new_diagram(self.uu_id)

        UI_auxiliary.set_shape_rhombus(self.uu_id, size, 100, 100)  # ひし形
        self.callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()

        UI_auxiliary.edit_control_auxiliary.add_key_frame(0, UI_auxiliary.option_data["media_id"], self.uu_id)

        def draw(send):
            sub_name, pos_px = send
            now = UI_auxiliary.edit_diagram_position(sub_name, x=pos_px)
            UI_auxiliary.diagram_draw(sub_name)
            UI_auxiliary.edit_control_auxiliary.move_key_frame(UI_auxiliary.pxf.sub_point_f[self.uu_id], UI_auxiliary.option_data["media_id"], self.uu_id)

            print("sub_point_f", UI_auxiliary.pxf.sub_point_f[self.uu_id], pos_px)

        # 気をつけて!!!!!!!!
        # 気をつけて!!!!!!!!
        # 気をつけて!!!!!!!!
        UI_auxiliary.pxf.callback_operation.set_event("obj_sub_point", draw)
        # 気をつけて!!!!!!!!
        # 気をつけて!!!!!!!!
        # 気をつけて!!!!!!!!

        UI_auxiliary.pxf.set_sub_point(self.uu_id)
        UI_auxiliary.pxf.set_px_ratio_sub_point(self.uu_id, center_x)

        UI_auxiliary.edit_diagram_color(self.uu_id, "#000000")
        pos, size = UI_auxiliary.get_diagram_position_size("bar")
        UI_auxiliary.edit_diagram_position(self.uu_id, y=center_y + size[1]/2)

        UI_auxiliary.diagram_draw(self.uu_id)

        self.click_flag = False

        def click_start(event):
            self.click_flag = True
            self.key_stop_once = UI_auxiliary.stack_add_timelime_keyframe(stop_once=True, add_type="mov", media_id=UI_auxiliary.option_data["media_id"])
            self.mouse_sta, self.mouse_touch_sta, self.diagram_join_sta = UI_auxiliary.get_diagram_contact(self.uu_id)

            self.view_pos_sta = UI_auxiliary.edit_diagram_position(self.uu_id)[0]
            self.callback_operation.event("sub_sta", info=UI_auxiliary.pxf.get_event_data())

            UI_auxiliary.edit_diagram_color(self.uu_id, "#ff0000")

            # print(self.uu_id)

            # self.key_frame_time_old_data = UI_auxiliary.edit_control_auxiliary.get_key_frame(UI_auxiliary.option_data["media_id"])

        def click_position(event):
            if not self.click_flag:
                return
            self.now_mouse, _, self.diagram_join = UI_auxiliary.get_diagram_contact(self.uu_id)

            self.now_mov_x = copy.deepcopy(self.now_mouse[0] - self.mouse_sta[0])

            self.pos = self.view_pos_sta + self.now_mov_x
            # print("sub_pos", self.pos)

            # if UI_auxiliary.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
            UI_auxiliary.pxf.set_px_ratio_sub_point(self.uu_id, self.pos)

            self.callback_operation.event("sub_mov", info=UI_auxiliary.pxf.get_event_data())

        def click_end(event):

            if self.click_flag:
                self.key_stop_once[1](self.key_stop_once[0])

            self.click_flag = False
            self.mouse_sta, _, self.diagram_join_sta = UI_auxiliary.get_diagram_contact(self.uu_id, del_mouse=True)
            _, _, self.diagram_join = UI_auxiliary.get_diagram_contact(self.uu_id, del_mouse=True)
            self.callback_operation.event("sub_end", info=UI_auxiliary.pxf.get_event_data())

            key_frame_id = self.uu_id
            # UI_auxiliary.stack_add("frame", (self.key_frame_time_old_data, UI_auxiliary.option_data["media_id"], key_frame_id))
            UI_auxiliary.edit_diagram_color(self.uu_id, "#000000")

        UI_auxiliary.add_diagram_event(self.uu_id, "Button-1", click_start)
        UI_auxiliary.add_diagram_event(self.uu_id, "Motion", click_position)
        UI_auxiliary.add_diagram_event(self.uu_id, "ButtonRelease-1", click_end)

        def make_internal_key_frame():
            pass

        def this_del(info=True):  # このinfoはundostackに追加するかどうか

            # ###print("thisdel")
            if info:
                #self.key_frame_time_old_data = UI_auxiliary.edit_control_auxiliary.get_key_frame(UI_auxiliary.option_data["media_id"])
                # key_frame_id = self.uu_id
                # UI_auxiliary.stack_add("frame", (self.key_frame_time_old_data, UI_auxiliary.option_data["media_id"], key_frame_id))
                UI_auxiliary.timeline_send_data.stack_add_timelime_keyframe(add_type="del", media_id=UI_auxiliary.option_data["media_id"])

                # UI_auxiliary.stack_add("frame", (self.key_frame_time_old_data, UI_auxiliary.option_data["media_id"]))

            UI_auxiliary.edit_control_auxiliary.del_key_frame_point(UI_auxiliary.option_data["media_id"], self.uu_id)

            UI_auxiliary.del_diagram(self.uu_id)
            UI_auxiliary.pxf.del_sub_point(self.uu_id)
            UI_auxiliary.callback_operation.del_event("tihs_del_{0}".format(self.uu_id))
            UI_auxiliary.pxf.callback_operation.del_event("obj_sub_point", func=draw)

            self.callback_operation.all_del_event()

        # 気をつけて!!!!!!!!
        # 気をつけて!!!!!!!!
        # 気をつけて!!!!!!!!
        UI_auxiliary.callback_operation.set_event("tihs_del_{0}".format(self.uu_id), this_del)  # これはdata指定!!!!!!slef.じゃないよ！気をつけて!!!!!!!!1
        # 気をつけて!!!!!!!!
        # 気をつけて!!!!!!!!
        # 気をつけて!!!!!!!!

        # ###print(self.callback_operation.all_get_event())

        def right_click(event):

            self.popup2 = UI_auxiliary.operation["plugin"]["other"]["menu_popup"].MenuPopup(UI_auxiliary.window, popup=True)
            popup_list = [("中間点削除", this_del)]
            self.popup2.set(popup_list)

            mouse, _, _, xy = UI_auxiliary.window_event_data["contact"]()
            UI_auxiliary.popup_click_position, _, _ = UI_auxiliary.get_diagram_contact("bar")

            for i in range(2):
                mouse[i] += xy[i]

            self.popup2.show(mouse[0], mouse[1])

        UI_auxiliary.add_diagram_event(self.uu_id, "Button-2", right_click)

        UI_auxiliary.diagram_stack(self.uu_id, False)
        UI_auxiliary.diagram_stack(self.uu_id, True, "bar")

        # ###print("追加終了")


class parts:

    def UI_set(self, UI_auxiliary):  # data ←継承元(ファイルが違う＋プラグイン形式なのでこのような形に)

        UI_auxiliary.timeline_send_data = TimelineSendData()

        UI_auxiliary.value = 0
        UI_auxiliary.click_flag = False

        UI_auxiliary.new_diagram("bar")
        UI_auxiliary.edit_diagram_size("bar", x=100, y=20)
        UI_auxiliary.edit_diagram_position("bar", x=100, y=0)
        UI_auxiliary.edit_diagram_color("bar", "#00ff00")

        UI_auxiliary.edit_diagram_width("bar", 2, outline="#ffffff")

        UI_auxiliary.territory_draw()
        UI_auxiliary.territory_stack(False)

        # UI_auxiliary.obj_now_layer = 0

        # UI_auxiliary.timeline_object_ID = None

        UI_auxiliary.pxf = UI_auxiliary.plus_px_frame_data(direction=0, debug_name="obj")

        def edit_layer(layer_number):
            layer_pos = layer_number * UI_auxiliary.edit_diagram_size("bar")[1]
            UI_auxiliary.edit_diagram_position("bar", y=layer_pos)
            pos, size = UI_auxiliary.get_diagram_position_size("bar")

            for k in UI_auxiliary.pxf.sub_point_f.keys():
                UI_auxiliary.edit_diagram_position(k, y=layer_pos + size[1]/2)
                UI_auxiliary.diagram_draw(k)

        UI_auxiliary.edit_layer = edit_layer
        # print("layer_pos", layer_pos)

        # UI_auxiliary.pos_add_y = pos_add_y

        def draw(info):
            px_pos, px_size = info

            UI_auxiliary.edit_diagram_position("bar", x=px_pos)
            UI_auxiliary.edit_diagram_size("bar", x=px_size)
            UI_auxiliary.territory_draw()
            UI_auxiliary.edit_control_auxiliary.move_key_frame(UI_auxiliary.pxf.ratio_f[0], UI_auxiliary.option_data["media_id"], "default_sta")
            UI_auxiliary.edit_control_auxiliary.move_key_frame(UI_auxiliary.pxf.ratio_f[0] + UI_auxiliary.pxf.ratio_f[1], UI_auxiliary.option_data["media_id"], "default_end")

        UI_auxiliary.pxf.callback_operation.set_event("draw_func", draw)

        # UI_auxiliary.pxf.set_draw_func(draw)

        def media_object_del(stack=True):

            # UI_auxiliary.edit_control_auxiliary.callback_operation.event("element_ui_all_del")

            UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("media_lord")[0](del_all=True)

            if stack:
                # old_data = UI_auxiliary.edit_control_auxiliary.media_object_had_layer(UI_auxiliary.option_data["media_id"])
                UI_auxiliary.timeline_send_data.stack_add_timelime_media(add_type="del", media_id=UI_auxiliary.option_data["media_id"])
                # UI_auxiliary.stack_add_timelime_media(add_type="del", media_id=UI_auxiliary.option_data["media_id"])

            UI_auxiliary.callback_operation.event("end", info=UI_auxiliary.pxf.get_event_data())
            UI_auxiliary.callback_operation.event("del", UI_auxiliary.option_data["media_id"])

            # send_parameter_control()

        UI_auxiliary.media_object_del = media_object_del

        def media_object_separate():
            frame = UI_auxiliary.pxf.px_to_f(UI_auxiliary.popup_click_position[0])

            # UI_auxiliary.callback_operation.event("tihs_del_{0}".format(k))

            # click_f_pos = UI_auxiliary.pxf.px_to_f(frame)
            UI_auxiliary.callback_operation.event("separate", info=(UI_auxiliary.option_data["media_id"], frame))

        def make_KeyFrame(uu_id=None, pos_f=None):
            bar_pos = UI_auxiliary.edit_diagram_position("bar")

            size = UI_auxiliary.edit_diagram_size("bar")[1] / 2
            center_x = copy.deepcopy(UI_auxiliary.popup_click_position[0]) if pos_f is None else UI_auxiliary.pxf.f_to_px(pos_f)
            center_y = copy.deepcopy(bar_pos[1])
            new_key_frame = KeyFrame(UI_auxiliary, size, center_x, center_y, uu_id=uu_id)
            new_key_frame.callback_operation.set_event("sub_sta", UI_auxiliary.timeline_send_datatimeline_nowtime_approval_False)
            new_key_frame.callback_operation.set_event("sub_end", UI_auxiliary.timeline_send_data.timeline_nowtime_approval_True)

            return new_key_frame

        UI_auxiliary.make_KeyFrame = make_KeyFrame

        def add_key_frame():
            UI_auxiliary.timeline_send_data.stack_add_timelime_keyframe(add_type="add", media_id=UI_auxiliary.option_data["media_id"])
            # self.key_frame_time_old_data = UI_auxiliary.edit_control_auxiliary.get_key_frame(UI_auxiliary.option_data["media_id"])

            new_key_frame = make_KeyFrame()
            UI_auxiliary.edit_control_auxiliary.add_key_frame(UI_auxiliary.pxf.sub_point_f[new_key_frame.uu_id], UI_auxiliary.option_data["media_id"], new_key_frame.uu_id)

            # ckey_frame_id = new_key_frame.uu_id
            # UI_auxiliary.stack_add("frame", (self.key_frame_time_old_data, UI_auxiliary.option_data["media_id"], key_frame_id))

            # UI_auxiliary.stack_add("frame", (self.key_frame_time_old_data,UI_auxiliary.option_data["media_id"]))

        UI_auxiliary.popup_click_flag = False

        def set_right_click_pop():

            UI_auxiliary.popup = UI_auxiliary.operation["plugin"]["other"]["menu_popup"].MenuPopup(UI_auxiliary.window, popup=True)

            effect_dict = UI_auxiliary.operation["plugin"]["effect"]

            effect_user_list = ["エフェクト"]

            for k in effect_dict.keys():
                effect_get = EffectGet(UI_auxiliary.edit_control_auxiliary, UI_auxiliary.option_data["media_id"], k, UI_auxiliary.timeline_send_data.stack_add_timelime_effect)
                effect_user_list.append(k)
                effect_user_list.append(effect_get.add_element)

            synthetic_dict = UI_auxiliary.operation["plugin"]["synthetic"]

            synthetic_user_list = ["合成方式"]

            for k in synthetic_dict.keys():
                synthetic_get = SyntheticGet(UI_auxiliary.edit_control_auxiliary, UI_auxiliary.option_data["media_id"], k)
                synthetic_user_list.append(k)
                synthetic_user_list.append(synthetic_get.edit_synthetic)

            popup_list = [effect_user_list, synthetic_user_list, ("分割", media_object_separate), ("削除", media_object_del), ("中間点追加", add_key_frame)]
            UI_auxiliary.popup.set(popup_list)

        #UI_auxiliary.set_right_click_pop = set_right_click_pop

        UI_auxiliary.popup_click_position = [0, 0]

        def right_click(event):
            UI_auxiliary.edit_diagram_color("bar", "#0000ff")

            if not UI_auxiliary.popup_click_flag:
                set_right_click_pop()

            UI_auxiliary.popup_click_flag = True

            mouse, _, _, xy = UI_auxiliary.window_event_data["contact"]()
            UI_auxiliary.popup_click_position, _, _ = UI_auxiliary.get_diagram_contact("bar")

            for i in range(2):
                mouse[i] += xy[i]

            same_value = UI_auxiliary.pxf.get_same_value(UI_auxiliary.pxf.px_to_f(UI_auxiliary.popup_click_position[0]))

            if not same_value is None:
                UI_auxiliary.popup.edit_bool_twice("中間点追加", False)

            if UI_auxiliary.pxf.ratio_f[1] <= 1:
                UI_auxiliary.popup.edit_bool_twice("分割", False)
                UI_auxiliary.popup.edit_bool_twice("中間点追加", False)

            UI_auxiliary.popup.show(mouse[0], mouse[1])
            UI_auxiliary.popup.edit_bool_twice("中間点追加", True)
            UI_auxiliary.popup.edit_bool_twice("分割", True)

            UI_auxiliary.edit_diagram_color("bar", "#00ff00")

        UI_auxiliary.add_diagram_event("bar", "Button-2", right_click)

        # popup_list = [("ファイル", "終了", self.UI_auxiliary.window_exit), ("新規", "シーン", None, "レイヤー", new_layer), ("追加", "動画", new_obj)]
        # self.popup.set(popup_list)
        UI_auxiliary.callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()

        UI_auxiliary.media_object_parameter_bool = True

        # def set_parameter_permit(flag_bool):
        #    UI_auxiliary.media_object_parameter_bool = flag_bool
        #    ####print("非同期 :", flag_bool)

        UI_auxiliary.click_flag = False
        UI_auxiliary.mov_lock = False

        UI_auxiliary.now_f_click_start_for_parameter_control = 0

        def send_parameter_control():

            send_data = ParameterSendData()
            send_data.now_f = UI_auxiliary.now_f_click_start_for_parameter_control
            send_data.media_id = UI_auxiliary.option_data["media_id"]
            send_data.stack_add_timelime_effect = UI_auxiliary.timeline_send_data.stack_add_timelime_effect
            UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("media_lord")[0](send_data)

        UI_auxiliary.send_parameter_control = send_parameter_control
        UI_auxiliary.click_move_stack_flag = False

        UI_auxiliary.click_start_sta_layer = ""
        UI_auxiliary.click_start_end_layer = ""

        def click_effect_shortcut(event):
            key = event.keysym
            print("click_effect_shortcut", key)

            if not UI_auxiliary.click_flag:
                return

            shortcut_key = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

            if not key in shortcut_key:
                return

            key_number = shortcut_key.index(key)
            print(key, key_number)

            send_data = ParameterSendData()
            send_data.now_f = UI_auxiliary.now_f_click_start_for_parameter_control
            send_data.media_id = UI_auxiliary.option_data["media_id"]
            send_data.stack_add_timelime_effect = UI_auxiliary.timeline_send_data.stack_add_timelime_effect
            UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("media_lord")[0](send_data)
            UI_auxiliary.edit_control_auxiliary.callback_operation.event("automatic_opening", info=key_number)

        UI_auxiliary.window_event_data["add"]("Key", click_effect_shortcut)

        def click_start(event):

            print("click_start")

            UI_auxiliary.click_start_sta_layer = UI_auxiliary.edit_control_auxiliary.get_now_layer_id(UI_auxiliary.option_data["media_id"])

            if UI_auxiliary.mov_lock:
                return

            UI_auxiliary.obj_stop_once = UI_auxiliary.timeline_send_data.stack_add_timelime_media(stop_once=True, add_type="mov", media_id=UI_auxiliary.option_data["media_id"])

            UI_auxiliary.click_move_stack_flag = False
            UI_auxiliary.click_flag = True
            UI_auxiliary.mouse_sta, UI_auxiliary.mouse_touch_sta, UI_auxiliary.diagram_join_sta = UI_auxiliary.get_diagram_contact("bar")
            UI_auxiliary.view_pos_sta = UI_auxiliary.edit_diagram_position("bar")[0]
            UI_auxiliary.view_size_sta = UI_auxiliary.edit_diagram_size("bar")[0]

            UI_auxiliary.edit_diagram_color("bar", "#ff0000")

            UI_auxiliary.callback_operation.event("sta", info=UI_auxiliary.pxf.get_event_data())

            UI_auxiliary.now_f_click_start_for_parameter_control = UI_auxiliary.pxf.px_to_f(UI_auxiliary.mouse_sta[0])

            # UI_auxiliary.temp_pos_size = [None, None]

            # set_parameter_permit(False)
            # ###print("非同期開始")

            # send_UI_auxiliary.text_a_return = text_a_return
            # send_UI_auxiliary.text_b_return = text_b_return

            # func = UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("media_lord")[0]
            # thread_1 = UI_auxiliary.edit_control_auxiliary.threading.Thread(target=func, args=(send_data,))
            # thread_1.start()

            send_parameter_control()

            # UI_auxiliary.click_start_old_media_data = UI_auxiliary.edit_control_auxiliary.media_object_had_layer(UI_auxiliary.option_data["media_id"])

            # ###print("非同期")

        def click_position(event):

            if not UI_auxiliary.click_flag or UI_auxiliary.mov_lock:
                return

            now_mouse, _, UI_auxiliary.diagram_join = UI_auxiliary.get_diagram_contact("bar")
            now_mov_x = copy.deepcopy(now_mouse[0] - UI_auxiliary.mouse_sta[0])
            now_mov_y = copy.deepcopy(now_mouse[1] - UI_auxiliary.mouse_sta[1])

            if now_mov_x != 0:
                UI_auxiliary.click_move_stack_flag = True

            # print("now_mouse", now_mouse[0])

            if UI_auxiliary.mouse_touch_sta[0][0]:  # 左側移動

                pos = UI_auxiliary.view_pos_sta + now_mov_x
                size = UI_auxiliary.view_size_sta - now_mov_x

                sub_extremity = UI_auxiliary.pxf.get_extremity_px()

                # - UI_auxiliary.pxf.f_to_px(1)

                """
                if not sub_extremity is None and sub_extremity[0] <= pos:
                    # print("検知 A")
                    old_pos = copy.deepcopy(pos)
                    pos = sub_extremity[0] - 1
                    size += old_pos - pos
                """

                if size < UI_auxiliary.pxf.f_to_px(1):
                    old_size = copy.deepcopy(size)
                    size = UI_auxiliary.pxf.f_to_px(1)
                    pos += old_size - size

                UI_auxiliary.pxf.set_px_ratio(position=pos, size=size, left_move=True)

            elif UI_auxiliary.mouse_touch_sta[0][1]:  # 右側移動

                pos = UI_auxiliary.view_pos_sta
                size = UI_auxiliary.view_size_sta+now_mov_x

                sub_extremity = UI_auxiliary.pxf.get_extremity_px()

                if size < UI_auxiliary.pxf.f_to_px(1):
                    size = UI_auxiliary.pxf.f_to_px(1)

                UI_auxiliary.pxf.set_px_ratio(position=pos, size=size, right_move=True)

            elif UI_auxiliary.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                pos = UI_auxiliary.view_pos_sta + now_mov_x
                size = UI_auxiliary.view_size_sta

                # print("now_mov_x", now_mov_x, UI_auxiliary.click_move_stack_flag)

                UI_auxiliary.pxf.set_px_ratio(position=pos, size=size, sub_mov=True, main_mov=False)
                UI_auxiliary.callback_operation.event("updown", info=(UI_auxiliary.mouse_sta[1], now_mouse[1],  UI_auxiliary.option_data["media_id"], edit_layer))

            UI_auxiliary.callback_operation.event("mov", info=UI_auxiliary.pxf.get_event_data())

        def click_end(event):
            UI_auxiliary.click_start_end_layer = UI_auxiliary.edit_control_auxiliary.get_now_layer_id(UI_auxiliary.option_data["media_id"])

            if UI_auxiliary.click_start_sta_layer != UI_auxiliary.click_start_end_layer:
                UI_auxiliary.click_move_stack_flag = True

            # print(UI_auxiliary.sta_layer, UI_auxiliary.end_layer, UI_auxiliary.click_move_stack_flag)

            if UI_auxiliary.click_flag and UI_auxiliary.click_move_stack_flag:
                UI_auxiliary.obj_stop_once[1](UI_auxiliary.obj_stop_once[0])

            UI_auxiliary.click_flag = False
            UI_auxiliary.mouse_sta, _, UI_auxiliary.diagram_join_sta = UI_auxiliary.get_diagram_contact("bar", del_mouse=True)
            _, _, UI_auxiliary.diagram_join = UI_auxiliary.get_diagram_contact("bar", del_mouse=True)

            UI_auxiliary.edit_diagram_color("bar", "#00ff00")
            UI_auxiliary.callback_operation.event("end", info=UI_auxiliary.pxf.get_event_data())

            # UI_auxiliary.callback_operation.event("mov", info=UI_auxiliary.pxf.get_event_data())

        # async def sleeping():
        #     loop = asyncio.get_event_loop()
        #     sec = 1
        #     print(f'start:  {sec}秒待つよ')
        #     await loop.run_in_executor(None, time.sleep, sec)
        #     print(f'finish: {sec}秒待つよ')

        #     UI_auxiliary.callback_operation.event("end", info=UI_auxiliary.pxf.get_event_data())

        UI_auxiliary.add_diagram_event("bar", "Button-1", click_start)
        UI_auxiliary.window_event_data["add"]("Motion", click_position)
        UI_auxiliary.add_diagram_event("bar", "ButtonRelease-1", click_end)

        # UI_auxiliary.all_del_diagram_event("bar")

        # UI_auxiliary.del_diagram_event("bar", "ButtonRelease-1", click_end)

        # UI_auxiliary.edit_timeline_range = edit_timeline_range

        return UI_auxiliary


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
