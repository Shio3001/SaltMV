# coding:utf-8
import sys
import os
import copy

import random
import math
import threading


class InitialValue:
    def __init__(self, data):  # data ←継承元(ファイルが違う＋プラグイン形式なのでこのような形に)
        self.data = data
        self.operation = self.data.operation
        self.data.all_data.now_time = 0

    def main(self):

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

        def now_time_update(scroll_data):
            self.data.all_data.now_time = scroll_data.ratio_f[0]

            # print(self.data.all_data.now_time)

        nowtime_bar.callback_operation.set_event("mov", now_time_update)

        #now_layer = 0

        def timeline_nowtime_approval_True(_):
            nowtime_bar.click_flag = True
            print("許可")

        def timeline_nowtime_approval_False(_):
            nowtime_bar.click_flag = False
            print("停止")

        timeline_scroll.callback_operation.set_event("sta", timeline_nowtime_approval_False)
        timeline_scroll.callback_operation.set_event("end", timeline_nowtime_approval_True)

        #self.data.all_data.callback_operation.set_event("del_layer_elements", del_layer_elements)

        def media_object_separate(media_id):
            scroll_data = self.data.timeline_object[media_id].pxf.get_event_data()

            if not scroll_data.ratio_f[0] < self.data.all_data.now_time < scroll_data.ratio_f[0] + scroll_data.ratio_f[1]:
                print("返送")
                return

            a_size = self.data.all_data.now_time - scroll_data.ratio_f[0]
            self.data.timeline_object[media_id].pxf.set_f_ratio(size=a_size)

            copy_obj, layer_id = self.data.all_data.copy_object_elements(media_id, sta=self.data.all_data.now_time, end=scroll_data.ratio_f[1])

            layer_number = self.data.all_data.layer_id_to_layer_number(layer_id)

            make_object(copy_obj.obj_id, sta=self.data.all_data.now_time, end=scroll_data.ratio_f[0] + scroll_data.ratio_f[1], layer_number=layer_number)

        # test_layer =

        # for i in range(10):
        #    test_layer_loop = self.data.all_data.add_layer_elements()

        #self.scrollbar_sta_end = [0, 0]

        def reflect_timeline_to_movie(scroll_data):

            media_id = scroll_data.option_data["media_id"]

            #print("id_s", test_layer.layer_id, scroll_data.option_data["media_id"])

            get_media_data = self.data.all_data.media_object(media_id)
            get_media_data.installation = [scroll_data.ratio_f[0], scroll_data.ratio_f[0] + scroll_data.ratio_f[1]]
            self.data.all_data.media_object(media_id, data=get_media_data)

            #print(self.data.all_data.media_object(layer_id, media_id).installation, "installation", scroll_data.ratio_f)
            # self.data.timeline_object[-1].

        def new_layer():
            new_layer = self.data.all_data.add_layer_elements()
            make_layer()
            # #print(new_layer.layer_id)

        def make_layer():
            pass

        def new_obj():
            new_object = self.data.all_data.add_object_elements()
            make_object(new_object.obj_id)

        def layer_updown(mouse_pos):
            pos, obj_id, edit_layer, click_start = mouse_pos
            now_layer = self.data.all_data.get_now_layer_number(obj_id)

            mov_layer = math.floor((abs(pos) - (timeline_size / 2)) / timeline_size)

            #print("pos", pos)

            new_layer = now_layer

            if pos < -1 * timeline_size:
                new_layer = now_layer - mov_layer

            if pos > timeline_size:
                new_layer = now_layer + mov_layer

            #print("現在のレイヤー", now_layer)

            if new_layer < 0:
                new_layer = 0

            if new_layer > self.data.all_data.get_layer_length() - 1:
                new_layer = self.data.all_data.get_layer_length() - 1

            new_layer_id = self.data.all_data.layer_number_to_layer_id(new_layer)
            layer = self.data.all_data.layer()
            layer.object_group[obj_id][1] = new_layer_id
            self.data.all_data.layer(data=layer)

            edit_layer(new_layer)
            # click_start(None)

        def del_object_ui(media_id):
            print("削除対象物:", media_id)
            self.data.timeline_object[media_id].del_territory()
            #del self.data.timeline_object[media_id].callback_operation
            del self.data.timeline_object[media_id]
            self.data.all_data.del_object_elements(media_id)
            self.data.all_data.callback_operation.event("element_del")

        def all_del_object_ui():
            for media_id in self.data.timeline_object.keys():
                self.data.timeline_object[media_id].del_territory()
                self.data.all_data.del_object_elements(media_id)
                #print("削除 {0}".format(media_id))

            self.data.timeline_object = {}
            self.data.all_data.callback_operation.event("element_del")
            # print(self.data.timeline_object)

        # def media_objct_click():

        """
        def parameter(media_id):
            obj = self.data.all_data.media_object(media_id)
            elements = obj.effect_group
            #self.data.all_data.callback_operation.event("media_lord", info=())

            send = (elements, self.data.all_data.now_time)
            func = self.data.all_data.callback_operation.get_event("media_lord")[0]
            thread = threading.Thread(target=func, args=(send,))
            thread.start()
        """

        def make_object(media_id, sta=0, end=20, layer_number=0):
            option_data = {"media_id": media_id}
            #print("new_id", option_data)

            print(len(self.data.timeline_object))

            new_obj = self.data.new_parts("timeline", media_id, parts_name="timeline_object", option_data=option_data)

            self.data.timeline_object[media_id] = new_obj
            del new_obj

            #print("生成オブジェクトID", media_id)

            self.data.timeline_object[media_id].edit_territory_position(x=timeline_left, y=timeline_up)
            self.data.timeline_object[media_id].edit_diagram_size("bar", y=timeline_size)
            # self.data.timeline_object[media_id].territory_stack(False)
            self.data.timeline_object[media_id].callback_operation.set_event("mov", reflect_timeline_to_movie)  # コールバック関数登録
            self.data.timeline_object[media_id].callback_operation.set_event("updown", layer_updown)
            self.data.timeline_object[media_id].callback_operation.set_event("del", del_object_ui)

            self.data.timeline_object[media_id].callback_operation.set_event("separate", media_object_separate)
            self.data.timeline_object[media_id].callback_operation.set_event("sta", timeline_nowtime_approval_False)
            self.data.timeline_object[media_id].callback_operation.set_event("end", timeline_nowtime_approval_True)
            #self.data.timeline_object[media_id].callback_operation.set_event("parameter_lord", parameter)

            # .del_diagram_event("bar", "Button-1", click_start)

            self.data.timeline_object[media_id].edit_layer(layer_number)

            # self.data.timeline_object[media_id].timeline_object_ID =

            frame_len = self.data.all_data.scene().editor["len"]

            #print("frame_len", frame_len)
            #print("scrollbar_sta_end", self.scrollbar_sta_end)

            self.data.timeline_object[media_id].pxf.init_set_sta_end_f(sta=0, end=frame_len)
            self.data.timeline_object[media_id].pxf.set_sta_end_f(sta=self.scrollbar_sta_end[0], end=self.scrollbar_sta_end[1])

            obj_time = self.data.all_data.media_object(media_id)

            scroll_data = timeline_scroll.pxf.get_event_data()

            self.data.timeline_object[media_id].pxf.set_f_ratio(position=sta, size=end - sta)

            # callback_operation.event("updown"

            window_size_edit(None)

        # for i in range(1):
        #    new_object()

        def loading_movie_data():
            # print("取得")
            get_scene = self.data.all_data.scene()
            frame_len = get_scene.editor["len"]

            timeline_scroll.pxf.init_set_sta_end_f(sta=0, end=frame_len)
            timeline_scroll.pxf.set_f_ratio()
            #print("layer個数", len(get_scene.layer_group))

            # print(get_scene.editor)
            # print(get_scene.layer_group)
            # print(get_scene.layer_group.object_group)

            obj_list = [get_scene.layer_group.object_group.keys(), get_scene.layer_group.object_group.values()]

            # print(obj_list)

            for obj_k, obj_v in zip(obj_list[0], obj_list[1]):
                #print(obj_k, "実行")
                sta_f = obj_v[0].installation[0]  # 開始地点解釈
                end_f = obj_v[0].installation[1]  # 終了地点解釈
                layer_number = get_scene.layer_group.layer_layer_id[obj_v[1]]  # 所属レイヤー解釈
                make_object(media_id=obj_k, sta=sta_f, end=end_f, layer_number=layer_number)

            # self.data.edit_menubar_bool("新規","シーン",False)

            # print("取得終了")

        def edit_data_reset():
            all_del_object_ui()
            self.data.all_data.new_edit_data()
            loading_movie_data()

        self.data.all_data.callback_operation.set_event("reset", edit_data_reset)
        self.data.all_data.callback_operation.set_event("file_input_before", all_del_object_ui)
        self.data.all_data.callback_operation.set_event("file_input_after", loading_movie_data)

        # new_object(s)

        # def sta_end_f_

        def timeline_view_range(scroll_data):
            frame_len = self.data.all_data.scene().editor["len"]

            sta_end_long = scroll_data.sta_end_f[1] - scroll_data.sta_end_f[0]

            sta_f = frame_len * (scroll_data.ratio_f[0] / 100)
            end_f = frame_len * ((scroll_data.ratio_f[0] + scroll_data.ratio_f[1]) / 100)

            self.scrollbar_sta_end = [sta_f, end_f]

            nowtime_bar.pxf.init_set_sta_end_f(sta=0, end=frame_len)
            nowtime_bar.pxf.set_sta_end_f(sta=sta_f, end=end_f)
            nowtime_bar.pxf.set_f_ratio()
            #print(sta_f, end_f, "staend")

            for i in self.data.timeline_object.values():
                i.pxf.init_set_sta_end_f(sta=0, end=frame_len)
                i.pxf.set_sta_end_f(sta=sta_f, end=end_f)
                i.pxf.set_f_ratio()

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

            # new_object()

        self.data.add_window_event("Configure", window_size_edit)
        window_size_edit(None)

        self.timeline_menubar = self.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.data.window)
        main_menubar_list = [("ファイル", "終了", self.data.window_exit), ("新規", "シーン", None, "レイヤー", new_layer), ("追加", "動画", new_obj)]
        self.timeline_menubar.set(main_menubar_list)
        self.data.window_title_set("タイムライン")
        return self.data


class CentralRole:
    pass
