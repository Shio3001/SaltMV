# coding:utf-8
from tkinter.constants import TOP
from pysrc.elements import make_id
import sys
import os
import copy

import random
import math
import threading
import datetime
import inspect
import time
import sounddevice
import wave
import cv2


class InitialValue:
    def __init__(self, window_control):  # data ←継承元(ファイルが違う＋プラグイン形式なのでこのような形に)
        self.window_control = window_control
        self.operation = self.window_control.operation

        self.time_lime_space_flag = 0
        self.nowtime_bar = None
        self.layer_draw = 0
        # self.window_control.edit_control_auxiliary.now_time = 0
        # self.redo_undo_stack = []
        # self.tthis_type_safe = ["media_length",]
        # self.add_type_safe_obj = ["add", "mov", "del", "split", "lord"]
        # self.add_type_safe_frame = ["f_add", "f_mov", "f_del"]

    def main(self):
        def undo_run(event=None):
            self.operation["undo"].confirmed_insert()
        self.window_control.add_window_event("Command-Key-z", undo_run)

        def undo_run_frame(undo):
            now_key_frame = self.window_control.edit_control_auxiliary.get_key_frame(undo.media_id)
            del_undo_frame(undo.media_id, now_key_frame)
            self.window_control.edit_control_auxiliary.media_object_had_layer(undo.media_id, undo.target_media_data)
            undo_make_frame(undo.media_id, undo.media_id_key_frame)

        def del_undo_frame(media_id, id_time):
            for k in id_time.keys():
                if k in ["default_sta", "default_end"]:
                    continue
                # print(" - undo : 削除 ", k)
                self.window_control.timeline_object[media_id].callback_operation.event("tihs_del_{0}".format(k), info=False)

        def undo_mov_frame(media_id, id_time):
            for point_key, point_val in zip(id_time.keys(), id_time.values()):
                if point_key in ["default_sta", "default_end"]:
                    continue

                print("point_val, media_id, point_key", point_val, media_id, point_key)
                # self.window_control.timeline_object[media_id].make_KeyFrame(uu_id=point_key, pos_f=point_val)

                self.window_control.edit_control_auxiliary.move_key_frame(point_val, media_id, point_key)
                self.window_control.timeline_object[media_id].pxf.set_f_ratio_sub_point(point_key, point_val)
                # self.window_control.timeline_object[media_id].callback_operation.event("sub_mov", info=self.window_control.timeline_object[media_id].pxf.get_event_data())

        def undo_make_frame(media_id, id_time):
            for point_key, point_val in zip(id_time.keys(), id_time.values()):
                if point_key in ["default_sta", "default_end"]:
                    continue
                self.window_control.timeline_object[media_id].make_KeyFrame(uu_id=point_key, pos_f=point_val)
                # print(" + undo : 追加 ", point_key, point_val)

        def undo_run_obj(undo):
            add_type = undo.add_type

            old_data_obj = undo.target_media_data[0]
            old_data_layer = undo.target_media_data[1]

            if add_type == "add":  # 削除
                self.window_control.edit_control_auxiliary.callback_operation.event("element_ui_all_del")

                self.window_control.edit_control_auxiliary.media_object_had_layer(undo.media_id, undo.target_media_data)
                self.window_control.timeline_object[old_data_obj.obj_id].media_object_del(stack=False)

            if add_type == "mov":

                del_undo_frame(old_data_obj.obj_id, undo.media_id_key_frame)
                undo_make_frame(old_data_obj.obj_id, undo.media_id_key_frame)

                self.window_control.timeline_object[old_data_obj.obj_id].send_parameter_control()
                self.window_control.edit_control_auxiliary.media_object_had_layer(undo.media_id, undo.target_media_data)

                sta_f = old_data_obj.installation[0]  # 開始地点解釈
                end_f = old_data_obj.installation[1]

                get_scene = self.window_control.edit_control_auxiliary.scene()
                layer_number = get_scene.layer_group.layer_layer_id[old_data_layer]  # 所属レイヤー解釈
                print("所属レイヤー解釈", old_data_layer, layer_number)

                new_layer_id = self.window_control.edit_control_auxiliary.layer_number_to_layer_id(layer_number)
                self.window_control.edit_control_auxiliary.layer_id_set(undo.media_id, new_layer_id)

                self.window_control.timeline_object[old_data_obj.obj_id].edit_layer(layer_number)
                frame_len = get_scene.editor["len"]

                self.window_control.timeline_object[old_data_obj.obj_id].pxf.init_set_sta_end_f(sta=0, end=frame_len)
                self.window_control.timeline_object[old_data_obj.obj_id].pxf.set_sta_end_f(sta=self.scrollbar_sta_end[0], end=self.scrollbar_sta_end[1])

                self.window_control.timeline_object[old_data_obj.obj_id].pxf.set_f_ratio(position=sta_f, size=end_f - sta_f)
                self.window_control.timeline_object[old_data_obj.obj_id].callback_operation.event("mov", info=self.window_control.timeline_object[old_data_obj.obj_id].pxf.get_event_data())

                undo_mov_frame(old_data_obj.obj_id, undo.media_id_key_frame)

            if add_type == "split":
                self.window_control.timeline_object[old_data_obj.obj_id].send_parameter_control()
                old_data_split = undo.target_media_data_split[0]
                old_data_split_layer = undo.target_media_data_split[1]

                del_undo_frame(undo.split_media_id, undo.split_media_id_key_frame)
                del_undo_frame(undo.media_id, undo.media_id_key_frame)
                del_object_ui(undo.split_media_id)
                undo_make_frame(old_data_obj.obj_id, undo.media_id_key_frame)

                self.window_control.edit_control_auxiliary.media_object_had_layer(undo.media_id, undo.target_media_data)

                sta_f = old_data_obj.installation[0]  # 開始地点解釈
                end_f = old_data_obj.installation[1]

                get_scene = self.window_control.edit_control_auxiliary.scene()
                layer_number = get_scene.layer_group.layer_layer_id[old_data_layer]  # 所属レイヤー解釈
                self.window_control.timeline_object[old_data_obj.obj_id].edit_layer(layer_number)
                frame_len = get_scene.editor["len"]

                self.window_control.timeline_object[old_data_obj.obj_id].pxf.init_set_sta_end_f(sta=0, end=frame_len)
                self.window_control.timeline_object[old_data_obj.obj_id].pxf.set_sta_end_f(sta=self.scrollbar_sta_end[0], end=self.scrollbar_sta_end[1])

                self.window_control.timeline_object[old_data_obj.obj_id].pxf.set_f_ratio(position=sta_f, size=end_f - sta_f)
                self.window_control.timeline_object[old_data_obj.obj_id].callback_operation.event("mov", info=self.window_control.timeline_object[old_data_obj.obj_id].pxf.get_event_data())

                undo_mov_frame(old_data_obj.obj_id, undo.media_id_key_frame)

            if add_type == "del":  # 再追加
                self.window_control.edit_control_auxiliary.media_object_had_layer(undo.media_id, undo.target_media_data)
                self.window_control.edit_control_auxiliary.callback_operation.event("element_ui_all_del")

                # self.window_control.edit_control_auxiliary.media_object_had_layer(old_data_obj.obj_id, old_data)
                sta_f = old_data_obj.installation[0]  # 開始地点解釈
                end_f = old_data_obj.installation[1]  # 終了地点解釈
                get_scene = self.window_control.edit_control_auxiliary.scene()
                layer_number = get_scene.layer_group.layer_layer_id[old_data_layer]  # 所属レイヤー解釈
                make_object(old_data_obj.obj_id, sta=sta_f, end=end_f, layer_number=layer_number)

                for point_key, point_val in zip(old_data_obj.effect_point_internal_id_time.keys(), old_data_obj.effect_point_internal_id_time.values()):
                    self.window_control.edit_control_auxiliary.add_key_frame_point_onely(point_val, old_data_obj.obj_id, point_key)

                    if point_key in ["default_sta", "default_end"]:
                        continue

                    self.window_control.timeline_object[old_data_obj.obj_id].make_KeyFrame(uu_id=point_key, pos_f=point_val)

                self.window_control.timeline_object[old_data_obj.obj_id].send_parameter_control()
                undo_mov_frame(old_data_obj.obj_id, undo.media_id_key_frame)

        def undo_run_effect(undo):
            # print("undo_run_effect", undo.media_id, undo.target_media_data)
            self.window_control.edit_control_auxiliary.media_object_had_layer(undo.media_id, undo.target_media_data)
            old_data_obj = undo.target_media_data[0]
            old_data_layer = undo.target_media_data[1]

            # self.window_control.edit_control_auxiliary.callback_operation.event("media_lord")

            self.window_control.timeline_object[undo.media_id].send_parameter_control()

            if undo.add_type == "effect_add":
                pass
            if undo.add_type == "effect_del":
                pass

        def undo_lord(undo):
            # self.window_control.edit_control_auxiliary.media_object_had_layer(undo.media_id, undo.target_media_data)

            if undo.add_type == "lord":
                for i in self.window_control.timeline_object.values():
                    i.media_object_del(stack=False)

                self.window_control.timeline_object = {}

        def stack_add_timelime_effect(stop_once=None, add_type=None, media_id=None):
            stop_once = self.window_control.operation["undo"].add_stack(stop_once=stop_once, media_id=media_id, classification="timelime_effect", add_type=add_type, func=undo_run_effect)
            if stop_once:
                return stop_once

        def stack_add_timelime_media(stop_once=None, add_type=None, media_id=None):
            stop_once = self.window_control.operation["undo"].add_stack(stop_once=stop_once, media_id=media_id, classification="timelime_media", add_type=add_type, func=undo_run_obj)
            if stop_once:
                return stop_once

        def stack_add_timelime_keyframe(stop_once=None, add_type=None, media_id=None):
            stop_once = self.window_control.operation["undo"].add_stack(stop_once=stop_once, media_id=media_id, classification="timelime_keyframe", add_type=add_type, func=undo_run_frame)
            if stop_once:
                return stop_once
        # stack_add_timelime_media(add_type="lord", media_id=None)
        self.window_control.operation["undo"].add_stack(classification="timelime_media", add_type="lord", func=undo_lord)

        # old_data = [None, 0]
        # stack_add_timelime_media("lord", old_data)

        # self.window_control.add_window_event("Command-Key-z", undo_stack)

        self.window_control.new_canvas("timeline")
        self.window_control.edit_canvas_size("timeline", x=1000, y=1000)
        self.window_control.edit_canvas_position("timeline", x=0, y=0)
        self.window_control.window_title_set("タイムライン")

        # #print(button.canvas_data.territory["main"].diagram)

        shape = []

        timeline_left = 50  # タイムラインの左側のshape(x)
        timeline_up = 50  # タイムラインの上側のshape(y)
        timeline_size = 20  # タイムラインの幅(y)

        left_up_color = "#ffffff"

        shape.append(None)
        shape[0] = self.window_control.new_parts("timeline", "s0", parts_name="shape")  # 左側のやつ
        shape[0].edit_territory_size(x=timeline_left)
        shape[0].edit_diagram_color("0", left_up_color)

        shape.append(None)
        shape[1] = self.window_control.new_parts("timeline", "s1", parts_name="shape")  # 上側のやつ
        shape[1].edit_territory_size(y=timeline_up)
        shape[1].edit_territory_position(x=timeline_left)
        shape[1].edit_diagram_color("0", left_up_color)

        self.window_control.timeline_object = {}

        timeline_scroll = self.window_control.new_parts("timeline", "srob", parts_name="scroll_x")
        timeline_scroll.set_lr_edit(True)
        timeline_scroll.pxf.init_set_sta_end_f(sta=0, end=100)

        scroll_size = 20
        timeline_scroll.edit_territory_size(y=scroll_size)
        timeline_scroll.edit_territory_position(x=timeline_left, y=timeline_up - scroll_size)
        timeline_scroll.territory_draw()

        self.end_to_sta_time = 0

        def get_permission_elapsed_time():
            bool_time = 0.2 <= time.time() - self.end_to_sta_time
            return bool_time

        self.nowtime_bar = self.window_control.new_parts("timeline", "nowtime_bar", parts_name="timeline_nowtime")
        self.nowtime_bar.get_permission_elapsed_time = get_permission_elapsed_time
        self.nowtime_bar.pxf.init_set_sta_end_f(sta=0, end=100)
        self.nowtime_bar.edit_territory_size(y=10)
        self.nowtime_bar.edit_territory_position(x=timeline_left, y=timeline_up)
        self.nowtime_bar.territory_draw()

        # ##print(self.window_control.edit_control_auxiliary.now_time)

        def now_time_edit(scroll_data):
            self.time_lime_space_flag == 0
            self.window_control.edit_control_auxiliary.now_time_update(scroll_data)

        def time_lime_space(event):
            self.preview_move()

        self.window_control.add_window_event("space", time_lime_space)

        self.nowtime_bar.callback_operation.set_event("mov", now_time_edit)

        # now_layer = 0

        def timeline_nowtime_approval_True(t=None):
            # self.window_control.window.update()
            self.nowtime_bar.edit_diagram_color("now", "#ff0000")
            self.nowtime_bar.click_flag = True
            self.end_to_sta_time = time.time()
            print("許可")

        def timeline_nowtime_approval_False(t=None):
            self.nowtime_bar.edit_diagram_color("now", "#0000ff")
            self.nowtime_bar.click_flag = False
            print("停止")

        timeline_scroll.callback_operation.set_event("sta", timeline_nowtime_approval_False)
        timeline_scroll.callback_operation.set_event("end", timeline_nowtime_approval_True)

        # self.window_control.edit_control_auxiliary.callback_operation.set_event("del_layer_elements", del_layer_elements)

        def media_object_separate(send):
            timeline_nowtime_approval_False()

            media_id, click_f_pos = send
            scroll_data = self.window_control.timeline_object[media_id].pxf.get_event_data()
            if not scroll_data.ratio_f[0] < click_f_pos < scroll_data.ratio_f[0] + scroll_data.ratio_f[1]:
                # #print("返送")
                return

            obj_stop_once = stack_add_timelime_media(add_type="split", media_id=media_id, stop_once=True)

            a_size = click_f_pos - scroll_data.ratio_f[0]

            self.window_control.timeline_object[media_id].mov_lock = True
            old_data = self.window_control.edit_control_auxiliary.media_object_had_layer(media_id)

            copy_obj, layer_id = self.window_control.edit_control_auxiliary.copy_object_elements(media_id, sta=click_f_pos, end=scroll_data.ratio_f[1])
            layer_number = self.window_control.edit_control_auxiliary.layer_id_to_layer_number(layer_id)
            make_object(copy_obj.obj_id, sta=click_f_pos, end=scroll_data.ratio_f[0] + scroll_data.ratio_f[1], layer_number=layer_number)

            obj_stop_once[1](obj_stop_once[0], split_media_id=copy_obj.obj_id)

            self.window_control.timeline_object[copy_obj.obj_id].mov_lock = True

            items = copy.deepcopy(self.window_control.timeline_object[media_id].pxf.sub_point_f).items()

            for k, v in items:
                # print(k, v)
                if v < click_f_pos:  # 左側
                    pass
                    # print(" < < < < < < < < < < < < < < < < < < < < 左側", k, v)
                if v > click_f_pos:  # 右側
                    pass
                    # print(" > > > > > > > > > > > > > > > > > > > >右側", k, v)
                    # self.window_control.timeline_object[media_id].pxf.sub_point_f[k] 矛盾

                    frame = copy.deepcopy(self.window_control.timeline_object[media_id].pxf.sub_point_f[k])

                    if k == "default_end" or k == "default_sta":
                        self.window_control.edit_control_auxiliary.del_key_frame_point(media_id, k)
                        continue

                    self.window_control.timeline_object[media_id].callback_operation.event("tihs_del_{0}".format(k), info=False)
                    self.window_control.timeline_object[copy_obj.obj_id].make_KeyFrame(uu_id=k, pos_f=frame)
                    self.window_control.edit_control_auxiliary.add_key_frame_point_onely(frame, copy_obj.obj_id, k)

                if v == click_f_pos:  # ちょうど一緒
                    # #print("等")
                    self.window_control.timeline_object[media_id].callback_operation.event("tihs_del_{0}".format(k), info=False)

            split_items = copy.deepcopy(self.window_control.timeline_object[copy_obj.obj_id].pxf.sub_point_f).items()

            self.window_control.timeline_object[media_id].pxf.set_f_ratio(size=a_size)

            # この関数が原因だわ

            self.window_control.timeline_object[media_id].mov_lock = False
            self.window_control.timeline_object[copy_obj.obj_id].mov_lock = False

            self.window_control.timeline_object[media_id].callback_operation.event("mov", info=self.window_control.timeline_object[media_id].pxf.get_event_data())
            self.window_control.timeline_object[media_id].callback_operation.event("end", info=self.window_control.timeline_object[media_id].pxf.get_event_data())

            timeline_nowtime_approval_True()
            print("分割処理終了")

            # self.window_control.window.update()

        def reflect_timeline_to_movie(scroll_data):
            media_id = scroll_data.option_data["media_id"]
            self.window_control.edit_control_auxiliary.edit_object_installation(media_id, sta=scroll_data.ratio_f[0], end=scroll_data.ratio_f[0] + scroll_data.ratio_f[1])

            # これを生成時に実行しないとダメ__?

        self.window_control.layer_object = []

        def new_layer():
            new_layer = self.window_control.edit_control_auxiliary.add_layer_elements()
            new_len_layer = len(new_layer.layer_layer_id)
            make_layer(new_len_layer)
            # #print(new_layer.layer_id)

        def make_layer(new_len_layer):

            now_len_layer = len(self.window_control.layer_object)

            for i in range(now_len_layer, new_len_layer):
                now_lb = self.window_control.new_parts("timeline", "layer_{0}".format(i), parts_name="timeline_layer")  # 左側のやつ
                now_lb.set_layer_number(i)

                now_lb.new_obj = new_obj
                now_lb.timeline_nowtime_approval_False = timeline_nowtime_approval_False  # 定義
                now_lb.timeline_nowtime_approval_True = timeline_nowtime_approval_True  # 定義
                self.window_control.layer_object.append(now_lb)

        def new_obj(layer_number=0, add_time=0):
            new_object = self.window_control.edit_control_auxiliary.add_object_elements(layer_number=layer_number)
            nowtime = self.window_control.edit_control_auxiliary.now_time_update()

            nowtime += add_time
            make_object(new_object.obj_id, sta=nowtime, end=nowtime+20, layer_number=layer_number)

            # old_data = self.window_control.edit_control_auxiliary.media_object_had_layer(new_object.obj_id)
            # stack_add("add", old_data)
            stack_add_timelime_media(add_type="add", media_id=new_object.obj_id)
            # stack_add_timelime_keyframe(add_type="lord", media_id=new_object.obj_id)

        def layer_updown(mouse_pos):  # この関数重たそうだから要調整かな
            sta, end,  obj_id, edit_layer = mouse_pos
            now_layer = self.window_control.edit_control_auxiliary.get_now_layer_number(obj_id)

            layer_num = len(self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.layer_layer_id)

            new_layer = end // timeline_size

            if new_layer > layer_num - 1:
                new_layer = layer_num - 1

            if new_layer < 0:
                new_layer = 0

            # print("new_layer", new_layer)

            new_layer_id = self.window_control.edit_control_auxiliary.layer_number_to_layer_id(new_layer)
            self.window_control.edit_control_auxiliary.layer_id_set(obj_id, new_layer_id)
            # self.window_control.edit_control_auxiliary.edit_data.scenes[self.window_control.edit_control_auxiliary.edit_data.now_scene].layer_group.object_group[obj_id][1] = new_layer_id
            edit_layer(new_layer)

        def del_object_ui(media_id):
            # print("削除対象物:", media_id)
            self.window_control.timeline_object[media_id].UI_auxiliary.del_territory()
            # del self.window_control.timeline_object[media_id].callback_operation
            del self.window_control.timeline_object[media_id]
            self.window_control.edit_control_auxiliary.del_object_elements(media_id)
            self.window_control.edit_control_auxiliary.callback_operation.event("element_del")

        def all_del_object_ui():
            for media_id in self.window_control.timeline_object.keys():
                self.window_control.timeline_object[media_id].UI_auxiliary.del_territory()
                self.window_control.edit_control_auxiliary.del_object_elements(media_id)
                # ##print("削除 {0}".format(media_id))

            self.window_control.timeline_object = {}
            self.window_control.edit_control_auxiliary.callback_operation.event("element_del")
            # ##print(self.window_control.timeline_object)

        # def media_objct_click():

        """
        def parameter(media_id):
            obj = self.window_control.edit_control_auxiliary.media_object(media_id)
            elements = obj.effect_group
            # self.window_control.edit_control_auxiliary.callback_operation.event("media_lord", info=())

            send = (elements, self.window_control.edit_control_auxiliary.now_time)
            func = self.window_control.edit_control_auxiliary.callback_operation.get_event("media_lord")[0]
            thread = threading.Thread(target=func, args=(send,))
            thread.start()
        """

        def make_object(media_id, sta=0, end=20, layer_number=0):
            option_data = {"media_id": media_id}

            # #print(len(self.window_control.timeline_object))

            new_obj = self.window_control.new_parts("timeline", media_id, parts_name="timeline_object", option_data=option_data)

            new_obj.timeline_send_data.set_timeline_nowtime_approval_False(timeline_nowtime_approval_False)  # 定義
            new_obj.timeline_send_data.set_timeline_nowtime_approval_True(timeline_nowtime_approval_True)  # 定義
            new_obj.timeline_send_data.set_stack_add_timelime_media(stack_add_timelime_media)
            new_obj.timeline_send_data.set_stack_add_timelime_keyframe(stack_add_timelime_keyframe)
            new_obj.timeline_send_data.set_stack_add_timelime_effect(stack_add_timelime_effect)

            # new_obj.set_right_click_pop()

            new_obj.UI_auxiliary.edit_territory_position(x=timeline_left, y=timeline_up)
            new_obj.UI_auxiliary.edit_diagram_size("bar", y=timeline_size)
            new_obj.callback_operation.set_event("mov", reflect_timeline_to_movie)  # コールバック関数登録
            new_obj.callback_operation.set_event("updown", layer_updown)
            new_obj.callback_operation.set_event("del", del_object_ui)
            new_obj.callback_operation.set_event("separate", media_object_separate, duplicate=False)
            new_obj.callback_operation.set_event("sta", timeline_nowtime_approval_False)
            new_obj.callback_operation.set_event("end", timeline_nowtime_approval_True)
            new_obj.edit_layer(layer_number)

            frame_len = self.window_control.edit_control_auxiliary.scene_editor()["len"]

            new_obj.pxf.init_set_sta_end_f(sta=0, end=frame_len)
            new_obj.pxf.set_sta_end_f(sta=self.scrollbar_sta_end[0], end=self.scrollbar_sta_end[1])
            new_obj.pxf.set_f_ratio(position=sta, size=end - sta)

            new_obj.callback_operation.event("mov", info=new_obj.pxf.get_event_data())

            self.window_control.timeline_object[media_id] = new_obj

            # del new_obj
            window_size_edit()

        # self.loading_movie_data_try = 0

        def loading_movie_data(new=None):
            self.window_control.operation["undo"].all_del_stack()

            for media_ui in self.window_control.timeline_object.values():
                media_ui.del_territory()

            self.window_control.timeline_object = {}

            if not new is None:
                self.window_control.edit_control_auxiliary.change_now_scene(new)
            # ここで現在シーンが変わる

            get_scene = self.window_control.edit_control_auxiliary.scene()
            frame_len = get_scene.editor["len"]
            bpm = get_scene.editor["bpm"]
            fps = get_scene.editor["fps"]

            obj_list = [get_scene.layer_group.object_group.keys(), get_scene.layer_group.object_group.values()]
            timeline_scroll.callback_operation.event("mov", info=timeline_scroll.pxf.get_event_data())

            nowtime = self.window_control.edit_control_auxiliary.now_time_update()

            self.nowtime_bar.pxf.init_set_sta_end_f(sta=0, end=frame_len)
            self.nowtime_bar.frame_set(nowtime)

            self.timeline_bpm.pxf.init_set_sta_end_f(sta=0, end=frame_len)

            len_layer = len(get_scene.layer_group.layer_layer_id)
            make_layer(len_layer)

            for obj_k, obj_v in zip(obj_list[0], obj_list[1]):
                # print(obj_k, "実行")
                sta_f = obj_v[0].installation[0]  # 開始地点解釈
                end_f = obj_v[0].installation[1]  # 終了地点解釈

                for e in obj_v[0].effect_group.values():
                    print("effect_point_internal_id_point", e.effect_point_internal_id_point)

                layer_number = get_scene.layer_group.layer_layer_id[obj_v[1]]  # 所属レイヤー解釈
                make_object(media_id=obj_k, sta=sta_f, end=end_f, layer_number=layer_number)

                for point_key, point_val in zip(obj_v[0].effect_point_internal_id_time.keys(), obj_v[0].effect_point_internal_id_time.values()):
                    self.window_control.edit_control_auxiliary.add_key_frame_point_onely(point_val, obj_k, point_key)

                    if point_key in ["default_sta", "default_end"]:
                        continue

                    self.window_control.timeline_object[obj_k].make_KeyFrame(uu_id=point_key, pos_f=point_val)

            self.timeline_bpm.set_bpm(fps=fps, bpm=bpm)
            window_size_edit()

            self.window_control.edit_control_auxiliary.callback_operation.event("preview_setup")

        def edit_data_reset():
            all_del_object_ui()
            self.window_control.edit_control_auxiliary.new_edit_data()
            loading_movie_data()

        self.window_control.edit_control_auxiliary.callback_operation.set_event("reset", edit_data_reset)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("file_input_before", all_del_object_ui)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("file_input_after", loading_movie_data)

        # new_object(s)

        # def sta_end_f_

        def obj_long_edit(media_obj, view_frame_len, view_sta_f, view_end_f):
            media_obj.pxf.init_set_sta_end_f(sta=0, end=view_frame_len)
            media_obj.pxf.set_sta_end_f(sta=view_sta_f, end=view_end_f)
            media_obj.pxf.set_f_ratio()

        self.timeline_bpm = self.window_control.new_parts("timeline", "bpm_view", parts_name="timeline_bpm")
        self.timeline_bpm.edit_territory_position(x=timeline_left, y=timeline_up)
        self.timeline_bpm.territory_draw()

        def timeline_view_range(scroll_data):
            view_frame_len = self.window_control.edit_control_auxiliary.scene().editor["len"]

            # sta_end_long = scroll_data.sta_end_f[1] - scroll_data.sta_end_f[0]

            view_sta_f = round(view_frame_len * (scroll_data.ratio_f[0] / 100))
            view_end_f = round(view_frame_len * ((scroll_data.ratio_f[0] + scroll_data.ratio_f[1]) / 100))

            self.scrollbar_sta_end = [view_sta_f, view_end_f]

            self.nowtime_bar.pxf.init_set_sta_end_f(sta=0, end=view_frame_len)
            self.nowtime_bar.pxf.set_sta_end_f(sta=view_sta_f, end=view_end_f)
            self.nowtime_bar.pxf.set_f_ratio()
            [obj_long_edit(media_obj, view_frame_len, view_sta_f, view_end_f) for media_obj in self.window_control.timeline_object.values()]

            self.timeline_bpm.pxf.init_set_sta_end_f(sta=0, end=view_frame_len)
            self.timeline_bpm.pxf.set_sta_end_f(sta=view_sta_f, end=view_end_f)
            self.timeline_bpm.set_bpm()

            # with self.window_control.edit_control_auxiliary.ThreadPoolExecutor() as executor:
            #    [executor.submit(obj_long_edit(media_obj, frame_len, sta_f, end_f)) for media_obj in self.window_control.timeline_object.values()]

        timeline_scroll.callback_operation.set_event("mov", timeline_view_range)  # コールバック関数登録
        timeline_scroll.callback_operation.event("mov", info=timeline_scroll.pxf.get_event_data())

        def get_timelime_scroll_status():
            return self.scrollbar_sta_end

        self.window_control.edit_control_auxiliary.callback_operation.set_event("get_timelime_scroll_status", get_timelime_scroll_status)

        def window_size_edit(e=None):
            size_x, size_y = self.window_control.get_window_size()
            self.window_control.edit_canvas_size("timeline",  x=size_x, y=size_y)

            timeline_width = size_x - timeline_left
            timeline_hight = size_y - timeline_up

            shape[0].edit_territory_size(y=size_y)
            shape[1].edit_territory_size(x=timeline_width)

            self.nowtime_bar.pxf.set_sta_end_px(sta=timeline_left, end=size_x, space=0)
            self.nowtime_bar.edit_territory_size(x=timeline_width, y=timeline_hight)
            self.nowtime_bar.edit_diagram_size("now", y=timeline_hight)
            self.nowtime_bar.pxf.set_f_ratio()

            # print("ウィンドウサイズ", size_x, size_y)

            # length = self.window_control.edit_control_auxiliary.scene().editer["len"]
            timeline_scroll.edit_territory_size(x=timeline_width)
            timeline_scroll.pxf.set_sta_end_px(sta=timeline_left, end=size_x, space=0)
            timeline_scroll.pxf.set_f_ratio()

            for i in self.window_control.timeline_object.values():
                i.UI_auxiliary.edit_territory_size(x=timeline_width, y=timeline_hight)
                i.pxf.set_sta_end_px(sta=timeline_left, end=size_x)
                i.pxf.set_f_ratio()

            # timeline_scroll.pxf.set_scroll_minimum_value_px(self.window_control.timeline_object[-1].pxf.f_px_func(1))

            shape[0].territory_draw()
            shape[1].territory_draw()

            self.timeline_bpm.pxf.set_sta_end_px(sta=timeline_left, end=size_x, space=0)
            self.timeline_bpm.set_bpm(bpm_y_view_size=timeline_hight)

        self.window_control.add_window_event("Configure", window_size_edit)
        window_size_edit()

        get_scene = self.window_control.edit_control_auxiliary.scene()
        bpm = get_scene.editor["bpm"]
        fps = get_scene.editor["fps"]
        self.timeline_bpm.set_bpm(fps=fps, bpm=bpm)

        """
        scene_now_view = self.window_control.new_parts("timeline", "scene_now_view", parts_name="textbox")
        scene_now_view.edit_territory_position(x=0, y=0)
        scene_now_view.edit_territory_size(x=20, y=10)
        scene_now_view.territory_draw()
        """

        # def now_time_flag_edit():
        #    self.nowtime_bar.scene_change_flag = False

        def editor_func(editor_func_send):

            timeline_nowtime_approval_False()

            editor_func_name, editor_func_val = editor_func_send
            print("editor_func_send", editor_func_send)

            self.window_control.edit_control_auxiliary.get_set_scene_edior(name=editor_func_name, data=editor_func_val)

            loading_movie_data(new=self.window_control.edit_control_auxiliary.scene_id())
            self.window_control.edit_control_auxiliary.callback_operation.event("preview_setup")

            timeline_nowtime_approval_True()

        def editor_setting_change(option_data):
            timeline_nowtime_approval_False()

            self.popup = self.window_control.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.window_control.window, popup=True)

            pop_list = []

            edior = self.window_control.edit_control_auxiliary.get_set_scene_edior()
            self.window_control.edit_control_auxiliary.callback_operation.set_event("text_input_end", editor_func, duplicate=False)
            for k in edior.keys():
                EditorGet_file = self.window_control.edit_control_auxiliary.get_bool_editor_select_file(k)
                EditorGet_folder = self.window_control.edit_control_auxiliary.get_bool_editor_select_folder(k)

                edior_get = EditorGet(self.window_control.edit_control_auxiliary, k, edior[k], EditorGet_file, EditorGet_folder)
                scene_name_func = ("{0} 現在:{1}".format(k, edior[k]), edior_get.run)
                pop_list.append(scene_name_func)

            self.popup.set(pop_list)

            background_mouse, _, _, xy = self.window_control.get_window_contact()
            mouse = [0, 0]
            for i in range(2):
                mouse[i] = background_mouse[i] + xy[i]

            self.popup.show(mouse[0], mouse[1])

            timeline_nowtime_approval_True()

        def scene_change(option_data):
            # self.nowtime_bar.one_lock()
            timeline_nowtime_approval_False()

            self.popup = self.window_control.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.window_control.window, popup=True)

            scene_name_list = self.window_control.edit_control_auxiliary.get_scene_name_list()

            pop_list = []

            for k in scene_name_list:
                scene_get = SceneGet(k, loading_movie_data, timeline_nowtime_approval_False, scene_list_button)

                scene_name_func = ("　　 : " + k, scene_get.change) if k != self.window_control.edit_control_auxiliary.edit_data.now_scene else ("現在 : " + k, scene_get.change)
                pop_list.append(scene_name_func)

            # print(scene_name_list, pop_list)

            self.popup.set(pop_list)

            background_mouse, _, _, xy = self.window_control.get_window_contact()
            mouse = [0, 0]
            for i in range(2):
                mouse[i] = background_mouse[i] + xy[i]

            self.popup.show(mouse[0], mouse[1])

            timeline_nowtime_approval_True()

        list_button = 105

        scene_list_button = self.window_control.new_parts("timeline", "scene_list_button", parts_name="button")  # 左側のやつ
        scene_list_button.edit_territory_size(x=100, y=timeline_up - scroll_size - 10)
        scene_list_button.edit_territory_position(x=timeline_left, y=5)
        scene_list_button.edit_diagram_color("background", "#229922")
        scene_list_button.edit_diagram_color("text", "#ffffff")
        scene_list_button.diagram_stack("text", True)
        scene_list_button.edit_diagram_text("text", text="シーン選択")
        scene_list_button.territory_draw()
        scene_list_button.callback_operation.set_event("button", scene_change)

        edit_settings_button = self.window_control.new_parts("timeline", "edit_settings_button", parts_name="button")  # 左側のやつ
        edit_settings_button.edit_territory_size(x=100, y=timeline_up - scroll_size - 10)
        edit_settings_button.edit_territory_position(x=timeline_left+list_button, y=5)
        edit_settings_button.edit_diagram_color("background", "#229922")
        edit_settings_button.edit_diagram_color("text", "#ffffff")
        edit_settings_button.diagram_stack("text", True)
        edit_settings_button.edit_diagram_text("text", text="編集設定")
        edit_settings_button.territory_draw()
        edit_settings_button.callback_operation.set_event("button", editor_setting_change)

        def run_button_func(r=None):
            self.preview_move()
            self.nowtime_bar.one_lock()

        self.run_button = self.window_control.new_parts("timeline", "run_button", parts_name="button")  # 左側のやつ
        self.run_button.edit_territory_size(x=100, y=timeline_up - scroll_size - 10)
        self.run_button.edit_territory_position(x=timeline_left+2*list_button, y=5)
        self.run_button.edit_diagram_color("background", "#229922")
        self.run_button.edit_diagram_color("text", "#ffffff")
        self.run_button.diagram_stack("text", True)
        self.run_button.edit_diagram_text("text", text="再生")
        self.run_button.territory_draw()
        self.run_button.callback_operation.set_event("button", run_button_func)

        def run_cash_clear_func(r=None):
            self.nowtime_bar.one_lock()
            self.window_control.edit_control_auxiliary.callback_operation.event("cash_clear")

        self.run_cash_clear = self.window_control.new_parts("timeline", "run_cash_clear", parts_name="button")  # 左側のやつ
        self.run_cash_clear.edit_territory_size(x=100, y=timeline_up - scroll_size - 10)
        self.run_cash_clear.edit_territory_position(x=timeline_left+3*list_button, y=5)
        self.run_cash_clear.edit_diagram_color("background", "#222299")
        self.run_cash_clear.edit_diagram_color("text", "#ffffff")
        self.run_cash_clear.diagram_stack("text", True)
        self.run_cash_clear.edit_diagram_text("text", text="一時保存削除", font_size=15)
        self.run_cash_clear.territory_draw()
        self.run_cash_clear.callback_operation.set_event("button", run_cash_clear_func)

        def add_scene():
            self.window_control.edit_control_auxiliary.add_scene_elements()

        new_layer()

        self.timeline_menubar = self.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.window_control.window)
        main_menubar_list = [("ファイル", "終了", self.window_control.window_exit), ("新規", "シーン", add_scene, "レイヤー", new_layer)]
        self.timeline_menubar.set(main_menubar_list)
        self.window_control.window_title_set("タイムライン")
        self.window_control.window_size_set(x=1200, y=700)

        return self.window_control

    def preview_move(self):
        self.time_lime_space_flag = 1 - self.time_lime_space_flag

        if self.time_lime_space_flag == 0:  # off
            self.window_control.edit_control_auxiliary.callback_operation.event("sound_stop")

            self.run_button.edit_diagram_text("text", text="再生")
            self.run_button.edit_diagram_color("background", "#229922")

        if self.time_lime_space_flag == 1:  # on
            self.window_control.edit_control_auxiliary.callback_operation.event("re_scene")

            self.run_button.edit_diagram_text("text", text="停止")
            self.run_button.edit_diagram_color("background", "#992222")

            process_time = self.window_control.edit_control_auxiliary.get_now_time()
            fps = self.window_control.edit_control_auxiliary.scene_editor()["fps"]
            mov_len = self.window_control.edit_control_auxiliary.scene_editor()["len"]
            one_fps = 1 / fps

            self.window_control.edit_control_auxiliary.callback_operation.event("sound_init")

            while True:
                if process_time >= mov_len or self.time_lime_space_flag == 0:
                    break

                print("再生", process_time)

                sta_section_time = time.time()

                self.window_control.edit_control_auxiliary.callback_operation.event("preview", info=(process_time, True))
                self.nowtime_bar.preview_frame_set(process_time)

                update_section_time = time.time()

                # if not self.window_control.edit_control_auxiliary.scene_editor()["preview"] == "opencv":
                self.window_control.window.update()

                end_section_time = time.time()
                section = end_section_time - sta_section_time

                sleep_time = one_fps - section
                print("sleep_time ", sleep_time, one_fps, section, "うちupdate時間 :", end_section_time - update_section_time, "update直接以外の時間 :", update_section_time - sta_section_time)

                if sleep_time > 0:
                    print(sleep_time)
                    time.sleep(sleep_time)

                fps_end_section_time = time.time()
                print("fps_time ", fps_end_section_time - sta_section_time)

                process_time += 1


