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

        # print(button.canvas_data.territory["main"].diagram)

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

        def new_objct():
            self.data.timeline_objct.append(None)
            self.data.timeline_objct[-1] = self.data.new_parts("timeline", "t_{0}".format(len(self.data.timeline_objct)), parts_name="timeline_objct")

        # def edit_view_range
            # timeline_objct[-1].edit_timeline_range

        new_objct()

        # def timeline_range_edit(sta, end):
        #    pass

        def window_size_edit(event):
            size_x, size_y = self.data.get_window_size()
            self.data.edit_canvas_size("timeline",  x=size_x, y=size_y)

            shape[0].edit_territory_size(y=size_y)
            shape[1].edit_territory_size(x=size_x - timeline_left)

            print("ウィンドウサイズ", size_x, size_y)

            #length = self.data.all_data.scene().editer["len"]

            l = timeline_left
            r = size_x

            #l = (size_x - timeline_left) / length
            #r = size_x / length

            for i in self.data.timeline_objct:
                print(l, r)
                i.edit_timeline_range(sta_px=l, end_px=r, sta_f=50, end_f=150)

                print(i.px_f_func(100))

            shape[0].territory_draw()
            shape[1].territory_draw()

            # new_objct()

        self.data.add_window_event("Configure", window_size_edit)
        window_size_edit(None)

        return self.data


class CentralRole:
    pass
