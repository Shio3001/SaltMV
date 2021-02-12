import tkinter as tk
import copy
import inspect

permission = 3  # 接触範囲許可範囲


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self, window, all_data, all_UI_data, GUI_base_color, GUI_alpha_color):
        self.window = window
        self.all_data = all_data
        self.all_UI_data = all_UI_data
        self.GUI_base_color = GUI_base_color
        self.GUI_alpha_color = GUI_alpha_color

        self.common_control = CommonControl(self.window)
        self.tk = tk

        self.canvas_data = CanvasData(self.window)

    def edit_canvas_size(self, x=None, y=None):
        self.canvas_data.size = self.common_control.xy_compilation(self.canvas_data.size, x=x, y=y)

    def edit_canvas_position(self, x=None, y=None):
        self.canvas_data.position = self.common_control.xy_compilation(self.canvas_data.position, x=x, y=y)

    def get_canvas_contact(self):
        canvas_edge, canvas_join = self.common_control.xy_compilation(self.canvas_data)
        return canvas_edge, canvas_join

    def add_canvas_event(self, key, func):
        func_name = self.common_control.get_func_name(func)
        self.canvas_data.event["{0}{1}".format(key, func_name)] = func
        self.canvas_data.canvas = self.common_control.event_bind(self.canvas_data.canvas, self.canvas_data.event)

    def del_canvas_event(self, key):
        del self.canvas_data.event[key]

    # territory

    def new_territory(self, name):
        self.canvas_data.territory[name] = TerritoryData(self.canvas_data.canvas)

    def del_territory(self, name):
        del self.canvas_data.territory[name]

    def edit_territory_size(self, name, x=None, y=None):
        self.canvas_data.territory[name].size = self.common_control.xy_compilation(self.canvas_data.territory[name].size, x=x, y=y)

    def edit_territory_position(self, name, x=None, y=None):
        self.canvas_data.territory[name].position = self.common_control.xy_compilation(self.canvas_data.territory[name].position, x=x, y=y)

    def get_territory_contact(self, name):
        territory_edge, territory_join = self.common_control.xy_compilation(self.canvas_data.territory[name])
        return territory_edge, territory_join

    """
    def add_territory_event(self, key, func):
        func_name = self.common_control.get_func_name(func)
        self.territory.event["{0}{1}".format(key, func_name)] = func
        self.territory.canvas = self.common_control.event_bind(self.territory.canvas, self.canvas_data.event)
    """

    # diagram

    def new_diagram(self, ca_name, di_name):
        self.canvas_data.territory[ca_name].diagram[di_name] = DiagramData(self.canvas_data.canvas)

    def del_diagram(self, ca_name, di_name):
        del self.canvas_data.territory[ca_name].diagram[di_name]

    def new_textbox(self, ca_name, di_name):
        self.canvas_data.territory[ca_name].diagram[di_name] = TextBoxData(self.canvas_data.canvas)

    def edit_diagram_size(self, ca_name, di_name, x=None, y=None):
        self.canvas_data.territory[ca_name].diagram[di_name].size = self.common_control.xy_compilation(self.canvas_data.territory[ca_name].diagram[di_name].size, x=x, y=y)

    def edit_diagram_position(self, ca_name, di_name, x=None, y=None):
        self.canvas_data.territory[ca_name].diagram[di_name].position = self.common_control.xy_compilation(self.canvas_data.territory[ca_name].diagram[di_name].position, x=x, y=y)

    def get_diagram_contact(self, ca_name, di_name):
        diagram_edge, diagram_join = self.common_control.xy_compilation(self.canvas_data.territory[ca_name].diagram[di_name])
        return diagram_edge, diagram_join


class CanvasData:
    def __init__(self, window):
        self.size = [0, 0]
        self.position = [0, 0]
        self.canvas = tk.Canvas(window, highlightthickness=0, width=self.size[0], height=self.size[1])
        self.territory = {}

        self.event = {}

    def event_link(self):
        pass


class TerritoryData:
    def __init__(self, canvas):
        self.size = [0, 0]
        self.position = [0, 0]
        self.canvas = canvas
        self.diagram = {}
        self.event = {}


class DiagramData:
    def __init__(self, territory):
        self.size = [0, 0]
        self.position = [0, 0]
        self.text = ""

        self.event = {}

    def event_link(self):
        pass


class TextBoxData:
    def __init__(self, territory):
        self.position = [0, 0]
        self.text = ""


class CommonControl:
    def __init__(self, window):
        self.window = window

    def xy_compilation(self, origin, x=None, y=None):  # 設定項目を変更する
        if not x is None:
            origin[0] = x

        if not y is None:
            origin[1] = y

        return origin

    # def contact_edge(self):
    #    return

    def event_bind(self, target, list):
        return target

    def get_mouse_position(self):  # マウスの位置を取得
        mouse = []
        mouse[0] = self.window.winfo_pointerx() - self.window.winfo_rootx()
        mouse[1] = self.window.winfo_pointery() - self.window.winfo_rooty()

        return mouse

    def contact_detection(self, data):  # 辺に触れているか
        mouse = self.get_mouse_position()

        edge_detection = [[False, False], [False, False]]  # 辺に対する #x左,x右,y上,y下
        join_detection = [False, False, False]  # 中に対する #x , y, xy

        for i in range(2):
            if (data.position[i] - permission) <= mouse[i] <= (data.position[i] + permission):
                edge_detection[i][0] = True

            if (data.position[i] + data.size[i] - permission) <= mouse[i] <= (data.position[i] + data.size[i] + permission):
                edge_detection[i][1] = True

        for j in range(2):

            if (data.position[i] - permission) <= mouse[i] <= (data.position[i] + data.size[i] + permission):
                join_detection[i] = True

        if join_detection[0] and join_detection[1]:
            join_detection[2] = True

        return edge_detection, join_detection

    def get_func_name(self, func):
        func_name = (str(func)[1].replace("<")).replace(">")
        print(func_name)
        return func_name
