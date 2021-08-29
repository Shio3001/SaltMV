# coding:utf-8
import sys
import os
import copy

#import cv2
#from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        #self.all_elements = self.data.all_elements
        #self.elements = self.data.elements
        self.tk = self.data.tk

        self.UI_parts = self.data.UI_parts  # パーツひとつひとつのデータ

        self.preview_image_tk = None
        self.now_name = None
        # self.UI_operation = self.data.UI_operation  # パーツを整形するためのデータ

    def main(self):
        self.data.new_canvas("text_input")
        self.data.edit_canvas_size("text_input", x=200, y=50)
        self.data.edit_canvas_position("text_input", x=0, y=0)

        textbox = self.data.new_parts("text_input", "text_input_textbox", parts_name="textbox")  # 左側のやつ
        textbox.edit_diagram_position("textbox", x=0, y=0)
        textbox.edit_diagram_size("textbox", x=200, y=30)
        textbox.territory_draw()

        self.data.window_size_set(x=200, y=50, lock_x=False, lock_y=False)

        close_save = self.data.new_parts("text_input", "close_save", parts_name="button")  # 左側のやつ
        close_non_save = self.data.new_parts("text_input", "close_non_save", parts_name="button")  # 左側のやつ

        green = "#229922"
        red = "#992222"

        def set_init_val(init_val):
            textbox.edit_diagram_text("textbox", text=init_val)

        def text_input_request(name):

            self.now_name = copy.deepcopy(name)
            self.data.window_open_close(True)

            close_save.edit_diagram_color("background", green)
            close_non_save.edit_diagram_color("background", red)

            self.data.window_title_set(str(name))

        def text_input_save_end(event):
            close_save.edit_diagram_color("background", "#111111")
            close_non_save.edit_diagram_color("background", "#111111")
            input_text = textbox.get_textbox_text("textbox")
            self.data.all_data.callback_operation.event("text_input_end", info=(self.now_name, input_text))
            self.data.window_open_close(False)

        def text_input_non_save_end(event):
            self.data.window_open_close(False)

        self.data.all_data.callback_operation.set_event("set_init_val", set_init_val)
        self.data.all_data.callback_operation.set_event("text_input_request", text_input_request, duplicate=False)

        close_save.edit_territory_size(x=100, y=20)
        close_save.edit_territory_position(x=0, y=30)
        close_save.edit_diagram_color("background", green)
        close_save.edit_diagram_color("text", "#ffffff")
        close_save.diagram_stack("text", True)
        close_save.edit_diagram_text("text", text="決定")
        close_save.territory_draw()
        close_save.callback_operation.set_event("button", text_input_save_end)

        close_non_save.edit_territory_size(x=100, y=20)
        close_non_save.edit_territory_position(x=100, y=30)
        close_non_save.edit_diagram_color("background", red)
        close_non_save.edit_diagram_color("text", "#ffffff")
        close_non_save.diagram_stack("text", True)
        close_non_save.edit_diagram_text("text", text="戻る")
        close_non_save.territory_draw()
        close_non_save.callback_operation.set_event("button", text_input_non_save_end)

        self.data.window_open_close(False)
