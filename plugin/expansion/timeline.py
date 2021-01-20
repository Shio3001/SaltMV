# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.timeline = data

    def main(self):

        def exit():
            self.timeline.window.destroy()

        timeline_menubar_list = [
            ("ウインドウ", [("閉じる", exit)])
        ]

        display_size = self.timeline.display_size_get()
        self.timeline.window_title_set("タイムライン")
        size = [1000, 400]
        self.timeline.window_size_set(size)
        self.timeline.menubar_set(timeline_menubar_list)
        print(display_size)

        timeline_height = 20

        test_var = self.timeline.new_parts(parts_name="timeline_var")
        test_var.edit_timeline_height(timeline_height)

        test_frame = []

        for i in range(20):
            test_frame.append(None)
            test_frame[i] = self.timeline.new_parts(parts_name="timeline_frame")
            test_frame[i].edit_canvas_position(height_position=i * timeline_height)
            # test_frame[i].edit_canvas_size(height_size=5)

        return self.timeline


class CentralRole:
    pass
