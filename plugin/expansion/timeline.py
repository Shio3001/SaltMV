# coding:utf-8
import sys
import os
import copy

import random


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation

    def main(self):
        self.data.new_canvas("timeline")
        self.data.edit_canvas_size("timeline", x=1000, y=1000)
        self.data.edit_canvas_position("timeline", x=100, y=100)
        self.data.window_title_set("タイムライン")

        # print(button.canvas_data.territory["main"].diagram)

        button = self.data.new_parts("timeline", "buttonpppp", parts_name="button")
        button.edit_territory_position(x=200, y=200)
        button.territory_draw()

        #print(scroll.canvas_data.territory["i"].diagram["view"].position, "a")

        textbox = self.data.new_parts("timeline", "tepppop", parts_name="textbox")
        scroll = self.data.new_parts("timeline", "i", parts_name="scroll_x")

        def scroll_edit(self):
            a = random.random()
            scroll.edit_percent_percentage(size=a)

            button.edit_diagram_text("text", text=str(round(a*100)), font_size=20)
            button.diagram_draw("text")
        #
        # print(button.canvas_data.territory["main"].diagram)

        button.add_territory_event("Button-1", scroll_edit)

        return self.data


class CentralRole:
    pass
