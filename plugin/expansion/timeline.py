# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation

    def main(self):
        self.data.new_canvas("timeline")
        self.data.edit_canvas_size("timeline", x=1000, y=1000)
        self.data.edit_canvas_position("timeline", x=0, y=0)
        self.data.window_title_set("タイムライン")

        button = self.data.new_parts("timeline", parts_name="button")
        button.edit_territory_position("main", x=200, y=200)
        button.territory_draw("main")

        scroll = self.data.new_parts("timeline", parts_name="scroll_x")

        return self.data


class CentralRole:
    pass