class CentralRole:
    pass


class EditorGet:
    def __init__(self, edit_control_auxiliary, name, init_val, file=False, folder=False):
        self.name = name
        self.edit_control_auxiliary = edit_control_auxiliary
        self.init_val = init_val
        self.file = file
        self.folder = folder

    def run(self):
        self.edit_control_auxiliary.callback_operation.event("set_init_val", info=self.init_val)

        if self.file:
            self.edit_control_auxiliary.callback_operation.event("text_input_request_file_open", info=self.name)
        elif self.folder:
            self.edit_control_auxiliary.callback_operation.event("text_input_request_folder_open", info=self.name)
        else:
            self.edit_control_auxiliary.callback_operation.event("text_input_request", info=self.name)


class SceneGet:
    def __init__(self, scene_id, loading_movie_data, now_time_flag_edit, scene_list_button):
        self.scene_id = copy.deepcopy(scene_id)
        self.loading_movie_data = loading_movie_data
        now_time_flag_edit()
        self.scene_list_button = scene_list_button
        # self.change_now_scene = change_now_scene_func
        # self.scene_now_view = scene_now_view

    def change(self):

        self.scene_list_button.edit_diagram_color("background", "#111111")
        self.scene_list_button.territory_draw()

        self.loading_movie_data(new=self.scene_id)

        self.scene_list_button.edit_diagram_color("background", "#229922")
        self.scene_list_button.territory_draw()
        # self.scene_now_view.edit_diagram_text("textbox1", text=self.scene_id)
        # self.scene_now_view.territory_draw()
