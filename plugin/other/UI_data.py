import tkinter as tk
import copy

"""
class SendCanvasData:
    def __init__(self, window, all_data, all_UI_data, GUI_base_color, GUI_alpha_color):
        self.window = window
        self.tk = tk
        self.operation = all_data.operation
        self.all_data = all_data
        self.all_UI_data = all_UI_data

        self.canvas_size = [10, 10]
        self.canvas_position = [0, 0]


class SendTextData:
    def __init__(self, window, all_data, all_UI_data, GUI_base_color, GUI_alpha_color):
"""


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self, window, all_data, all_UI_data, GUI_base_color, GUI_alpha_color):
        # canvas系：文字入力なし 表示だけ
        # textbox系：文字入力あり 入力あり
        self.window = window
        self.tk = tk

        self.canvas = None

        self.operation = all_data.operation
        self.all_data = all_data
        self.all_UI_data = all_UI_data

        self.canvas_size = [10, 10]
        self.canvas_position = [0, 0]

        # self.canvas_color = GUI_alpha_color

        self.text = ""
        self.text_position = [0, 0]

        self.event_canvas_key = []
        self.event_canvas_processing = []

        self.event_window_key = []
        self.event_window_processing = []

        self.processing = self.template
        self.user_event = "Button-2"

        self.mouse_position = [0, 0]
        self.view_data = {}
        self.view_within = {}
        #self.motion_history = []

        self.territory_data = {}

        self.canvas_pic = None

        self.mouse_motion = {"catch": False}
        self.mouse_touch = {}
        self.canvas_within = {"x": False, "y": False, "xy": False}

        self.window_event_data = {}

        self.prg_dict = {}

        self.GUI_base_color = GUI_base_color
        self.GUI_alpha_color = GUI_alpha_color

        self.operation["log"].write("パーツ初期設定")

    def template(self):
        self.operation["log"].write("関数が指定されていません")

    def window_event_del(self, key):
        key_index = self.event_window_key.index(key)

        self.operation["log"].write("削除前:{0} ".format(self.event_window_key))

        # self.window.unbind("{0}".format(key_index), self.event_window_processing[key_index])

        del self.event_window_key[key_index]
        del self.event_window_processing[key_index]

        self.operation["log"].write("削除:{0} 番号:{1}".format(key, key_index))
        self.operation["log"].write("key:{0} prg:{1}".format(self.event_window_key, self.event_window_processing))

        self.canvas_update()

    def canvas_event_del(self, key):
        self.operation["log"].write("削除前:{0} ".format(self.event_canvas_key))

        key_index = self.event_canvas_key.index(key)

        # self.window.unbind("{0}".format(key_index), self.event_canvas_processing[key_index])
        del self.event_canvas_key[key_index]
        del self.event_canvas_processing[key_index]

        self.operation["log"].write("削除:{0} 番号:{1}".format(key, key_index))
        self.operation["log"].write("key:{0} prg:{1}".format(self.event_canvas_key, self.event_canvas_processing))

        self.canvas_update()

    def canvas_update(self):
        if not self.canvas is None:
            self.canvas.destroy()
            # self.operation["log"].write("パーツ更新のため削除")

        print("c1", self.canvas)
        self.canvas = tk.Canvas(self.window, highlightthickness=0, width=self.canvas_size[0], height=self.canvas_size[1])
        # self.canvas.configure(bg=self.GUI_alpha_color)
        # self.canvas.place(x=self.canvas_position[0], y=self.canvas_position[1])
        print("c2", self.canvas)
        self.canvas_change_position()
        self.paint()

        for k, p in zip(self.event_window_key, self.event_window_processing):
            self.window.bind("<{0}>".format(k), p, "+")

        for k, p in zip(self.event_canvas_key, self.event_canvas_processing):
            self.canvas.bind("<{0}>".format(k), p, "+")

        for data in self.territory_data:
            for k, p in zip(data.data.event_key, data.data.event_processing):
                self.canvas.bind("<{0}>".format(k), p, "+")

        self.operation["log"].write("キャンバス設置")

    def set_canvas_pic(self):
        if self.canvas_pic is None:
            pass

    def make_blank_space(self, data, view_position, view_size, blank_limitline):

        # 左、上,右,下

        self.operation["log"].write("限界線", blank_limitline)
        self.operation["log"].write("限界線修正前", view_position, view_size)

        for i in [0, 1]:  # 余白を作る
            if view_position[i] < blank_limitline[0][i]:
                view_size[i] -= blank_limitline[0][i] - view_position[i]
                view_position[i] = blank_limitline[0][i]

                self.operation["log"].write("座標修正", view_position)

            if view_position[i] + view_size[i] > blank_limitline[1][i]:
                view_size[i] = blank_limitline[1][i] - view_position[i]

                self.operation["log"].write("サイズ修正", view_size)

        self.operation["log"].write("限界線修正後", view_position, view_size)
        self.operation["log"].write()

        return view_position, view_size

    def paint(self):

        if self.__canvas_authenticity() == "Entry":
            return

        self.canvas.delete("all")

        for data in list(self.view_data.values()):

            view_position = copy.deepcopy(data.position)
            view_size = copy.deepcopy(data.size)

            blank_limitline = [data.blank_space, [self.canvas_size[i] - data.blank_space[i] for i in [0, 1]]]

            if data.blank_space != [0, 0]:
                view_position, view_size = self.make_blank_space(data, view_position, view_size, blank_limitline)

            if data.fill == True:
                self.__view_paint(data.blank_space[0], data.blank_space[1], self.canvas_size[0] - data.blank_space[0], self.canvas_size[1] - data.blank_space[1], color=data.color)
            else:

                for s, i in zip(["x", "y"], [0, 1]):
                    if data.match[s] == True:
                        view_position[i] = 0
                        view_size[i] = self.canvas_size[i] - data.blank_space[i]

                self.__view_paint(view_position[0], view_position[1], view_size[0] + view_position[0], view_size[1] + view_position[1], color=data.color)

        if not self.text is None:
            canvas_center = [s / 2 for s in self.canvas_size]
            self.canvas.create_text(canvas_center[0], canvas_center[1], text=self.text)

    def __view_paint(self, x, y, size_x, size_y, color=None):  # 塗りつぶし
        if self.canvas_pic is None:
            self.canvas.create_rectangle(x, y, size_x, size_y, fill=color, outline="", width=0, tags="")  # 塗りつぶし
        else:
            self.canvas.create_rectangle(x, y, size_x, size_y, outline="", width=0, image=self.canvas_pic, anchor='nw')  # 塗りつぶし
        # self.canvas.create_rectangle(0 + data.blank_space[0], 0 + data.blank_space[1], self.canvas_size[0] - data.blank_space[0], self.canvas_size[1] - data.blank_space[1], fill=data.color, outline="", width=0)  # 塗りつぶし
        # self.canvas.create_rectangle(view_position[0], view_position[1], view_size[0] + view_position[0], view_size[1] + view_position[1], fill=data.color, outline="", width=0)  # 塗りつぶし
        return

    def tk_picture(self, tk_image):
        self.canvas.delete("all")
        self.canvas_pic = tk_image
        self.__view_paint(0, 0, self.canvas_size[0], self.canvas_size[1])
        return

    def canvas_change_size(self):
        self.canvas.config(width=self.canvas_size[0])
        self.canvas.config(height=self.canvas_size[1])

        self.paint()

    def canvas_change_position(self):
        self.canvas.place(x=self.canvas_position[0], y=self.canvas_position[1])
        self.paint()

    def canvas_for_event(self, processing=None, user_event=None):
        if not user_event is None:
            self.event_canvas_key.append(user_event)
            self.event_canvas_processing.append(processing)
        self.canvas_update()

    def window_for_event(self, processing=None, user_event=None):
        if not user_event is None:
            self.event_window_key.append(user_event)
            self.event_window_processing.append(processing)
        self.canvas_update()

    def edit_canvas_position(self, width_position=None, height_position=None):
        _ = self.__canvas_authenticity()
        if not width_position is None:
            self.canvas_position[0] = width_position
        if not height_position is None:
            self.canvas_position[1] = height_position
        self.canvas_change_position()

    def edit_canvas_size(self, width_size=None, height_size=None):
        _ = self.__canvas_authenticity()
        if not width_size is None:
            self.canvas_size[0] = width_size
        if not height_size is None:
            self.canvas_size[1] = height_size
        self.canvas_change_size()

    def edit_canvas_text(self, text=None, width_text_position=None, height_text_position=None):
        self.text = text
        self.text_position = [width_text_position, height_text_position]
        self.canvas_update()

    def set_mouse_motion(self, select, cursor=None):
        self.mouse_motion["catch"] = select
        self.canvas_update()

    def edit_territory_new(self, name):
        self.territory_data[name] = PartsTerritoryData()

    def edit_territory_position(self, name, width_position=None, height_position=None):
        if not width_position is None:
            self.territory_data[name].position[0] = width_position
        if not height_position is None:
            self.territory_data[name].position[1] = height_position

    def edit_territory_size(self, name, width_size=None, height_size=None):
        if not width_size is None:
            self.territory_data[name].size[0] = width_size
        if not height_size is None:
            self.territory_data[name].size[1] = height_size

    def territory_for_event(self, processing=None, user_event=None):
        if not user_event is None:
            # self.event_territory[]
            self.event_canvas_key.append(user_event)
            self.event_canvas_processing.append(processing)
        self.canvas_update()

        self.paint()
    # canvas内描画のため

    def edit_view_new(self, name):
        self.view_data[name] = PartsViewData(self.GUI_alpha_color)
        self.canvas_update()
        self.disclosure()

    def edit_view_color(self, name, color=None):
        if not color is None:
            self.view_data[name].color = color
        self.paint()

    def edit_view_position(self, name, width_position=None, height_position=None):
        if not width_position is None:
            self.view_data[name].position[0] = width_position
        if not height_position is None:
            self.view_data[name].position[1] = height_position
        self.paint()

    def edit_view_size(self, name, width_size=None, height_size=None):
        if not width_size is None:
            self.view_data[name].size[0] = width_size
        if not height_size is None:
            self.view_data[name].size[1] = height_size
        self.paint()

    def edit_view_fill(self, name, fill_select):
        self.view_data[name].fill = fill_select
        self.view_data[name].size = self.canvas_size
        self.paint()

    def edit_view_blank_space(self, name, width_size=None, height_size=None):  # blank_space = 空白設定
        if not width_size is None:
            self.view_data[name].blank_space[0] = width_size
        if not height_size is None:
            self.view_data[name].blank_space[1] = height_size
        self.paint()

    def disclosure(self):  # canvasに書かれている描画keyを開示
        self.operation["log"].write(list(self.view_data.keys()))

    def edit_view_match(self, name, direction, user_select):
        self.view_data[name].match[direction] = user_select

    # テキストボックスのため

    def textbox_update(self):
        if not self.canvas is None:
            _ = self.textbox_text_get()
            self.canvas.destroy()

        self.canvas = tk.Entry()
        self.canvas = self.tk.Entry(width=self.canvas_size[0], highlightthickness=0, relief="flat")
        self.canvas_change_position()

        self.canvas.insert(0, self.text)

    def textbox_text_get(self):
        self.text = self.canvas.get()
        return self.text

    def __canvas_authenticity(self):  # キャンバスかどうかを確認
        if str(type(self.canvas)) == "<class 'tkinter.Canvas'>":
            self.operation["log"].write("Canvas")
            return "Canvas"

        elif str(type(self.canvas)) == "<class 'tkinter.Entry'>":
            self.operation["log"].write("Entry")
            return "Entry"

        else:
            self.operation["log"].write("canvasが設定されていません")
            self.canvas_update()
            return None

    def set_cursor(self, name=None):  # マウスのcursorをnameに入ってるものに変更する
        if name is None:
            name = "arrow"

        self.window.config(cursor=name)
        self.canvas.config(cursor=name)

    # def notion_andkey(self, name):  # マウスが動いたときのeventを設定
    #    self.notion_key = name

    def get_window_data(self):
        return {"size": [self.window.winfo_width(), self.window.winfo_height()]}

    def get_canvas_data(self):  # canvasのwindow内相対位置を返却
        return {"position": copy.deepcopy(self.canvas_position), "size": copy.deepcopy(self.canvas_size)}

    # def get_territory_data(self,name):
    #    return {"position","size": }

    def get_mouse_position(self, name, reset=None):  # mouseのwindow内相対位置を返却

        if reset == True:
            self.__mouse_data_set()

        self.mouse_position_get(name)
        return copy.deepcopy(self.mouse_motion), copy.deepcopy(self.mouse_touch), copy.deepcopy(self.canvas_within)

    def get_view_position(self):  # 長方形など四角形(0°)のときのみしかつかえません、あしからず
        for k, d in zip(list(self.view_data.keys()), list(self.view_data.values())):
            # self.operation["log"].write(d.position)
            # self.operation["log"].write(d.size)
            touch_xy = [(d.position[i] + self.canvas_position[i]) <= self.mouse_motion[ixy] <= (d.position[i] + d.size[i] + self.canvas_position[i]) for i, ixy in zip([0, 1], ["x", "y"])]
            if sum(touch_xy) == 2:
                self.view_within[k] = True
            else:
                self.view_within[k] = False

            # self.operation["log"].write(sum(touch_xy))

        return self.view_within

    def __mouse_data_set(self):
        self.mouse_motion["x"] = self.window.winfo_pointerx() - self.window.winfo_rootx()
        self.mouse_motion["y"] = self.window.winfo_pointery() - self.window.winfo_rooty()
        self.mouse_touch["left"] = False  # 左
        self.mouse_touch["right"] = False  # 右
        self.mouse_touch["top"] = False
        self.mouse_touch["under"] = False

        self.mouse_touch["left_inside"] = False  # 左
        self.mouse_touch["right_inside"] = False  # 右
        self.mouse_touch["top_inside"] = False
        self.mouse_touch["under_inside"] = False

        self.territory_within = {"x": False, "y": False, "xy": False}
        #self.canvas_within = {"x": False, "y": False, "xy": False}

    def mouse_position_get(self, name):
        self.__mouse_data_set()

        edge = {}

        edge["left"] = self.canvas_position[0] + self.territory_data[name].position[0]
        edge["right"] = edge["left"] + self.territory_data[name].position[0]
        edge["top"] = self.canvas_position[1] + self.territory_data[name].position[1]
        edge["under"] = edge["top"] + self.territory_data[name].position[1]

        tolerance = 3  # 許容範囲

        if edge["left"] - tolerance <= self.mouse_motion["x"] <= edge["left"] + tolerance:
            self.mouse_touch["left"] = True

        if edge["right"] - tolerance <= self.mouse_motion["x"] <= edge["right"] + tolerance:
            self.mouse_touch["right"] = True

        if edge["top"] - tolerance <= self.mouse_motion["y"] <= edge["top"] + tolerance:
            self.mouse_touch["top"] = True

        if edge["under"] - tolerance <= self.mouse_motion["y"] <= edge["under"] + tolerance:
            self.mouse_touch["under"] = True

        if not self.canvas is None:
            for i, j in zip([["left", "right"], ["top", "under"]], ["x", "y"]):
                if edge[i] <= self.mouse_motion[j] <= edge[i]:
                    self.territory_within[j] = True
                else:
                    self.territory_within[j] = False

            if self.territory_within["x"] == True and self.territory_within["y"] == True:
                self.territory_within["xy"] = True
            else:
                self.territory_within["xy"] = False


class PartsTerritoryData:
    def __init__(self):
        self.position = [0, 0]
        self.size = [0, 0]

        self.event_key = []
        self.event_processing = []
        self.territory_within = {}


class PartsViewData:
    def __init__(self, color):
        self.color = color
        self.position = [0, 0]
        self.size = [0, 0]
        self.fill = False
        self.match = {"x": False, "y": False}
        self.blank_space = [0, 0]


# classひとつひとつに描画するデータを差し込み、classの数forかなにかでまわして描画していく作戦s
