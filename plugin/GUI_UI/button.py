# coding:utf-8
import sys
import os
import copy


class parts:
    def __init__(self, data):
        self.data = data

    def UI_set(self, text="text", position=[0, 0], size=[0, 0]):

        def click(event):
            print("test")

        self.base_canvas = self.data.new_canvas(width_size=size[0], height_size=size[1])
        self.base_canvas.place(x=position[0], y=position[1])

        self.base_canvas.bind('<Button-1>', click)
        self.base_canvas.create_rectangle(0, 0, size[0], size[1], fill='green', outline="")  # 塗りつぶし

        canvas_center = [s / 2 for s in size]
        self.base_canvas.create_text(canvas_center[0], canvas_center[1], text=text)

        print("追加")
