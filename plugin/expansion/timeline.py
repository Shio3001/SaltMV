# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation

    # def get_all_elements(self)

    def main(self):
        self.data.new_canvas("timeline")
        self.data.edit_canvas_size("timeline", x=100, y=100)
        self.data.window_title_set("タイムライン")

        shape = []
        shape.append(None)
        shape[0] = self.data.new_parts("timeline", parts_name="shape")

        print(self.data.canvas_data)

        return self.data


class CentralRole:
    pass
