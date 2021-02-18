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
        self.data.edit_canvas_size("timeline", x=300, y=300)
        self.data.edit_canvas_position("timeline", x=0, y=0)
        self.data.window_title_set("タイムライン")

        shape = []
        shape.append(None)
        shape[0] = self.data.new_parts("timeline", parts_name="shape")

        def test(event):
            print("test")

        def test2(event):
            print("test2")

        self.data.add_canvas_event("timeline", "Button-1", test)
        #self.data.add_canvas_event("timeline", "Button-2", test)
        #self.data.add_canvas_event("timeline", "Button-1", test2)
        print(self.data.get_canvas_event("timeline"))
        self.data.del_canvas_event("timeline", "Button-1", test)
        print(self.data.get_canvas_event("timeline"))
        # self.data.all_del_canvas_event("timeline")

        return self.data


class CentralRole:
    pass
