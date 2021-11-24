# coding:utf-8
import sys
import os
import copy
import datetime
import inspect
import time
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import cv2


class InitialValue:
    def __init__(self, window_control):
        self.window_control = window_control
        self.operation = self.window_control.operation

        self.flag_re_instance = False

        self.salt_bezier_curveModule = self.operation["SaltBezierCurve"]
        self.salt_bezier_curveInstance = None

        self.window_width = 0
        self.window_height = 0
        self.view_height_size08 = 0
        self.view_height_size01 = 0

        self.close_save_green = "#229922"
        self.close_save_red = "#992222"
        self.close_save_gray = "#111111"

    def main(self):
        self.window_control.new_canvas("easing_beziercurve")
        self.window_control.edit_canvas_size("easing_beziercurve", x=500, y=500)
        self.window_control.edit_canvas_position("easing_beziercurve", x=0, y=0)
        self.window_control.window_title_set("イージング設定")

        self.window_width, self.window_height = self.window_control.get_window_size()

        self.easing_preview = self.window_control.new_parts("easing_beziercurve", "easing_preview", parts_name="pillow_view")
        self.easing_preview.size_update(self.window_width, self.window_height)

        self.salt_bezier_curveInstance = self.salt_bezier_curveModule.ForPyInterface(int(self.window_width), int(self.window_height))

        greenpoint = self.window_control.new_parts("easing_beziercurve", "greenpoint", parts_name="easing_point")  # 上側のやつ
        greenpoint.edit_territory_position(x=0, y=0)
        greenpoint.edit_diagram_color("point", "#11ff11")

        redpoint = self.window_control.new_parts("easing_beziercurve", "redpoint", parts_name="easing_point")  # 上側のやつ
        redpoint.edit_territory_position(x=0, y=0)
        redpoint.edit_diagram_color("point", "#ff1111")

        redpoint.edit_diagram_position("point", x=50, y=0)
        greenpoint.edit_diagram_position("point", x=100, y=0)

        self.end_to_sta_time = 0

        def get_permission_elapsed_time():
            bool_time = 0.2 <= time.time() - self.end_to_sta_time
            return bool_time

        def save_end(e=None):
            if self.flag_re_instance:
                return

            close_save.edit_diagram_color("background", self.close_save_gray)
            self.window_control.window.update()
            close_save.territory_draw()
            #input_text = textbox.get_textbox_text("textbox")
            #self.window_control.edit_control_auxiliary.callback_operation.event("text_input_end", info=(self.now_name, input_text))
            self.window_control.window_open_close(False)

        close_save = self.window_control.new_parts("easing_beziercurve", "close_save", parts_name="button")  # 左側のやつ
        close_save.edit_territory_size(x=100, y=20)
        close_save.edit_territory_position(x=0, y=0)
        close_save.edit_diagram_color("background", self.close_save_green)
        close_save.edit_diagram_color("text", "#ffffff")
        close_save.diagram_stack("text", True)
        close_save.edit_diagram_text("text", text="決定")
        close_save.territory_draw()
        close_save.callback_operation.set_event("button", save_end)

        textboxRX = self.window_control.new_parts("text_input", "text_input_textbox", parts_name="textbox")  # 左側のやつ
        textboxRX.edit_diagram_position("textbox", x=0, y=0)
        textboxRX.edit_diagram_size("textbox", x=200, y=30)
        textboxRX.territory_draw()
        textboxRY = self.window_control.new_parts("text_input", "text_input_textbox", parts_name="textbox")  # 左側のやつ
        textboxRY.edit_diagram_position("textbox", x=0, y=0)
        textboxRY.edit_diagram_size("textbox", x=200, y=30)
        textboxRY.territory_draw()
        textboxGX = self.window_control.new_parts("text_input", "text_input_textbox", parts_name="textbox")  # 左側のやつ
        textboxGX.edit_diagram_position("textbox", x=0, y=0)
        textboxGX.edit_diagram_size("textbox", x=200, y=30)
        textboxGX.territory_draw()
        textboxGY = self.window_control.new_parts("text_input", "text_input_textbox", parts_name="textbox")  # 左側のやつ
        textboxGY.edit_diagram_position("textbox", x=0, y=0)
        textboxGY.edit_diagram_size("textbox", x=200, y=30)
        textboxGY.territory_draw()

        # def window_size_edit_start(e=None):
        #     print("start", self.flag_re_instance)
        #     self.flag_re_instance = True

        def window_size_edit_mov(e=None):
            if not get_permission_elapsed_time():
                return

            self.flag_re_instance = True
            print("mov", self.flag_re_instance)

        def window_size_edit_end(e=None):
            if not self.flag_re_instance:
                return

            self.flag_re_instance = False

            self.window_width, self.window_height = self.window_control.get_window_size()
            self.view_height_size08 = int(self.window_height * 0.8)
            self.view_height_size01 = int(self.window_height * 0.1)

            close_save.edit_territory_position(x=0, y=self.view_height_size08)
            close_save.edit_territory_size(x=self.window_width, y=self.view_height_size01 * 2)
            close_save.territory_draw()

            self.salt_bezier_curveInstance = self.salt_bezier_curveModule.ForPyInterface(int(self.window_width), int(self.view_height_size08))

            print("再インスタンス化", self.window_width, self.window_height)

            print("end", self.flag_re_instance)

            self.salt_bezier_curveInstance.Setx1y1(0, 0)
            self.salt_bezier_curveInstance.Setx2y2(100, 100)
            view_easing()

            point_size = self.window_width * 0.025

            if point_size < 10:
                point_size = 10

            greenpoint.edit_diagram_size("point", point_size, point_size)
            redpoint.edit_diagram_size("point", point_size, point_size)

            greenpoint.territory_draw()
            redpoint.territory_draw()

            self.end_to_sta_time = time.time()

        def view_easing():

            image_numpy = cv2.cvtColor(self.salt_bezier_curveInstance.GetView().astype('uint8').reshape(self.view_height_size08, self.window_width, 1), cv2.COLOR_GRAY2RGB)

            self.window_control.edit_canvas_size("easing_beziercurve",  x=self.window_width, y=self.window_height)
            self.easing_preview.size_update(self.window_width, self.view_height_size08)

            print(image_numpy.shape)

            image_pil = Image.fromarray(image_numpy)
            self.easing_preview.view(ImageTk.PhotoImage(image_pil))

            redpoint.diagram_stack("point", True)
            greenpoint.diagram_stack("point", True)
            redpoint.territory_draw()
            greenpoint.territory_draw()

            print(self.window_width, self.window_height)

        def easing_mov():
            pass

        def easing_end(e=None):

            print("easing_end")

            self.salt_bezier_curveInstance = self.salt_bezier_curveModule.ForPyInterface(int(self.window_width), int(self.view_height_size08))

            green_x_rate = greenpoint.edit_diagram_position("point")[0] / self.window_width * 100
            green_y_rate = 100 - (greenpoint.edit_diagram_position("point")[1] / self.window_height) * 100
            red_x_rate = redpoint.edit_diagram_position("point")[0] / self.window_width * 100
            red_y_rate = 100 - (redpoint.edit_diagram_position("point")[1] / self.window_height) * 100

            print("green_red", green_x_rate, green_y_rate, red_x_rate, red_y_rate)

            self.salt_bezier_curveInstance.Setx1y1(green_x_rate, green_y_rate)
            self.salt_bezier_curveInstance.Setx2y2(red_x_rate, red_y_rate)
            view_easing()

        #greenpoint.add_diagram_event("point", "ButtonRelease-1", easing_end)
        #redpoint.add_diagram_event("point", "ButtonRelease-1", easing_end)

        redpoint.callback_operation.set_event("click_end", easing_end)
        greenpoint.callback_operation.set_event("click_end", easing_end)

        #self.window_control.add_window_event("Button-1", window_size_edit_start)
        self.window_control.add_window_event("Configure", window_size_edit_mov)
        self.window_control.add_window_event("ButtonRelease-1", window_size_edit_end)


class CentralRole:
    pass
