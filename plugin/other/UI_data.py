import tkinter as tk
import copy
import inspect

permission = 3  # 接触範囲許可範囲


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self, window, all_data, all_UI_data, GUI_base_color, GUI_alpha_color):
        self.window = window
        self.all_data = all_data
        self.operation = all_data.operation
        self.all_UI_data = all_UI_data
        self.GUI_base_color = GUI_base_color
        self.GUI_alpha_color = GUI_alpha_color

        self.common_control = CommonControl(self.window)
        self.tk = tk

        self.canvas_data = CanvasData(self.window)

    # 以下canvas

    def edit_canvas_size(self, x=None, y=None):
        self.canvas_data.size = self.common_control.xy_compilation(self.canvas_data.size, x=x, y=y)

    def edit_canvas_position(self, x=None, y=None):
        self.canvas_data.position = self.common_control.xy_compilation(self.canvas_data.position, x=x, y=y)

    def get_canvas_contact(self):
        canvas_edge, canvas_join = self.common_control.xy_compilation(self.canvas_data)
        return canvas_edge, canvas_join

    # 以下territory

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

    # 以下diagram

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

    #####################################################################################

    def add_canvas_event(self, key, func):  # event
        self.canvas_data.event[self.common_control.get_bind_name(key, func)] = [key, func]
        self.canvas_data = self.common_control.canvas_event_bind(self.canvas_data)

    def del_canvas_event(self, key, func):  # event
        del self.canvas_data.event[self.common_control.get_bind_name(key, func)]

    def add_territory_event(self, name, key, func):  # event
        self.canvas_data.territory[name].event[self.common_control.get_bind_name(key, func)] = [key, func]
        self.canvas_data = self.common_control.territory_event_bind(self.canvas_data, name)

    def del_territory_event(self, name, key, func):  # event
        del self.canvas_data.territory[name].event[self.common_control.get_bind_name(key, func)]

    def add_diagram_event(self, ca_name, di_name, key, func):  # event
        self.canvas_data.territory[ca_name].diagram[di_name].event[self.common_control.get_bind_name(key, func)] = [key, func]
        self.canvas_data.diagram[di_name] = self.common_control.diagram_event_bind(self.canvas_data, ca_name, di_name)

    def del_diagram_event(self, ca_name, di_name, key, func):  # event
        del self.canvas_data.territory[ca_name].diagram[di_name].event[self.common_control.get_bind_name(key, func)]

    #####################################################################################

    def canvas_draw(self):
        for territory in self.canvas_data.territory:
            self.territory_draw(territory)

    def territory_draw(self, territory_data):
        for diagram in territory_data.diagram:
            self.diagram_draw(territory_data, diagram)

    def diagram_draw(self, territory_data, diagram_data):
        x, y, size_x, size_y = 0, 0, 0, 0

        if diagram_data.fill:
            x = territory_data.position[0]
            y = territory_data.position[1]

            size_x = territory_data.size[0]
            size_y = territory_data.size[0]

        else:
            x = territory_data.position[0] + diagram_data.position[0]
            y = territory_data.position[1] + diagram_data.position[1]

            size_x = diagram_data.size[0]
            size_y = diagram_data.size[1]

        color = diagram_data.color
        self.canvas_data.canvas.create_rectangle(x, y, size_x, size_y, fill=color, outline="", width=0, tags="")  # 塗りつぶし


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
        self.color = ""

        self.event = {}

    def event_link(self):
        pass

    def set_color(self, color):
        self.color = color


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

    def canvas_event_bind(self, data):
        for name, kp in zip(data.event.keys(), data.event.values()):
            data.canvas.bind("<{0}>".format(kp[0]), kp[1], "+")
        return data

    def territory_event_bind(self, data, name):
        return data

    def diagram_event_bind(self, data, ca_name, di_name):
        # for name, kp in zip(data.event.keys(), data.event.values()):
        #    data.canvas.bind("<{0}>".format(kp[0]), kp[1], "+")
        return data

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

    def get_bind_name(self, key, func):
        func_name = str(func.__name__)
        name = "{0}_{1}".format(key, func_name)
        print(name)
        return func_name
