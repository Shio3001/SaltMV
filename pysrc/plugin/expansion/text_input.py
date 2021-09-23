# coding:utf-8
import sys
import os
import copy

#import cv2
#from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont


class InitialValue:
    def __init__(self, data):
        self.window_control = data
        self.operation = self.window_control.operation
        #self.all_elements = self.window_control.all_elements
        #self.elements = self.window_control.elements
        self.tk = self.window_control.tk

        self.UI_parts = self.window_control.UI_parts  # パーツひとつひとつのデータ

        self.preview_image_tk = None
        self.now_name = None
        # self.UI_operation = self.window_control.UI_operation  # パーツを整形するためのデータ

    def main(self):
        self.window_control.new_canvas("text_input")
        self.window_control.edit_canvas_size("text_input", x=200, y=50)
        self.window_control.edit_canvas_position("text_input", x=0, y=0)

        textbox = self.window_control.new_parts("text_input", "text_input_textbox", parts_name="textbox")  # 左側のやつ
        textbox.edit_diagram_position("textbox", x=0, y=0)
        textbox.edit_diagram_size("textbox", x=200, y=30)
        textbox.territory_draw()

        self.window_control.window_size_set(x=200, y=50, lock_x=False, lock_y=False)

        close_save = self.window_control.new_parts("text_input", "close_save", parts_name="button")  # 左側のやつ
        close_non_save = self.window_control.new_parts("text_input", "close_non_save", parts_name="button")  # 左側のやつ

        green = "#229922"
        red = "#992222"
        gray = "#111111"

        def set_init_val(init_val):
            textbox.edit_diagram_text("textbox", text=init_val)

        def text_input_request(name):

            self.now_name = copy.deepcopy(name)
            self.window_control.window_open_close(True)

            close_save.edit_diagram_color("background", green)
            close_non_save.edit_diagram_color("background", red)

            self.window_control.window_title_set(str(name))

        def text_input_request_file_open(name):

            text_input_request(name)
            close_save.edit_diagram_color("background", gray)
            close_non_save.edit_diagram_color("background", gray)
            self.window_control.window.update()

            default = textbox.get_text("textbox")
            file_open_text = textbox.open_file_select(default)
            textbox.edit_diagram_text("textbox", text=file_open_text)

            close_save.edit_diagram_color("background", green)
            close_non_save.edit_diagram_color("background", red)

        def text_input_request_folder_open(name):
            text_input_request(name)
            close_save.edit_diagram_color("background", gray)
            close_non_save.edit_diagram_color("background", gray)
            self.window_control.window.update()

            default = textbox.get_text("textbox")
            folder_open_text = textbox.open_folder_select(default)
            textbox.edit_diagram_text("textbox", text=folder_open_text)

            close_save.edit_diagram_color("background", green)
            close_non_save.edit_diagram_color("background", red)

        def text_input_save_end(event):
            close_save.edit_diagram_color("background", gray)
            close_non_save.edit_diagram_color("background", gray)
            input_text = textbox.get_textbox_text("textbox")
            self.window_control.edit_control_auxiliary.callback_operation.event("text_input_end", info=(self.now_name, input_text))
            self.window_control.window_open_close(False)

        def text_input_non_save_end(event):
            self.window_control.window_open_close(False)

        self.window_control.edit_control_auxiliary.callback_operation.set_event("set_init_val", set_init_val)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("text_input_request", text_input_request, duplicate=False)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("text_input_request_file_open", text_input_request_file_open, duplicate=False)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("text_input_request_folder_open", text_input_request_folder_open, duplicate=False)

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

        self.window_control.window_open_close(False)
