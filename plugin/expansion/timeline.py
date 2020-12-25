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

        return self.timeline


class CentralRole:
    pass
