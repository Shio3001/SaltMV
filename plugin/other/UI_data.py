import tkinter as tk
import copy
import inspect


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self, window, canvas_data, common_control, all_data, all_UI_data, GUI_base_color, GUI_alpha_color, window_event_data, canvas_event_data):
        self.window = window
        self.canvas_data = canvas_data
        self.all_data = all_data
        self.operation = all_data.operation
        self.all_UI_data = all_UI_data
        self.GUI_base_color = GUI_base_color
        self.GUI_alpha_color = GUI_alpha_color
        self.common_control = common_control
        self.tk = tk

        self.window_event_data = window_event_data
        self.canvas_event_data = canvas_event_data

        # print("UI生成")

    def event_not_func(self, event):
        print("テストイベント")

    def new_territory(self, name):
        self.canvas_data.territory[name] = TerritoryData()

        self.new_diagram(name, "base")
        self.edit_diagram_fill(name, "base", True)
        self.edit_diagram_color(name, "base", "#111111")

    def del_territory(self, name):
        del self.canvas_data.territory[name]

        self.territory_draw(name, te_del=True)

    def edit_territory_size(self, name, x=None, y=None):
        self.canvas_data.territory[name].size = self.common_control.xy_compilation(self.canvas_data.territory[name].size, x=x, y=y)
        return self.canvas_data.territory[name].size

    def edit_territory_position(self, name, x=None, y=None):
        self.canvas_data.territory[name].position = self.common_control.xy_compilation(self.canvas_data.territory[name].position, x=x, y=y)
        return self.canvas_data.territory[name].position

    def get_territory_contact(self, name, del_mouse=False):
        mouse, territory_edge, territory_join = self.common_control.contact_detection(self.canvas_data.territory[name].position, self.canvas_data.territory[name].size, del_mouse)
        return mouse, territory_edge, territory_join

    # 以下diagram

    def new_diagram(self, te_name, di_name, diagram_type=None):
        if diagram_type is None:
            self.canvas_data.territory[te_name].diagram[di_name] = DiagramData()

        if diagram_type == "text":
            self.canvas_data.territory[te_name].diagram[di_name] = DiagramTextData()

        if diagram_type == "textbox":
            self.canvas_data.territory[te_name].diagram[di_name] = TextBoxData(self.canvas_data.canvas)

        print(self.canvas_data.territory[te_name].diagram)

    # def new_diagram_text(self, te_name, di_name):
    #    self.canvas_data.territory[te_name].diagram[di_name] = DiagramTextData()

    def del_diagram(self, te_name, di_name):
        self.diagram_draw(te_name, di_name, di_del=True)
        del self.canvas_data.territory[te_name].diagram[di_name]

    # def new_textbox(self, te_name, di_name):
    #    self.canvas_data.territory[te_name].diagram[di_name] = TextBoxData(self.canvas_data.canvas)

    def edit_diagram_size(self, te_name, di_name, x=None, y=None):
        self.canvas_data.territory[te_name].diagram[di_name].size = self.common_control.xy_compilation(self.canvas_data.territory[te_name].diagram[di_name].size, x=x, y=y)

        return self.canvas_data.territory[te_name].diagram[di_name].size

    def edit_diagram_position(self, te_name, di_name, x=None, y=None):
        self.canvas_data.territory[te_name].diagram[di_name].position = self.common_control.xy_compilation(self.canvas_data.territory[te_name].diagram[di_name].position, x=x, y=y)

        return self.canvas_data.territory[te_name].diagram[di_name].position

    def edit_diagram_fill(self, te_name, di_name, select):

        if select != True and select != False:
            self.operation["error"].action(message="TrueとFalse以外入れるな")

        self.canvas_data.territory[te_name].diagram[di_name].fill = select

    def edit_diagram_text_center(self, te_name, di_name, xy, select):
        if not self.get_diagram_type(te_name, di_name, "DiagramTextData"):
            self.operation["error"].action(message="これテキスト用じゃないぞ")

        i = {"x": 0, "y": 1}
        self.canvas_data.territory[te_name].diagram[di_name].center[i[xy]] = select

    def edit_diagram_target(self, te_name, di_name, target_di_name):
        if not target_di_name in self.canvas_data.territory[te_name].diagram.keys():
            self.operation["error"].action(message="そのキーは存在しない")

        self.canvas_data.territory[te_name].diagram[di_name].target = target_di_name

    def edit_diagram_color(self, te_name, di_name, color=None):
        if color is None or not color[0] == "#":
            color = self.GUI_alpha_color

        self.canvas_data.territory[te_name].diagram[di_name].color = color

    def edit_diagram_text(self, te_name, di_name, text=None):
        self.canvas_data.territory[te_name].diagram[di_name].text = text

    def get_diagram_contact(self, te_name, di_name, del_mouse=False):
        pos, size = self.get_diagram_position_size(te_name, di_name)
        mouse, diagram_edge, diagram_join = self.common_control.contact_detection(pos, size, del_mouse)
        return mouse, diagram_edge, diagram_join

    #####################################################################################

    def add_territory_event(self, te_name,  key, func):  # event
        bind_id_list = []
        di_name_list = []

        for di_name in self.canvas_data.territory[te_name].diagram.keys():
            new_bind_id = self.canvas_data.canvas.tag_bind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(key), func, "+")
            bind_id_list.append(new_bind_id)
            di_name_list.append(di_name)

        self.canvas_data.territory[te_name].event[self.common_control.get_tag_name(key, func)] = [key, func, bind_id_list, di_name_list]

    def del_territory_event(self, te_name,  key, func):  # event
        bind_id = self.canvas_data.territory[te_name].event[self.common_control.get_tag_name(key, func)][2]
        di_name = self.canvas_data.territory[te_name].event[self.common_control.get_tag_name(key, func)][3]

        #print("bind", bind_id)
        for d, b in zip(di_name, bind_id):
            self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(te_name, d), "<{0}>".format(key), b)

    def all_add_territory_event(self, te_name):
        for v in self.canvas_data.territory[te_name].event.values():
            for di_name in self.canvas_data.territory[te_name].diagram.keys():
                v[2] = self.canvas_data.canvas.tag_bind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(v[0]), v[1], "+")

    def all_del_territory_event(self, te_name):  # canvasの再生成時の復元
        for bind in self.canvas_data.territory[te_name].event.values():
            for di_name, v in zip(self.canvas_data.territory[te_name].diagram.keys(), bind[2]):
                self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(bind[0]), v)

        self.canvas_data.territory[te_name].event = {}

    def get_territory_event(self, te_name):
        return self.canvas_data.territory[te_name].event

    #####################################################################################

    def add_diagram_event(self, te_name, di_name, key, func):  # event
        a = self.common_control.get_tag_name(te_name, di_name)
        bind_id = self.canvas_data.canvas.tag_bind(a, "<{0}>".format(key), func, "+")

        # print(bind_id)

        self.canvas_data.territory[te_name].diagram[di_name].event[self.common_control.get_tag_name(key, func)] = [key, func, bind_id]

    def del_diagram_event(self, te_name, di_name, key, func):  # event
        bind_name = self.common_control.get_tag_name(key, func)
        bind_id = self.canvas_data.territory[te_name].diagram[di_name].event[bind_name][2]
        self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(key), bind_id)
        #print("tag unbind")
        del self.canvas_data.territory[te_name].diagram[di_name].event[bind_name]

    def all_add_diagram_event(self, te_name, di_name):
        for k, f in zip(self.canvas_data.territory[te_name].diagram[di_name].event.keys(), self.canvas_data.territory[te_name].diagram[di_name].event.values()):
            f[2] = self.canvas_data.territory[te_name].diagram[di_name].canvas.tag_bind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(f[0]), f[1], "+")

    def all_del_diagram_event(self, te_name, di_name):  # canvasの再生成時の復元
        for k, f in zip(self.canvas_data.territory[te_name].diagram[di_name].event.keys(), self.canvas_data.territory[te_name].diagram[di_name].event.values()):
            self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(te_name, di_name), "<{0}>".format(f[0]), f[2])
            #print(self.canvas_data.territory[te_name].diagram[di_name].event[k], f)

        self.canvas_data.territory[te_name].diagram[di_name].event = {}

    def get_diagram_event(self, te_name, di_name):
        return self.canvas_data.territory[te_name].diagram[di_name].event

    #####################################################################################

    def territory_stack(self, te_name, move):
        for di_name in self.canvas_data.territory[te_name].diagram.keys():

            tag = self.common_control.get_tag_name(te_name, di_name)

            #print(tag, move)
            if move == True:
                self.canvas_data.canvas.tag_raise(tag)

            elif move == False:
                self.canvas_data.canvas.tag_lower(tag)

    def diagram_stack(self, te_name, di_name, move, target=None):
        tag = self.common_control.get_tag_name(te_name, di_name)

        if move == True and target == None:
            self.canvas_data.canvas.tag_raise(tag)
            return

        elif move == False and target == None:
            self.canvas_data.canvas.tag_lower(tag)
            return

        if move == True:
            self.canvas_data.canvas.tag_raise(tag, target)
            return

        elif move == False:
            self.canvas_data.canvas.tag_lower(tag, target)
            return

    def territory_draw(self, te_name, te_del=False):
        for k in self.canvas_data.territory[te_name].diagram.keys():
            self.diagram_draw(te_name, k, te_del)

    # def get_diagram_name(self):

    def get_diagram_type(self, te_name, di_name, data_type):
        diagram_name = str(self.canvas_data.territory[te_name].diagram[di_name].__class__.__name__)

        if diagram_name == data_type:
            return True
        else:
            return False

    def diagram_draw(self, te_name, di_name, di_del=False):
        territory_data = self.canvas_data.territory[te_name]
        diagram_data = self.canvas_data.territory[te_name].diagram[di_name]

        if di_del:
            self.canvas_data.canvas.delete(self, self.common_control.get_tag_name(te_name, di_name))
            diagram_data.draw_tag = False
            return

        if self.get_diagram_type(te_name, di_name, "DiagramData"):
            self.diagram_shape_draw(territory_data, diagram_data, te_name, di_name)

        if self.get_diagram_type(te_name, di_name, "DiagramTextData"):
            self.diagram_text_draw(territory_data, diagram_data, te_name, di_name)

        if self.get_diagram_type(te_name, di_name, "TextBoxData"):
            pass

        diagram_data.draw_tag = True
        return

    def diagram_shape_draw(self, territory_data, diagram_data, te_name, di_name):
        xy, size_xy = [0, 0], [0, 0]  # 領域基準

        color = diagram_data.color

        for i in range(2):
            if diagram_data.fill:  # 座標の計算
                xy[i] = territory_data.position[i]
                size_xy[i] = territory_data.size[i]

            else:
                xy[i] = territory_data.position[i] + diagram_data.position[i]
                size_xy[i] = diagram_data.size[i]

        print("shape", xy, size_xy, te_name, di_name)
        if diagram_data.draw_tag:
            self.canvas_data.canvas.coords(self.common_control.get_tag_name(te_name, di_name), xy[0], xy[1], size_xy[0]+xy[0], size_xy[1]+xy[1])
        if not diagram_data.draw_tag:
            self.canvas_data.canvas.create_rectangle(xy[0], xy[1], size_xy[0]+xy[0], size_xy[1]+xy[1], fill=color, outline="", width=0, tags=self.common_control.get_tag_name(te_name, di_name))  # 塗りつぶし

        diagram_data.draw_tag = True

    def diagram_text_draw(self, territory_data, diagram_data, te_name, di_name):
        xy, size_xy = [0, 0], [0, 0]  # 領域基準
        for i in range(2):
            if not diagram_data.target is None:  # ターゲットが指定さてる場合
                diagram_target = territory_data.diagram[str(diagram_data.target)]
                xy[i] = diagram_target.position[i] + territory_data.position[i] + (diagram_target.size[i] / 2)

            elif diagram_data.center[i]:  # 中心になるよう設定さてる場合
                xy[i] = diagram_data.position[i] + (diagram_data.size[i] / 2) + territory_data.position[i]

            else:  # ターゲット指定されている場合
                xy[i] = diagram_data.position[i] + territory_data.position[i]

        print("text", xy, size_xy)

        if diagram_data.draw_tag:
            _, text_size = self.get_diagram_position_size(te_name, di_name)  # 生成する時テキストは真ん中の癖に変更しようとしたら左上指定になるのでサイズを取ってきてひく
            self.canvas_data.canvas.moveto(self.common_control.get_tag_name(te_name, di_name), xy[0] - (text_size[0] / 2), xy[1] - (text_size[1] / 2))
        if not diagram_data.draw_tag:
            self.canvas_data.canvas.create_text(xy[0], xy[1], text=diagram_data.text, tags=self.common_control.get_tag_name(te_name, di_name), font=(diagram_data.font_type, diagram_data.font_size))

        diagram_data.draw_tag = True

    # def get_territory_position_size(self,te_name):
    #    position, size

    def get_diagram_position_size(self, te_name, di_name):
        pos_size = self.canvas_data.canvas.bbox(self.common_control.get_tag_name(te_name, di_name))

        position = pos_size[0], pos_size[1]
        size = pos_size[2] - pos_size[0], pos_size[3] - pos_size[1]

        return position, size


class TerritoryData:
    def __init__(self):
        self.size = [0, 0]
        self.position = [0, 0]
        self.diagram = {}
        self.event = {}

        self.blank_space = [0, 0]


class DiagramBase:  # 指定不可
    size = [0, 0]
    position = [0, 0]
    color = None
    fill = False
    draw_tag = False


class DiagramData(DiagramBase):
    def __init__(self):
        self.event = {}


class DiagramTextData(DiagramBase):
    def __init__(self):
        self.text = ""
        self.font_size = 0
        self.font_type = None
        self.center = [True, True]

        self.target = None


class TextBoxData(DiagramBase):
    def __init__(self, territory):
        self.text = ""
