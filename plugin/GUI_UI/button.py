# coding:utf-8
import sys
import os
import copy


class parts:
    def __init__(self, data):
        self.data = data

    def UI_set(self, text=None, position=[None, None], size=[None, None], user_event=None, processing=None):

        self.data.edit_canvas_text(text=text)
        self.data.edit_canvas_position(width_position=position[0], height_position=position[1])
        self.data.edit_canvas_size(width_size=size[0], height_size=size[1])
        self.data.edit_canvas_color(color="#adff2f")
        self.data.canvas_for_button(processing=processing, user_event=user_event)
        self.data.canvas_update()

        print("追加")

        return self.data
