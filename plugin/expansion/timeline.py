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

        button = self.data.new_parts("timeline", "buttonpppp", parts_name="button")
        button.edit_territory_position(x=200, y=200)
        button.territory_draw()

        # print(button.canvas_data.territory["main"].diagram)
        scroll = self.data.new_parts("timeline", "scrollpppp", parts_name="scroll_x")

        def scroll_edit(self):
            a = random.random()
            scroll.edit_percent_percentage(size=a)
        # print(button.canvas_data.territory["main"].diagram)

        button.add_diagram_event("0", "Button-1", scroll_edit)

        return self.data


class CentralRole:
    pass
