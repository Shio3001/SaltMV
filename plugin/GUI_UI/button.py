# coding:utf-8
import sys
import os
import copy


class parts:
    def __init__(self, data):
        self.data = data

    def UI_set(self, text="text", position=[0, 0], size=[0, 0], user_event="Button-1", processing=None):

        # self.data.canvas

        self.data.new_canvas(width_size=size[0], height_size=size[1], width_position=position[0], height_position=position[1])
        self.data.full_canvas(color="#adff2f")
        self.data.text_canvas(text=text)

        #event = "Return"
        self.data.for_Button_canvas(processing, user_event)

        print("追加")
