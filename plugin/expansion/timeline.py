# coding:utf-8
import sys
import os
import copy

import random


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation

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

        self.data.timeline_objct = {}

        timeline_scroll = self.data.new_parts("timeline", "srob", parts_name="scroll_x")
        timeline_scroll.set_lr_edit(True)
        timeline_scroll.pxf.init_set_sta_end_f(sta=0, end=100)

        scroll_size = 20
        timeline_scroll.edit_territory_size(y=scroll_size)
        timeline_scroll.edit_territory_position(x=timeline_left, y=timeline_up - scroll_size)
        timeline_scroll.territory_draw()

        now_layer = 0

        def layer_elements(info):
            pass

        #self.data.all_data.callback_operation.set_event("del_layer_elements", del_layer_elements)

        # test_layer =

        # for i in range(10):
        #    test_layer_loop = self.data.all_data.add_layer_elements()

        #self.scrollbar_sta_end = [0, 0]

        def reflect_timeline_to_movie(scroll_data):

            media_id = scroll_data.option_data["media_id"]

            #print("id_s", test_layer.layer_id, scroll_data.option_data["media_id"])
            get_media_data = self.data.all_data.media_object(now_layer, media_id)

            get_media_data.installation = [scroll_data.ratio_f[0], scroll_data.ratio_f[0] + scroll_data.ratio_f[1]]
            self.data.all_data.media_object(now_layer, media_id, data=get_media_data)

            #print(self.data.all_data.media_object(layer_id, media_id).installation, "installation", scroll_data.ratio_f)
            # self.data.timeline_objct[-1].

        def new_layer():
            new_layer, leyer_number = self.data.all_data.add_layer_elements()
            make_layer(leyer_number)
            # print(new_layer.layer_id)

        def make_layer(leyer_number):
            pass

        def new_obj():
            new_object = self.data.all_data.add_object_elements(now_layer)
            make_objct(new_object.obj_id)

        def layer_updown(mouse_pos):
            pos, pos_set_y = mouse_pos
            now_layer = round(pos / timeline_size)
            now_layer = now_layer if now_layer > 0 else 0

            print("現在のレイヤー", now_layer)

            pos_set_y(now_layer)

        def make_objct(media_id):
            self.option_data = {"media_id": media_id}

            new_obj = self.data.new_parts("timeline", "t_{0}".format(len(self.data.timeline_objct)), parts_name="timeline_objct", option_data=self.option_data)

            self.data.timeline_objct[media_id] = new_obj
            self.data.timeline_objct[media_id].edit_territory_position(x=timeline_left, y=timeline_up)
            # self.data.timeline_objct[media_id].territory_stack(False)
            self.data.timeline_objct[media_id].callback_operation.set_event("mov", reflect_timeline_to_movie)  # コールバック関数登録
            self.data.timeline_objct[media_id].callback_operation.set_event("updown", layer_updown)

            frame_len = self.data.all_data.scene().editor["len"]

            print("frame_len", frame_len)
            #print("scrollbar_sta_end", self.scrollbar_sta_end)

            self.data.timeline_objct[media_id].pxf.init_set_sta_end_f(sta=0, end=frame_len)
            self.data.timeline_objct[media_id].pxf.set_sta_end_f(sta=self.scrollbar_sta_end[0], end=self.scrollbar_sta_end[1])

            obj_time = self.data.all_data.media_object(0, media_id)

            scroll_data = timeline_scroll.pxf.get_event_data()

            self.data.timeline_objct[media_id].pxf.set_f_ratio(position=0, size=20)

            window_size_edit(None)

        # for i in range(1):
        #    new_objct()

        def loading_movie_data():
            print("取得")
            get_scene = self.data.all_data.scene()

            frame_len = get_scene.editor["len"]

            print("layer個数", len(get_scene.layer_group))

            for layer in get_scene.layer_group.values():
                print("obj個数", len(layer.object_group), layer.object_group)
                for obj in layer.object_group.values():
                    print(obj, "実行")
                    make_objct(media_id=obj.objct_id)

            # new_objct(s)

        # def sta_end_f_

        def timeline_view_range(scroll_data):
            frame_len = self.data.all_data.scene().editor["len"]

            sta_end_long = scroll_data.sta_end_f[1] - scroll_data.sta_end_f[0]

            sta_f = frame_len * (scroll_data.ratio_f[0] / 100)
            end_f = frame_len * ((scroll_data.ratio_f[0] + scroll_data.ratio_f[1]) / 100)

            self.scrollbar_sta_end = [sta_f, end_f]

            #print(sta_f, end_f, "staend")

            for i in self.data.timeline_objct.values():
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

            # print("ウィンドウサイズ", size_x, size_y)

            # length = self.data.all_data.scene().editer["len"]
            timeline_scroll.edit_territory_size(x=timeline_width)
            timeline_scroll.pxf.set_sta_end_px(sta=timeline_left, end=size_x, space=0)
            timeline_scroll.pxf.set_f_ratio()

            for i in self.data.timeline_objct.values():
                i.edit_territory_size(x=timeline_width, y=timeline_hight)
                i.pxf.set_sta_end_px(sta=timeline_left, end=size_x)
                i.pxf.set_f_ratio()

            # timeline_scroll.pxf.set_scroll_minimum_value_px(self.data.timeline_objct[-1].pxf.f_px_func(1))

            shape[0].territory_draw()
            shape[1].territory_draw()

            # new_objct()

        self.data.add_window_event("Configure", window_size_edit)
        window_size_edit(None)

        self.data.all_data.fill_input_callback = loading_movie_data

        main_menubar_list = [("ファイル", "終了", self.data.window_exit), ("新規", "シーン", None, "レイヤー", new_layer), ("追加", "動画", new_obj)]
        self.data.menubar_set(main_menubar_list)
        self.data.window_title_set("タイムライン")
        return self.data


class CentralRole:
    pass
