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

        def window_size_edit(event):
            size_x, size_y = self.data.get_window_size()

            self.data.edit_canvas_size("timeline",  x=size_x, y=size_y)

            shape[0].edit_territory_size(y=size_y)
            shape[1].edit_territory_size(x=size_x - timeline_left)

            print(size_x, size_y)

            shape[0].territory_draw()
            shape[1].territory_draw()

        def get_mouse(event):

            mouse, _, _ = shape[0].get_diagram_contact("0")

            print(mouse)

        self.data.add_window_event("Configure", window_size_edit)
        self.data.add_window_event("Button-1", get_mouse)
        window_size_edit(None)

        #test_obj = self.data.new_parts("timeline", "t", parts_name="timeline_objct")

        return self.data


class CentralRole:
    pass
