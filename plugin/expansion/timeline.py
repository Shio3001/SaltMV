# coding:utf-8
from tkinter.constants import TOP
from elements import make_id
import sys
import os
import copy

import random
import math
import threading
import datetime
import inspect


class InitialValue:
    def __init__(self, data):  # data ←継承元(ファイルが違う＋プラグイン形式なのでこのような形に)
        self.data = data
        self.operation = self.data.operation
        self.data.all_data.now_time = 0
        #self.redo_undo_stack = []
        #self.tthis_type_safe = ["media_length",]
        #self.add_type_safe_obj = ["add", "mov", "del", "split", "lord"]
        #self.add_type_safe_frame = ["f_add", "f_mov", "f_del"]

    def main(self):
        def undo_run(event=None):
            self.operation["undo"].confirmed_insert()
        self.data.add_window_event("Command-Key-z", undo_run)

        def undo_run_frame(undo):
            old_effect_key_data = undo.target_media_data[0]
            old_media_id = undo.media_id
            #key_frame_id = old_data[2]

            key_frame_time_old_data = self.data.all_data.get_key_frame(old_media_id)
            for k in key_frame_time_old_data.keys():
                if k in ["default_sta", "default_end"]:
                    continue
                self.data.timeline_object[old_media_id].callback_operation.event("tihs_del_{0}".format(k), info=False)

            #self.data.all_data.get_key_frame(old_media_id, old_effect_key_data.effect_point_internal_id_time)

            self.data.all_data.media_object_had_layer(undo.media_id, undo.target_media_data)

            for point_key, point_val in zip(old_effect_key_data.effect_point_internal_id_time.keys(), old_effect_key_data.effect_point_internal_id_time.values()):
                if point_key in ["default_sta", "default_end"]:
                    continue
                self.data.timeline_object[old_media_id].make_KeyFrame(uu_id=point_key, pos_f=point_val)

        def undo_run_obj(undo):

            self.data.all_data.media_object_had_layer(undo.media_id, undo.target_media_data)

            add_type = undo.add_type

            print("操作", add_type)

            old_data_obj = undo.target_media_data[0]
            old_data_layer = undo.target_media_data[1]

            # self.data.timeline_object[old_data_obj.obj_id].send_parameter_control()

            self.data.all_data.callback_operation.event("media_lord")

            if add_type == "add":  # 削除

                self.data.timeline_object[old_data_obj.obj_id].media_object_del(stack=False)

            if add_type == "mov":
                #self.data.all_data.media_object_had_layer(old_data_obj.obj_id, old_data)
                sta_f = old_data_obj.installation[0]  # 開始地点解釈
                end_f = old_data_obj.installation[1]
                get_scene = self.data.all_data.scene()
                layer_number = get_scene.layer_group.layer_layer_id[old_data_layer]  # 所属レイヤー解釈

                frame_len = self.data.all_data.scene().editor["len"]

                print(old_data_obj.installation)

                self.data.timeline_object[old_data_obj.obj_id].pxf.init_set_sta_end_f(sta=0, end=frame_len)
                self.data.timeline_object[old_data_obj.obj_id].pxf.set_sta_end_f(sta=self.scrollbar_sta_end[0], end=self.scrollbar_sta_end[1])
                self.data.timeline_object[old_data_obj.obj_id].pxf.set_f_ratio(position=sta_f, size=end_f - sta_f)
                self.data.timeline_object[old_data_obj.obj_id].callback_operation.event("mov", info=self.data.timeline_object[old_data_obj.obj_id].pxf.get_event_data())

                #old_key_frame_data = [old_data_obj.effect_point_internal_id_time, old_data_obj.obj_id]
                undo_run_frame(undo)

            if add_type == "split":

                old_data_split = undo.target_media_data_split[0]
                old_data_split_layer = undo.target_media_data_split[1]

                self.data.timeline_object[old_data_split.obj_id].media_object_del(stack=False)

                #self.data.all_data.media_object_had_layer(old_data_obj.obj_id, old_data)
                sta_f = old_data_obj.installation[0]  # 開始地点解釈
                end_f = old_data_obj.installation[1]
                get_scene = self.data.all_data.scene()
                layer_number = get_scene.layer_group.layer_layer_id[old_data_layer]  # 所属レイヤー解釈

                frame_len = self.data.all_data.scene().editor["len"]

                print(old_data_obj.installation)

                undo_run_frame(undo)

                self.data.timeline_object[old_data_obj.obj_id].pxf.init_set_sta_end_f(sta=0, end=frame_len)
                self.data.timeline_object[old_data_obj.obj_id].pxf.set_sta_end_f(sta=self.scrollbar_sta_end[0], end=self.scrollbar_sta_end[1])
                self.data.timeline_object[old_data_obj.obj_id].pxf.set_f_ratio(position=sta_f, size=end_f - sta_f)
                self.data.timeline_object[old_data_obj.obj_id].callback_operation.event("mov", info=self.data.timeline_object[old_data_obj.obj_id].pxf.get_event_data())

                #old_key_frame_data = [old_data_obj.effect_point_internal_id_time, old_data_obj.obj_id]

            if add_type == "del":  # 再追加
                self.data.all_data.callback_operation.event("element_ui_all_del")

                #self.data.all_data.media_object_had_layer(old_data_obj.obj_id, old_data)
                sta_f = old_data_obj.installation[0]  # 開始地点解釈
                end_f = old_data_obj.installation[1]  # 終了地点解釈
                get_scene = self.data.all_data.scene()
                layer_number = get_scene.layer_group.layer_layer_id[old_data_layer]  # 所属レイヤー解釈
                make_object(old_data_obj.obj_id, sta=sta_f, end=end_f, layer_number=layer_number)

                for point_key, point_val in zip(old_data_obj.effect_point_internal_id_time.keys(), old_data_obj.effect_point_internal_id_time.values()):
                    self.data.all_data.add_key_frame(point_val, old_data_obj.obj_id, point_key)

                    if point_key in ["default_sta", "default_end"]:
                        continue

                    self.data.timeline_object[old_data_obj.obj_id].make_KeyFrame(uu_id=point_key, pos_f=point_val)

        def undo_lord(undo):
            #self.data.all_data.media_object_had_layer(undo.media_id, undo.target_media_data)

            if undo.add_type == "lord":
                for i in self.data.timeline_object.values():
                    i.media_object_del(stack=False)

                self.data.timeline_object = {}

        def stack_add_timelime_media(stop_once=None, add_type=None, media_id=None, split_media_id=None):
            stop_once = self.data.operation["undo"].add_stack(stop_once=stop_once, media_id=media_id, split_media_id=split_media_id, classification="timelime_media", add_type=add_type, func=undo_run_obj)
            if stop_once:
                return stop_once

        def stack_add_timelime_keyframe(stop_once=None, add_type=None, media_id=None, split_media_id=None):
            stop_once = self.data.operation["undo"].add_stack(stop_once=stop_once, media_id=media_id, split_media_id=split_media_id, classification="timelime_keyframe", add_type=add_type, func=undo_run_frame)
            if stop_once:
                return stop_once

        #stack_add_timelime_media(add_type="lord", media_id=None)
        self.data.operation["undo"].add_stack(classification="timelime_media", add_type="lord", func=undo_lord)

        #old_data = [None, 0]
        #stack_add_timelime_media("lord", old_data)

        #self.data.add_window_event("Command-Key-z", undo_stack)

        self.data.new_canvas("timeline")
        self.data.edit_canvas_size("timeline", x=1000, y=1000)
        self.data.edit_canvas_position("timeline", x=0, y=0)
        self.data.window_title_set("タイムライン")

        # ##print(button.canvas_data.territory["main"].diagram)

        shape = []

        timeline_left = 50  # タイムラインの左側のshape(x)
        timeline_up = 50  # タイムラインの上側のshape(y)
        timeline_size = 20  # タイムラインの幅(y)

        left_up_color = "#ffffff"

        shape.append(None)
        shape[0] = self.data.new_parts("timeline", "s0", parts_name="shape")  # 左側のやつ
        shape[0].edit_territory_size(x=timeline_left)
        shape[0].edit_diagram_color("0", left_up_color)

        shape.append(None)
        shape[1] = self.data.new_parts("timeline", "s1", parts_name="shape")  # 上側のやつ
        shape[1].edit_territory_size(y=timeline_up)
        shape[1].edit_territory_position(x=timeline_left)
        shape[1].edit_diagram_color("0", left_up_color)

        self.data.timeline_object = {}

        timeline_scroll = self.data.new_parts("timeline", "srob", parts_name="scroll_x")
        timeline_scroll.set_lr_edit(True)
        timeline_scroll.pxf.init_set_sta_end_f(sta=0, end=100)

        scroll_size = 20
        timeline_scroll.edit_territory_size(y=scroll_size)
        timeline_scroll.edit_territory_position(x=timeline_left, y=timeline_up - scroll_size)
        timeline_scroll.territory_draw()

        nowtime_bar = self.data.new_parts("timeline", "nowtime_bar", parts_name="timeline_nowtime")
        nowtime_bar.pxf.init_set_sta_end_f(sta=0, end=100)
        nowtime_bar.edit_territory_size(y=10)
        nowtime_bar.edit_territory_position(x=timeline_left, y=timeline_up)
        nowtime_bar.territory_draw()

        # print(self.data.all_data.now_time)

        def now_time_edit(scroll_data):
            self.data.all_data.now_time_update(scroll_data)

        nowtime_bar.callback_operation.set_event("mov", now_time_edit)

        # now_layer = 0

        def timeline_nowtime_approval_True(_):
            nowtime_bar.click_flag = True
            print("許可")

        def timeline_nowtime_approval_False(_):
            nowtime_bar.click_flag = False
            print("停止")

        timeline_scroll.callback_operation.set_event("sta", timeline_nowtime_approval_False)
        timeline_scroll.callback_operation.set_event("end", timeline_nowtime_approval_True)

        # self.data.all_data.callback_operation.set_event("del_layer_elements", del_layer_elements)

        def media_object_separate(send):
            media_id, click_f_pos = send
            scroll_data = self.data.timeline_object[media_id].pxf.get_event_data()
            if not scroll_data.ratio_f[0] < click_f_pos < scroll_data.ratio_f[0] + scroll_data.ratio_f[1]:
                print("返送")
                return

            self.data.timeline_object[media_id].mov_lock = True
            old_data = self.data.all_data.media_object_had_layer(media_id)

            a_size = click_f_pos - scroll_data.ratio_f[0]

            copy_obj, layer_id = self.data.all_data.copy_object_elements(media_id, sta=click_f_pos, end=scroll_data.ratio_f[1])
            layer_number = self.data.all_data.layer_id_to_layer_number(layer_id)
            make_object(copy_obj.obj_id, sta=click_f_pos, end=scroll_data.ratio_f[0] + scroll_data.ratio_f[1], layer_number=layer_number)

            self.data.timeline_object[copy_obj.obj_id].mov_lock = True

            items = copy.deepcopy(self.data.timeline_object[media_id].pxf.sub_point_f).items()

            for k, v in items:
                print(k, v)
                if click_f_pos > v:  # 左側
                    print("左側")
                if click_f_pos < v:  # 右側
                    print("右側")
                    # self.data.timeline_object[media_id].pxf.sub_point_f[k]

                    frame = copy.deepcopy(self.data.timeline_object[media_id].pxf.sub_point_f[k])
                    #self.data.timeline_object[copy_obj.obj_id].pxf.sub_point_f[k] = copy.deepcopy(self.data.timeline_object[media_id].pxf.sub_point_f[k])
                    self.data.timeline_object[media_id].callback_operation.event("tihs_del_{0}".format(k))
                    self.data.timeline_object[copy_obj.obj_id].make_KeyFrame(uu_id=k, pos_f=frame)

                if v == click_f_pos:  # ちょうど一緒
                    print("等")
                    self.data.timeline_object[media_id].callback_operation.event("tihs_del_{0}".format(k))

            self.data.timeline_object[media_id].pxf.set_f_ratio(size=a_size)
            self.data.timeline_object[media_id].mov_lock = False
            self.data.timeline_object[copy_obj.obj_id].mov_lock = False

            #old_data_split = self.data.all_data.media_object_had_layer(copy_obj.obj_id)
            #stack_add("split", old_data, old_data_split=old_data_split)
            stack_add_timelime_media(add_type="split", media_id=media_id, split_media_id=copy_obj.obj_id)

        def reflect_timeline_to_movie(scroll_data):
            media_id = scroll_data.option_data["media_id"]
            self.data.all_data.edit_object_installation(media_id, sta=scroll_data.ratio_f[0], end=scroll_data.ratio_f[0] + scroll_data.ratio_f[1])
            #get_media_data = self.data.all_data.media_object(media_id)
            #get_media_data.installation = [scroll_data.ratio_f[0], scroll_data.ratio_f[0] + scroll_data.ratio_f[1]]
            #self.data.all_data.media_object(media_id, data=get_media_data)

            # これを生成時に実行しないとダメ__?

        def new_layer():
            new_layer = self.data.all_data.add_layer_elements()
            make_layer()
            # #print(new_layer.layer_id)

        def make_layer():
            pass

        def new_obj():
            new_object = self.data.all_data.add_object_elements()
            make_object(new_object.obj_id)

            #old_data = self.data.all_data.media_object_had_layer(new_object.obj_id)
            #stack_add("add", old_data)
            stack_add_timelime_media(add_type="add", media_id=new_object.obj_id)
            #stack_add_timelime_keyframe(add_type="lord", media_id=new_object.obj_id)

        def layer_updown(mouse_pos):  # この関数重たそうだから要調整かな
            sta, end,  obj_id, edit_layer = mouse_pos
            now_layer = self.data.all_data.get_now_layer_number(obj_id)

            layer_num = len(self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.layer_layer_id)

            new_layer = end // timeline_size

            if new_layer > layer_num - 1:
                new_layer = layer_num - 1

            if new_layer < 0:
                new_layer = 0

            print("new_layer", new_layer)

            new_layer_id = self.data.all_data.layer_number_to_layer_id(new_layer)
            self.data.all_data.layer_id_set(obj_id, new_layer_id)
            #self.data.all_data.edit_data.scenes[self.data.all_data.edit_data.now_scene].layer_group.object_group[obj_id][1] = new_layer_id
            edit_layer(new_layer)

        def del_object_ui(media_id):
            print("削除対象物:", media_id)
            self.data.timeline_object[media_id].del_territory()
            # del self.data.timeline_object[media_id].callback_operation
            del self.data.timeline_object[media_id]
            self.data.all_data.del_object_elements(media_id)
            self.data.all_data.callback_operation.event("element_del")

        def all_del_object_ui():
            for media_id in self.data.timeline_object.keys():
                self.data.timeline_object[media_id].del_territory()
                self.data.all_data.del_object_elements(media_id)
                # print("削除 {0}".format(media_id))

            self.data.timeline_object = {}
            self.data.all_data.callback_operation.event("element_del")
            # print(self.data.timeline_object)

        # def media_objct_click():

        """
        def parameter(media_id):
            obj = self.data.all_data.media_object(media_id)
            elements = obj.effect_group
            # self.data.all_data.callback_operation.event("media_lord", info=())

            send = (elements, self.data.all_data.now_time)
            func = self.data.all_data.callback_operation.get_event("media_lord")[0]
            thread = threading.Thread(target=func, args=(send,))
            thread.start()
        """

        def make_object(media_id, sta=0, end=20, layer_number=0):
            option_data = {"media_id": media_id}

            print(len(self.data.timeline_object))

            new_obj = self.data.new_parts("timeline", media_id, parts_name="timeline_object", option_data=option_data)

            new_obj.timeline_nowtime_approval_False = timeline_nowtime_approval_False  # 定義
            new_obj.timeline_nowtime_approval_True = timeline_nowtime_approval_True  # 定義
            new_obj.stack_add_timelime_media = stack_add_timelime_media
            new_obj.stack_add_timelime_keyframe = stack_add_timelime_keyframe

            new_obj.set_right_click_pop()

            new_obj.edit_territory_position(x=timeline_left, y=timeline_up)
            new_obj.edit_diagram_size("bar", y=timeline_size)
            new_obj.callback_operation.set_event("mov", reflect_timeline_to_movie)  # コールバック関数登録
            new_obj.callback_operation.set_event("updown", layer_updown)
            new_obj.callback_operation.set_event("del", del_object_ui)
            new_obj.callback_operation.set_event("separate", media_object_separate)
            new_obj.callback_operation.set_event("sta", timeline_nowtime_approval_False)
            new_obj.callback_operation.set_event("end", timeline_nowtime_approval_True)
            new_obj.edit_layer(layer_number)

            frame_len = self.data.all_data.scene().editor["len"]

            new_obj.pxf.init_set_sta_end_f(sta=0, end=frame_len)
            new_obj.pxf.set_sta_end_f(sta=self.scrollbar_sta_end[0], end=self.scrollbar_sta_end[1])
            new_obj.pxf.set_f_ratio(position=sta, size=end - sta)

            new_obj.callback_operation.event("mov", info=new_obj.pxf.get_event_data())

            self.data.timeline_object[media_id] = new_obj

            # del new_obj
            window_size_edit(None)

        def loading_movie_data(new=None):
            self.data.operation["undo"].all_del_stack()

            for media_ui in self.data.timeline_object.values():
                media_ui.del_territory()

            self.data.timeline_object = {}

            if not new is None:
                self.data.all_data.change_now_scene(new)
            # ここで現在シーンが変わる

            get_scene = self.data.all_data.scene()
            frame_len = get_scene.editor["len"]

            obj_list = [get_scene.layer_group.object_group.keys(), get_scene.layer_group.object_group.values()]
            timeline_scroll.callback_operation.event("mov", info=timeline_scroll.pxf.get_event_data())

            nowtime = self.data.all_data.now_time_update()

            nowtime_bar.pxf.init_set_sta_end_f(sta=0, end=frame_len)
            nowtime_bar.frame_set(nowtime)

            for obj_k, obj_v in zip(obj_list[0], obj_list[1]):
                print(obj_k, "実行")
                sta_f = obj_v[0].installation[0]  # 開始地点解釈
                end_f = obj_v[0].installation[1]  # 終了地点解釈
                layer_number = get_scene.layer_group.layer_layer_id[obj_v[1]]  # 所属レイヤー解釈
                make_object(media_id=obj_k, sta=sta_f, end=end_f, layer_number=layer_number)

                for point_key, point_val in zip(obj_v[0].effect_point_internal_id_time.keys(), obj_v[0].effect_point_internal_id_time.values()):
                    self.data.all_data.add_key_frame(point_val, obj_k, point_key)

                    if point_key in ["default_sta", "default_end"]:
                        continue

                    self.data.timeline_object[obj_k].make_KeyFrame(uu_id=point_key, pos_f=point_val)

        def edit_data_reset():
            all_del_object_ui()
            self.data.all_data.new_edit_data()
            loading_movie_data()

        self.data.all_data.callback_operation.set_event("reset", edit_data_reset)
        self.data.all_data.callback_operation.set_event("file_input_before", all_del_object_ui)
        self.data.all_data.callback_operation.set_event("file_input_after", loading_movie_data)

        # new_object(s)

        # def sta_end_f_

        def obj_long_edit(media_obj, view_frame_len, view_sta_f, view_end_f):
            media_obj.pxf.init_set_sta_end_f(sta=0, end=view_frame_len)
            media_obj.pxf.set_sta_end_f(sta=view_sta_f, end=view_end_f)
            media_obj.pxf.set_f_ratio()

        def timeline_view_range(scroll_data):
            view_frame_len = self.data.all_data.scene().editor["len"]

            #sta_end_long = scroll_data.sta_end_f[1] - scroll_data.sta_end_f[0]

            view_sta_f = view_frame_len * (scroll_data.ratio_f[0] / 100)
            view_end_f = view_frame_len * ((scroll_data.ratio_f[0] + scroll_data.ratio_f[1]) / 100)

            self.scrollbar_sta_end = [view_sta_f, view_end_f]

            nowtime_bar.pxf.init_set_sta_end_f(sta=0, end=view_frame_len)
            nowtime_bar.pxf.set_sta_end_f(sta=view_sta_f, end=view_end_f)
            nowtime_bar.pxf.set_f_ratio()
            [obj_long_edit(media_obj, view_frame_len, view_sta_f, view_end_f) for media_obj in self.data.timeline_object.values()]

            # with self.data.all_data.ThreadPoolExecutor() as executor:
            #    [executor.submit(obj_long_edit(media_obj, frame_len, sta_f, end_f)) for media_obj in self.data.timeline_object.values()]

        timeline_scroll.callback_operation.set_event("mov", timeline_view_range)  # コールバック関数登録
        timeline_scroll.callback_operation.event("mov", info=timeline_scroll.pxf.get_event_data())

        def window_size_edit(event):
            size_x, size_y = self.data.get_window_size()
            self.data.edit_canvas_size("timeline",  x=size_x, y=size_y)

            timeline_width = size_x - timeline_left
            timeline_hight = size_y - timeline_up

            shape[0].edit_territory_size(y=size_y)
            shape[1].edit_territory_size(x=timeline_width)

            nowtime_bar.pxf.set_sta_end_px(sta=timeline_left, end=size_x, space=0)
            nowtime_bar.edit_territory_size(x=timeline_width, y=timeline_hight)
            nowtime_bar.edit_diagram_size("now", y=timeline_hight)
            nowtime_bar.pxf.set_f_ratio()

            # #print("ウィンドウサイズ", size_x, size_y)

            # length = self.data.all_data.scene().editer["len"]
            timeline_scroll.edit_territory_size(x=timeline_width)
            timeline_scroll.pxf.set_sta_end_px(sta=timeline_left, end=size_x, space=0)
            timeline_scroll.pxf.set_f_ratio()

            for i in self.data.timeline_object.values():
                i.edit_territory_size(x=timeline_width, y=timeline_hight)
                i.pxf.set_sta_end_px(sta=timeline_left, end=size_x)
                i.pxf.set_f_ratio()

            # timeline_scroll.pxf.set_scroll_minimum_value_px(self.data.timeline_object[-1].pxf.f_px_func(1))

            shape[0].territory_draw()
            shape[1].territory_draw()

        self.data.add_window_event("Configure", window_size_edit)
        window_size_edit(None)

        """
        scene_now_view = self.data.new_parts("timeline", "scene_now_view", parts_name="textbox") 
        scene_now_view.edit_territory_position(x=0, y=0)
        scene_now_view.edit_territory_size(x=20, y=10)
        scene_now_view.territory_draw()
        """

        def now_time_flag_edit():
            nowtime_bar.scene_change_flag = False

        def scene_change(option_data):
            timeline_nowtime_approval_False(None)

            self.popup = self.data.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.data.window, popup=True)

            scene_name_list = self.data.all_data.get_scene_name_list()

            pop_list = []

            for k in scene_name_list:
                scene_get = SceneGet(k, loading_movie_data, now_time_flag_edit)

                scene_name_func = ("　　 : " + k, scene_get.change) if k != self.data.all_data.edit_data.now_scene else ("現在 : " + k, scene_get.change)
                pop_list.append(scene_name_func)

            print(scene_name_list, pop_list)

            self.popup.set(pop_list)

            background_mouse, _, _, xy = self.data.get_window_contact()
            mouse = [0, 0]
            for i in range(2):
                mouse[i] = background_mouse[i] + xy[i]

            self.popup.show(mouse[0], mouse[1])

            timeline_nowtime_approval_True(None)

        scene_list_button = self.data.new_parts("timeline", "scene_list_button", parts_name="button")  # 左側のやつ
        scene_list_button.edit_territory_size(x=100, y=timeline_up - scroll_size - 10)
        scene_list_button.edit_territory_position(x=timeline_left, y=5)
        scene_list_button.edit_diagram_color("background", "#229922")
        scene_list_button.edit_diagram_color("text", "#ffffff")
        scene_list_button.diagram_stack("text", True)
        scene_list_button.edit_diagram_text("text", text="シーン選択")
        scene_list_button.territory_draw()
        scene_list_button.callback_operation.set_event("button", scene_change)

        def add_scene():
            self.data.all_data.add_scene_elements()

        new_layer()

        self.timeline_menubar = self.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.data.window)
        main_menubar_list = [("ファイル", "終了", self.data.window_exit), ("新規", "シーン", add_scene, "レイヤー", new_layer), ("追加", "動画", new_obj)]
        self.timeline_menubar.set(main_menubar_list)
        self.data.window_title_set("タイムライン")
        self.data.window_size_set(x=1200, y=700)

        return self.data


class CentralRole:
    pass


class SceneGet:
    def __init__(self, scene_id, loading_movie_data, now_time_flag_edit):
        self.scene_id = copy.deepcopy(scene_id)
        self.loading_movie_data = loading_movie_data
        now_time_flag_edit()
        #self.change_now_scene = change_now_scene_func
        #self.scene_now_view = scene_now_view

    def change(self):
        self.loading_movie_data(new=self.scene_id)

        #self.scene_now_view.edit_diagram_text("textbox1", text=self.scene_id)
        # self.scene_now_view.territory_draw()
