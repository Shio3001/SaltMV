# coding:utf-8
import sys
import os
import copy
import tkinter as tk


class parts:
    def __init__(self, data):
        self.data = data

    def UI_set(self, text="text", position=[0, 0], size=[0, 0]):

        def click(event):
            print("test")

        self.base_canvas = self.data.tk.Canvas(self.data.window, width=size[0], height=size[1])  # Canvasの作成
        self.base_canvas.place(x=position[0], y=position[1])
        self.base_canvas.create_text(size[0], size[1], text=text)
        self.base_canvas.bind('<Button-1>', click)
