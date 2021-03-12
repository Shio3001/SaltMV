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
        timeline_size = 30  # タイムラインの幅(y)

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

        self.data.timeline_objct = []

        timeline_scroll = self.data.new_parts("timeline", "srob", parts_name="scroll_x")
        timeline_scroll.set_lr_edit(True)

        scroll_size = 20
        timeline_scroll.edit_territory_size(y=scroll_size)
        timeline_scroll.edit_territory_position(x=timeline_left, y=timeline_up - scroll_size)
        timeline_scroll.territory_draw()

        def new_objct(p=0):
            self.data.timeline_objct.append(None)
            self.data.timeline_objct[-1] = self.data.new_parts("timeline", "t_{0}".format(len(self.data.timeline_objct)), parts_name="timeline_objct")
            #self.data.timeline_objct[-1].pxf.edit_timeline_range(sta_px=0, end_px=100, sta_f=5, end_f=100)
            self.data.timeline_objct[-1].pxf.edit_objct_frame(position=p, size=10)
            self.data.timeline_objct[-1].territory_stack(False)
            # self.data.timeline_objct[-1].territory_draw()

        for i in range(2):
            new_objct()

        def timeline_view_range(scroll_data):
            frame_len = self.data.all_data.scene().editor["len"]
            sta_f = frame_len * (scroll_data[0] / 100)
            end_f = frame_len * ((scroll_data[0] + scroll_data[1]) / 100)

            #timeline_scroll.set_pxf_slope(sta_px=timeline_left, end_px=size_x, space=20)
            timeline_scroll.pxf.edit_objct_frame()

            for i in self.data.timeline_objct:
                i.set_pxf_slope(sta_f=sta_f, end_f=end_f)
                i.pxf.edit_objct_frame()
                # #print(i.edit_diagram_size("bar"))

        timeline_scroll.set_scroll_event(timeline_view_range)

        def window_size_edit(event):
            size_x, size_y = self.data.get_window_size()
            self.data.edit_canvas_size("timeline",  x=size_x, y=size_y)

            timeline_width = size_x - timeline_left

            shape[0].edit_territory_size(y=size_y)
            shape[1].edit_territory_size(x=timeline_width)

            ##print("ウィンドウサイズ", size_x, size_y)

            #length = self.data.all_data.scene().editer["len"]
            timeline_scroll.edit_territory_size(x=timeline_width)
            timeline_scroll.set_pxf_slope(sta_px=timeline_left, end_px=size_x, space=20)
            timeline_scroll.pxf.edit_objct_frame()

            for i in self.data.timeline_objct:
                i.set_pxf_slope(sta_px=timeline_left, end_px=size_x)
                i.pxf.edit_objct_frame()

            # timeline_scroll.pxf.set_scroll_minimum_value_px(self.data.timeline_objct[-1].pxf.f_px_func(1))

            shape[0].territory_draw()
            shape[1].territory_draw()

            # new_objct()

        self.data.add_window_event("Configure", window_size_edit)
        window_size_edit(None)

        return self.data


class CentralRole:
    pass
