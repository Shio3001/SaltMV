# coding:utf-8
import sys
import os
import copy


class parts:
    def __init__(self, data):
        self.data = data

    def UI_set(self, text, position, size):
        self.base_canvas = self.data.tk.Canvas(self.data.window, width=size[0], height=size[1])  # Canvasの作成
        self.base_canvas.place(x=position[0], y=position[1])
        self.base_canvas.create_text(size[0]/2, size[1]/2, text=text)
        self.base_canvas.canvas.bind('<Button-1>', click)

        def click(event):
            print("test")
