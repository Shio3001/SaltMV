import tkinter as tk
import copy
import inspect


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self, window, canvas_data, common_control, all_data, all_UI_data, GUI_base_color, GUI_alpha_color):
        self.window = window
        self.canvas_data = canvas_data
        self.all_data = all_data
        self.operation = all_data.operation
        self.all_UI_data = all_UI_data
        self.GUI_base_color = GUI_base_color
        self.GUI_alpha_color = GUI_alpha_color

        self.common_control = common_control

        self.tk = tk

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
        mouse, territory_edge, territory_join = self.common_control.contact_detection(self.canvas_data.territory[name])
        return mouse, territory_edge, territory_join

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

    def edit_diagram_color(self, ca_name, di_name, color=None):
        if color is None:
            color = self.GUI_alpha_color
        self.canvas_data.territory[ca_name].diagram[di_name].color = color

    def edit_diagram_text(self, ca_name, di_name, text=None):

        self.canvas_data.territory[ca_name].diagram[di_name].text = text

    def get_diagram_contact(self, ca_name, di_name):
        mouse, diagram_edge, diagram_join = self.common_control.contact_detection(self.canvas_data.territory[ca_name].diagram[di_name])
        return mouse, diagram_edge, diagram_join

    #####################################################################################

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
        for v, k in zip(territory_data.diagram.keys(), territory_data.diagram.vales()):
            self.diagram_draw(territory_data, v)

    def diagram_draw(self, territory_data, diagram_data):
        xy, size_xy = [0, 0], [0, 0]  # 領域基準

        for i in range(2):
            if diagram_data.fill:  # 座標の計算
                xy[i] = territory_data.position[i]
                size_xy[i] = territory_data.size[i]

            else:
                xy[i] = territory_data.position[i] + diagram_data.position[i]
                size_xy[i] = diagram_data.size[i]

            # 左側が図形ー右側が余白反映

            if xy[i] < territory_data.blank_space[i]:
                difference = territory_data.blank_space[i] - xy[i]
                print("左上減算 : {0}".format(difference))

                xy[i] += difference
                size_xy[i] -= difference

            if xy[i] + size_xy[i] > territory_data.position[i] + territory_data.size[i] - territory_data.blank_space[i]:
                difference = (territory_data.position[i] + territory_data.size[i] - territory_data.blank_space[i]) - (xy[i] + size_xy[i])
                print("右下減算 : {0}".format(difference))

                size_xy[i] += difference

        if not diagram_data.text is None:
            pass

        color = diagram_data.color
        self.canvas_data.canvas.create_rectangle(xy[0], xy[1], size_xy[0], size_xy[1], fill=color, outline="", width=0, tags="")  # 塗りつぶし


class TerritoryData:
    def __init__(self, canvas):
        self.size = [0, 0]
        self.position = [0, 0]
        self.canvas = canvas
        self.diagram = {}
        self.event = {}

        self.blank_space = [0, 0]


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
