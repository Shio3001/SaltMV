# coding:utf-8
import sys
import numpy as np
import os
import copy
import tkinter as tk

GUI_main_name = "GUI_main"
GUI_base_Color = "#1a1a1a"


class CentralRole:
    def __init__(self):
        pass

    def main(self, all_elements, elements, internal_operation, app_name):
        expansion_keys = internal_operation["plugin"]["expansion"].keys()
        expansion_list = {}

        GUI_UI = internal_operation["plugin"]["GUI_UI"]

        base_data = [internal_operation, all_elements, elements, GUI_UI]
        send_main = SendWindowData(None, base_data)
        expansion_list["main"] = internal_operation["plugin"]["expansion"][GUI_main_name].InitialValue(send_main).main()

        for key in list(expansion_keys):
            print(key)
            if key != GUI_main_name:
                send_sub = SendWindowData(expansion_list["main"].window, base_data)
                expansion_list[key] = internal_operation["plugin"]["expansion"][key].InitialValue(send_sub).main()

        print(expansion_list)

        expansion_list["main"].window.mainloop()

        print("GUI終了")

        return


class SendWindowData:  # window生成のためのデータ
    def __init__(self, main_window, base_data):
        self.tk = tk
        self.menubar_list = {}
        self.window_size = [100, 100]
        self.window_name = "tkinter"
        self.main_window = main_window
        self.operation = base_data[0]
        self.all_elements = base_data[1]
        self.elements = base_data[2]
        print(base_data[3].keys())

        # self.GUI_UI = {key: base_data[3][key].parts(send_UI_data(self.main_window, self.operation)) for key in list(base_data[3].keys())}

        if not self.main_window is None:
            self.window = tk.Toplevel(self.main_window)
        else:
            self.window = tk.Tk()

        self.GUI_UI_parts = base_data[3]
        self.UI_operation = SendUIData(self.window, self.operation)

        self.window.configure(bg=GUI_base_Color)

    def display_size_get(self):
        self.display_size = [self.window.winfo_screenwidth(), self.window.winfo_screenheight()]
        return self.display_size

    def window_size_set(self, send):
        if not send is None:
            self.window_size = send
        self.window.resizable(width=True, height=True)
        self.window.geometry("{0}x{1}".format(self.window_size[0], self.window_size[1]))

    def window_title_set(self, send):
        if not send is None:
            self.window_name = send
        self.window.title(self.window_name)

    def menubar_set(self, send):
        if not send is None:
            self.menubar_list = send

        window_menubar = tk.Menu(self.window)
        self.window.config(menu=window_menubar)
        for bar in self.menubar_list:
            window_menubar_bar = tk.Menu(window_menubar, tearoff=0)
            window_menubar.add_cascade(label=bar[0], menu=window_menubar_bar)
            for tab in bar[1]:
                window_menubar_bar.add_command(label=tab[0], command=tab[1])

    def main(self):
        def window_exit():
            self.window.destroy()
            print("終了")

        self.window.mainloop()


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self, window, operation):
        self.window = window
        self.tk = tk
        self.operation = operation

        self.canvas = None

        self.canvas_size = [10, 10]
        self.canvas_position = [0, 0]

        self.canvas_color = "#ffffff"

        self.text = None
        self.text_position = [0, 0]

        self.event_key = None
        self.event_processing = None

        print("パーツ初期設定")

    def canvas_update(self):

        if not self.canvas is None:
            self.canvas.destroy()

        self.canvas = tk.Canvas(self.window, highlightthickness=0, width=self.canvas_size[0], height=self.canvas_size[1])
        self.canvas.place(x=self.canvas_position[0], y=self.canvas_position[1])
        self.canvas.create_rectangle(0, 0, self.canvas_size[0], self.canvas_size[1], fill=self.canvas_color, outline="")  # 塗りつぶし
        if not self.text is None:
            canvas_center = [s / 2 for s in self.canvas_size]
            self.canvas.create_text(canvas_center[0], canvas_center[1], text=self.text)

        if not self.event_key is None and not self.event_processing is None:
            self.canvas.bind('<{0}>'.format(self.event_key), self.event_processing)

    def canvas_for_button(self, processing=None, user_event=None):
        if processing is None:
            return

        if not user_event is None:
            self.event_key = user_event
            self.event_processing = processing

        self.canvas_update()

    def edit_canvas_position(self, width_position=None, height_position=None):
        if not width_position is None:
            self.canvas_position[0] = width_position
        if not height_position is None:
            self.canvas_position[1] = height_position

        self.canvas_update()

    def edit_canvas_size(self, width_size=None, height_size=None):
        if not width_size is None:
            self.canvas_size[0] = width_size
        if not height_size is None:
            self.canvas_size[1] = height_size

        self.canvas_update()

    def edit_canvas_text(self, text=None, width_text_position=None, height_text_position=None):
        self.text = text
        self.text_position = [width_text_position, height_text_position]

        self.canvas_update()

    def edit_canvas_color(self, color=None):
        if not color is None:
            self.canvas_color = color

        self.canvas_update()

    # def canvas_update(self):
        # self.canvas.create_rectangle(self.canvas_position[0], self.canvas_position[1], self.canvas_size[0], self.canvas_size[1], fill=self.canvas_color, outline="")  # 塗りつぶし

    """
    def place_canvas(self, width_position=None, height_position=None):

        

    def size_canvas(self)

    """

    """

    def new_canvas(self, width_size=None, height_size=None, width_position=None, height_position=None):

        if not width_size is None:
            self.canvas_size[0] = width_size
        if not height_size is None:
            self.canvas_size[1] = height_size
        if not width_position is None:
            self.position[0] = width_position
        if not height_position is None:
            self.position[1] = height_position

        del self.canvas

        self.canvas = tk.Canvas(self.window, highlightthickness=0, width=self.canvas_size[0], height=self.canvas_size[1])  # Canvasの作成
        self.canvas.place(x=self.position[0], y=self.position[1])

    def full_canvas(self, color="#ffffff"):
        self.__canvas_authenticity()
        self.canvas.create_rectangle(0, 0, self.canvas_size[0], self.canvas_size[1], fill='green', outline="")  # 塗りつぶし

    def for_Button_canvas(self, processing, user_event):
        if processing is None:
            return

        self.__canvas_authenticity()
        self.canvas.bind('<{0}>'.format(user_event), processing)

    def text_canvas(self, text="テキスト未指定"):
        self.__canvas_authenticity()
        canvas_center = [s / 2 for s in self.canvas_size]
        self.canvas.create_text(canvas_center[0], canvas_center[1], text=text)

    # ユーザー用 ----ここから上

    """
    # 処理用    ----ここから下

    def __canvas_authenticity(self):
        if str(type(self.canvas)) == "<class 'tkinter.Canvas'>":
            return True
        else:
            print("canvasが設定されていません")
            return False
