# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.timeline = data

    def main(self):

        def test():
            print("a")

        timeline_menubar_list = [
            ("ウインドウ", [("閉じる", test)])
        ]

        display_size = self.timeline.display_size_get()
        self.timeline.window_title_set("タイムライン")
        size = [1000, 400]
        self.timeline.window_size_set(size)
        self.timeline.menubar_set(timeline_menubar_list)
        print(display_size)

        return self.timeline

        # timeline_window_size = tuple(map(int, (display[0] * 0.55, display[1] * 0.8)))
        # timeline_window = tk.Toplevel(main_window)
        # timeline_menubar_list = [("タイムライン", (["閉じる", self.exit]))]
        # timeline_window = data.GUI_operation.window_set(timeline_window, "タイムライン", timeline_window_size, timeline_menubar_list)


class CentralRole:
    pass
