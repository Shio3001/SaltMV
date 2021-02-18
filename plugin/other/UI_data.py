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

        print("UI生成")

    def new_territory(self, name):
        self.canvas_data.territory[name] = TerritoryData()

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

    def new_diagram(self, te_name, di_name):
        self.canvas_data.territory[te_name].diagram[di_name] = DiagramData()

    def del_diagram(self, te_name, di_name):
        del self.canvas_data.territory[te_name].diagram[di_name]

    def new_textbox(self, te_name, di_name):
        self.canvas_data.territory[te_name].diagram[di_name] = TextBoxData(self.canvas_data.canvas)

    def edit_diagram_size(self, te_name, di_name, x=None, y=None):
        self.canvas_data.territory[te_name].diagram[di_name].size = self.common_control.xy_compilation(self.canvas_data.territory[te_name].diagram[di_name].size, x=x, y=y)

    def edit_diagram_position(self, te_name, di_name, x=None, y=None):
        self.canvas_data.territory[te_name].diagram[di_name].position = self.common_control.xy_compilation(self.canvas_data.territory[te_name].diagram[di_name].position, x=x, y=y)

    def edit_diagram_fill(self, te_name, di_name, select):
        if select != True != False:
            self.operation["error"].action(message="TrueとFalse以外入れるなあほ")

        self.canvas_data.territory[te_name].diagram[di_name].fill = select

    def edit_diagram_color(self, te_name, di_name, color=None):
        if color is None or not color[0] == "#":
            color = self.GUI_alpha_color

        self.canvas_data.territory[te_name].diagram[di_name].color = color

    def edit_diagram_text(self, te_name, di_name, text=None):
        self.canvas_data.territory[te_name].diagram[di_name].text = text

    def get_diagram_contact(self, te_name, di_name):
        mouse, diagram_edge, diagram_join = self.common_control.contact_detection(self.canvas_data.territory[te_name].diagram[di_name])
        return mouse, diagram_edge, diagram_join

    #####################################################################################

    def add_territory_event(self, te_name,  key, func):  # event
        bind_id = []

        for di_name in self.canvas_data.territory[te_name].diagram.keys():
            new_bind_id = self.canvas_data.canvas.tag_bind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(key), func, "+")
            print("new_bind", new_bind_id)
            bind_id.append(new_bind_id)

        self.canvas_data.territory[te_name].event[self.common_control.get_bind_name(key, func)] = [key, func, bind_id]

    def del_territory_event(self, te_name,  key, func):  # event
        bind_name = self.common_control.get_bind_name(key, func)

        print("del", self.canvas_data.territory[te_name].event)

        bind_id = self.canvas_data.territory[te_name].event[bind_name][2]

        for di_name in self.canvas_data.territory[te_name].diagram.keys():
            print(di_name, bind_id, "bind")

            for b in bind_id:
                print(key, bind_id, b, "e")
                self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(key), b)

        del self.canvas_data.territory[te_name].event[bind_name]

    def all_add_territory_event(self, te_name):
        pass
        # for k, f in zip(self.canvas_data.territory[te_name].event.keys(), self.canvas_data.territory[te_name].event.values()):
        #    for di_name, f in zip(self.canvas_data.territory[te_name].diagram.keys(), self.canvas_data.territory[te_name].diagram.values()):
        #        new_bind_id = self.canvas_data.canvas.tag_bind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(key), func, "+")

    def all_del_territory_event(self, te_name):  # canvasの再生成時の復元
        for k, f in zip(self.canvas_data.territory[te_name].event.keys(), self.canvas_data.territory[te_name].event.values()):
            print(self.canvas_data.territory[te_name].event[k], f)

        self.canvas_data.territory[te_name].event = {}

    def get_territory_event(self, te_name):
        return self.canvas_data.territory[te_name].event

    #####################################################################################

    def add_diagram_event(self, te_name, di_name, key, func):  # event
        a = self.common_control.get_tag_name(te_name, di_name)
        bind_id = self.canvas_data.canvas.tag_bind(a, "<{0}>".format(key), func, "+")

        print(bind_id)

        self.canvas_data.territory[te_name].diagram[di_name].event[self.common_control.get_bind_name(key, func)] = [key, func, bind_id]

    def del_diagram_event(self, te_name, di_name, key, func):  # event
        bind_name = self.common_control.get_bind_name(key, func)
        bind_id = self.canvas_data.territory[te_name].diagram[di_name].event[bind_name][2]
        self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(key), bind_id)
        print("tag unbind")
        del self.canvas_data.territory[te_name].diagram[di_name].event[bind_name]

    def all_add_diagram_event(self, te_name, di_name):
        for k, f in zip(self.canvas_data.territory[te_name].diagram[di_name].event.keys(), self.canvas_data.territory[te_name].diagram[di_name].event.values()):
            self.canvas_data.territory[te_name].diagram[di_name].canvas.tag_bind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(f[0]), f[1], "+")

    def all_del_diagram_event(self, te_name, di_name):  # canvasの再生成時の復元
        for k, f in zip(self.canvas_data.territory[te_name].diagram[di_name].event.keys(), self.canvas_data.territory[te_name].diagram[di_name].event.values()):
            self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(f[0]), f[2])
            print(self.canvas_data.territory[te_name].diagram[di_name].event[k], f)

        self.canvas_data.territory[te_name].diagram[di_name].event = {}

    def get_diagram_event(self, te_name, di_name):
        return self.canvas_data.territory[te_name].diagram[di_name].event

    #####################################################################################

    def territory_draw(self, te_name):
        for k in self.canvas_data.territory[te_name].diagram.keys():
            self.diagram_draw(te_name, k)

    def diagram_draw(self, te_name, di_name):
        territory_data = self.canvas_data.territory[te_name]
        diagram_data = self.canvas_data.territory[te_name].diagram[di_name]

        xy, size_xy = [0, 0], [0, 0]  # 領域基準

        for i in range(2):
            if diagram_data.fill:  # 座標の計算
                xy[i] = territory_data.position[i]
                size_xy[i] = territory_data.size[i]

                print("座標全選択")

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

        canvas_center = [size - xy / 2 for xy, size in zip(xy, size_xy)]

        print(xy, size_xy)

        if not diagram_data.text is None:
            self.canvas_data.canvas.create_text(canvas_center[0], canvas_center[1], text=diagram_data.text, tags=self.common_control.get_tag_name(te_name, di_name))
            return

        color = diagram_data.color

        print(color)
        self.canvas_data.canvas.create_rectangle(xy[0], xy[1], size_xy[0], size_xy[1], fill=color, outline="", width=0, tags=self.common_control.get_tag_name(te_name, di_name))  # 塗りつぶし
        return


class TerritoryData:
    def __init__(self):
        self.size = [0, 0]
        self.position = [0, 0]
        self.diagram = {}
        self.event = {}

        self.blank_space = [0, 0]


class DiagramData:
    def __init__(self):
        self.size = [0, 0]
        self.position = [0, 0]
        self.text = None
        self.color = ""
        self.fill = False

        self.event = {}

    def event_link(self):
        pass

    def set_color(self, color):
        self.color = color


class TextBoxData:
    def __init__(self, territory):
        self.position = [0, 0]
        self.text = ""
