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

        def window_size_edit_start(e=None):
            print("start", self.flag_re_instance)

        def window_size_edit_mov(e=None):

            self.flag_re_instance = True

            print("mov", self.flag_re_instance)

        def window_size_edit_end(e=None):

            if not self.flag_re_instance:
                return

            self.window_width, self.window_height = self.window_control.get_window_size()
            self.salt_bezier_curveInstance = self.salt_bezier_curveModule.ForPyInterface(int(self.window_width), int(self.window_height))

            print("再インスタンス化", self.window_width, self.window_height)

            self.flag_re_instance = False

            print("end", self.flag_re_instance)

            self.salt_bezier_curveInstance.Setx1y1(0, 0)
            self.salt_bezier_curveInstance.Setx2y2(100, 100)
            view_easing()

        def view_easing():

            image_numpy = cv2.cvtColor(self.salt_bezier_curveInstance.GetView().astype('uint8').reshape(self.window_height, self.window_width, 1), cv2.COLOR_GRAY2RGB)

            self.window_control.edit_canvas_size("easing_beziercurve",  x=self.window_width, y=self.window_height)
            self.easing_preview.size_update(self.window_width, self.window_height)

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

            self.salt_bezier_curveInstance = self.salt_bezier_curveModule.ForPyInterface(int(self.window_width), int(self.window_height))

            green_x_rate = greenpoint.edit_diagram_position("point")[0] / self.window_width * 100
            green_y_rate = 100 - (greenpoint.edit_diagram_position("point")[1] / self.window_height) * 100
            red_x_rate = redpoint.edit_diagram_position("point")[0] / self.window_width * 100
            red_y_rate = 100 - (redpoint.edit_diagram_position("point")[1] / self.window_height) * 100

            print("green_red", green_x_rate, green_y_rate, red_x_rate, red_y_rate)

            self.salt_bezier_curveInstance.Setx1y1(green_x_rate, green_y_rate)
            self.salt_bezier_curveInstance.Setx2y2(red_x_rate, red_y_rate)
            view_easing()

        greenpoint.add_diagram_event("point", "ButtonRelease-1", easing_end)
        redpoint.add_diagram_event("point", "ButtonRelease-1", easing_end)

        self.window_control.add_window_event("Button-1", window_size_edit_start)
        self.window_control.add_window_event("Configure", window_size_edit_mov)
        self.window_control.add_window_event("ButtonRelease-1", window_size_edit_end)


class CentralRole:
    pass
