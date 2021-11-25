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
        self.view_width_size01 = 0

        self.close_save_green = "#229922"
        self.close_save_red = "#992222"
        self.close_save_gray = "#111111"

        self.green_x_rate = 0
        self.green_y_rate = 0

        self.red_x_rate = 100
        self.red_y_rate = 100

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

            print("終了処理")

            close_save.edit_diagram_color("background", self.close_save_gray)
            self.window_control.window.update()
            close_save.territory_draw()
            self.window_control.edit_control_auxiliary.callback_operation.event("easing_request_end", info=(self.green_x_rate, self.green_y_rate, self.red_x_rate, self.red_y_rate))
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

        def for_textbox():
            textboxGX.edit_diagram_text("textbox", text=str(self.green_x_rate))
            textboxGY.edit_diagram_text("textbox", text=str(self.green_y_rate))
            textboxRX.edit_diagram_text("textbox", text=str(self.red_x_rate))
            textboxRY.edit_diagram_text("textbox", text=str(self.red_y_rate))

        def easing_request(info):
            self.window_control.window_open_close(True)
            close_save.edit_diagram_color("background", self.close_save_green)
            self.green_x_rate, self.green_y_rate, self.red_x_rate, self.red_y_rate = info

            for_textbox()
            window_size_edit_end()
            input_forcpp()

        self.window_control.edit_control_auxiliary.callback_operation.set_event("easing_request", easing_request)

        def green_red_view():

            gx = self.window_width * self.green_x_rate / 100
            gy = self.view_height_size08 * (100 - self.green_y_rate) / 100
            rx = self.window_width * self.red_x_rate / 100
            ry = self.view_height_size08 * (100 - self.red_y_rate) / 100
            greenpoint.edit_diagram_position("point", x=gx, y=gy)
            redpoint.edit_diagram_position("point", x=rx, y=ry)
            greenpoint.territory_draw()
            redpoint.territory_draw()

        def textboxGX_input(text):
            self.green_x_rate = int(text)
            input_forcpp()

        def textboxGY_input(text):
            self.green_y_rate = int(text)
            input_forcpp()

        def textboxRX_input(text):
            self.red_x_rate = int(text)
            input_forcpp()

        def textboxRY_input(text):
            self.red_y_rate = int(text)
            input_forcpp()

        def input_forcpp():

            # self.green_x_rate = greenpoint.edit_diagram_position("point")[0] / self.window_width * 100
            # self.green_y_rate = 100 - (greenpoint.edit_diagram_position("point")[1] / self.view_height_size08) * 100
            # self.red_x_rate = redpoint.edit_diagram_position("point")[0] / self.window_width * 100
            # self.red_y_rate = 100 - (redpoint.edit_diagram_position("point")[1] / self.view_height_size08) * 100

            green_red_view()

            self.salt_bezier_curveInstance = self.salt_bezier_curveModule.ForPyInterface(int(self.window_width), int(self.view_height_size08))
            self.salt_bezier_curveInstance.Setx1y1(self.green_x_rate, self.green_y_rate)
            self.salt_bezier_curveInstance.Setx2y2(self.red_x_rate, self.red_y_rate)
            view_easing()

        textboxGX = self.window_control.new_parts("easing_beziercurve", "textboxGX", parts_name="textbox")  # 左側のやつ
        textboxGX.edit_diagram_position("textbox", x=0, y=0)
        textboxGX.edit_diagram_size("textbox", x=200, y=30)
        textboxGX.territory_draw()
        textboxGY = self.window_control.new_parts("easing_beziercurve", "textboxGY", parts_name="textbox")  # 左側のやつ
        textboxGY.edit_diagram_position("textbox", x=0, y=0)
        textboxGY.edit_diagram_size("textbox", x=200, y=30)
        textboxGY.territory_draw()
        textboxRX = self.window_control.new_parts("easing_beziercurve", "textboxRX", parts_name="textbox")  # 左側のやつ
        textboxRX.edit_diagram_position("textbox", x=0, y=0)
        textboxRX.edit_diagram_size("textbox", x=200, y=30)
        textboxRX.territory_draw()
        textboxRY = self.window_control.new_parts("easing_beziercurve", "textboxRY", parts_name="textbox")  # 左側のやつ
        textboxRY.edit_diagram_position("textbox", x=0, y=0)
        textboxRY.edit_diagram_size("textbox", x=200, y=30)
        textboxRY.territory_draw()

        textboxGX.edit_diagram_text("textbox", entry_event=textboxGX_input)
        textboxGY.edit_diagram_text("textbox", entry_event=textboxGY_input)
        textboxRX.edit_diagram_text("textbox", entry_event=textboxRX_input)
        textboxRY.edit_diagram_text("textbox", entry_event=textboxRY_input)
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
            self.view_width_size01 = int(self.window_width * 0.1)

            close_save.edit_territory_position(x=0, y=self.view_height_size08)
            close_save.edit_territory_size(x=self.view_width_size01 * 2, y=self.view_height_size01 * 2)
            close_save.territory_draw()

            textboxGX.edit_diagram_position("textbox", x=self.view_width_size01 * 2, y=self.view_height_size08)
            textboxGX.edit_diagram_size("textbox", x=self.view_width_size01 * 4, y=self.view_height_size01)
            textboxGX.edit_diagram_text("textbox", text_color="#111111")
            textboxGX.edit_diagram_text("textbox", back_ground_color="#88ff88")
            textboxGX.territory_draw()

            textboxGY.edit_diagram_position("textbox", x=self.view_width_size01 * 2, y=self.view_height_size08 + self.view_height_size01)
            textboxGY.edit_diagram_size("textbox", x=self.view_width_size01 * 4, y=self.view_height_size01)
            textboxGY.edit_diagram_text("textbox", text_color="#111111")
            textboxGY.edit_diagram_text("textbox", back_ground_color="#88ff88")
            textboxGY.territory_draw()

            textboxRX.edit_diagram_position("textbox", x=self.view_width_size01 * 6, y=self.view_height_size08)
            textboxRX.edit_diagram_size("textbox", x=self.view_width_size01 * 4, y=self.view_height_size01)
            textboxRX.edit_diagram_text("textbox", text_color="#111111")
            textboxRX.edit_diagram_text("textbox", back_ground_color="#ff8888")
            textboxRX.territory_draw()

            textboxRY.edit_diagram_position("textbox", x=self.view_width_size01 * 6, y=self.view_height_size08 + self.view_height_size01)
            textboxRY.edit_diagram_size("textbox", x=self.view_width_size01 * 4, y=self.view_height_size01)
            textboxRY.edit_diagram_text("textbox", text_color="#111111")
            textboxRY.edit_diagram_text("textbox", back_ground_color="#ff8888")
            textboxRY.territory_draw()

            self.salt_bezier_curveInstance = self.salt_bezier_curveModule.ForPyInterface(int(self.window_width), int(self.view_height_size08))

            print("再インスタンス化", self.window_width, self.window_height)

            print("end", self.flag_re_instance)

            self.salt_bezier_curveInstance.Setx1y1(self.green_x_rate, self.green_y_rate)
            self.salt_bezier_curveInstance.Setx2y2(self.red_x_rate, self.red_x_rate)
            view_easing()

            point_size = self.window_width * 0.025

            if point_size < 10:
                point_size = 10

            greenpoint.edit_diagram_size("point", point_size, point_size)
            redpoint.edit_diagram_size("point", point_size, point_size)

            green_red_view()

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

            self.green_x_rate = greenpoint.edit_diagram_position("point")[0] / self.window_width * 100
            self.green_y_rate = 100 - (greenpoint.edit_diagram_position("point")[1] / self.view_height_size08) * 100
            self.red_x_rate = redpoint.edit_diagram_position("point")[0] / self.window_width * 100
            self.red_y_rate = 100 - (redpoint.edit_diagram_position("point")[1] / self.view_height_size08) * 100

            for_textbox()

            print("green_red", self.green_x_rate, self.green_y_rate, self.red_x_rate, self.red_y_rate)

            self.salt_bezier_curveInstance.Setx1y1(self.green_x_rate, self.green_y_rate)
            self.salt_bezier_curveInstance.Setx2y2(self.red_x_rate, self.red_y_rate)
            view_easing()

        #greenpoint.add_diagram_event("point", "ButtonRelease-1", easing_end)
        #redpoint.add_diagram_event("point", "ButtonRelease-1", easing_end)

        redpoint.callback_operation.set_event("click_end", easing_end)
        greenpoint.callback_operation.set_event("click_end", easing_end)

        #self.window_control.add_window_event("Button-1", window_size_edit_start)
        self.window_control.add_window_event("Configure", window_size_edit_mov)
        self.window_control.add_window_event("ButtonRelease-1", window_size_edit_end)

        window_size_edit_end()
        # self.window_control.window_open_close(False)


class CentralRole:
    pass
