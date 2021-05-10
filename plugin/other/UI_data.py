import tkinter as tk

import copy

import sys


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self,
                 window,
                 canvas_data,
                 common_control,
                 all_data,
                 all_UI_data,
                 GUI_base_color,
                 GUI_alpha_color,
                 window_event_data,
                 canvas_event_data,
                 territory_name,
                 font_data,
                 tkFont,
                 tkFont_list,
                 option_data):

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
        self.te_name = territory_name
        self.font_data = font_data

        self.tkFont = tkFont
        self.tkFont_list = tkFont_list

        self.option_data = option_data

        print("option_data", self.option_data)

        self.new_territory()

        self.operation["log"].write("UIdata生成")
        self.operation_timeline_calculation = self.operation["plugin"]["other"]["timeline_calculation"]

        self.popup_list = None

        #self.timeline_calculation = None

        # self.operation["log"].write("UI生成")

    def get_set_option_data(self, option_data=None):
        if not option_data is None:
            self.option_data = option_data
            return

        return self.option_data

    def event_not_func(self, event):
        pass

    def new_territory(self, base=None):
        if self.te_name in self.canvas_data.territory.keys():
            self.operation["error"].action(message="テリトリーネーム(UIパーツタグ): {0} は すでに使用されています".format(self.te_name))

        self.canvas_data.territory[self.te_name] = TerritoryData()
        self.operation["log"].write("テリトリー生成 {0}".format(self.te_name))

        if base != True:
            return

        self.new_diagram("base")
        self.edit_diagram_fill("base", True)
        self.edit_diagram_color("base", self.GUI_alpha_color)
        self.diagram_stack("base", False)

    def del_territory(self):
        self.territory_draw(te_del=True)

        del self.canvas_data.territory[self.te_name]

    def plus_px_frame_data(self, direction=None, debug_name=None, size_del=None):
        timeline_calculation = self.operation_timeline_calculation.TimelineCalculation(self.common_control, self.canvas_data.territory[self.te_name], self.get_set_option_data, direction=direction, debug_name=debug_name, size_del=size_del)
        return timeline_calculation

    def edit_territory_size(self, x=None, y=None):
        self.canvas_data.territory[self.te_name].size = self.common_control.xy_compilation(self.canvas_data.territory[self.te_name].size, x=x, y=y)
        return copy.deepcopy(self.canvas_data.territory[self.te_name].size)

    def edit_territory_position(self, x=None, y=None):
        self.canvas_data.territory[self.te_name].position = self.common_control.xy_compilation(self.canvas_data.territory[self.te_name].position, x=x, y=y)
        return copy.deepcopy(self.canvas_data.territory[self.te_name].position)

    def get_territory_contact(self, del_mouse=False):
        mouse, territory_edge, territory_join = self.common_control.contact_detection(self.canvas_data.territory[self.te_name].position, self.canvas_data.territory[self.te_name].size, del_mouse)

        for i in range(2):
            mouse[i] -= (self.edit_territory_position()[i] + self.canvas_data.position[0])

        return mouse, territory_edge, territory_join

    # 以下diagram

    def new_diagram(self,  di_name, diagram_type=None):

        if di_name in self.canvas_data.territory[self.te_name].diagram.keys():
            self.operation["error"].action(message="ダイアグラムネーム(UI構成タグ): {0} は すでに使用されています".format(di_name))

        if diagram_type is None:
            self.canvas_data.territory[self.te_name].diagram[di_name] = DiagramData()

        if diagram_type == "text":
            self.canvas_data.territory[self.te_name].diagram[di_name] = DiagramTextData()
            self.del_diagram("base")

        if diagram_type == "textbox":
            self.canvas_data.territory[self.te_name].diagram[di_name] = TextBoxData(self.canvas_data.canvas)
            self.del_diagram("base")

        self.operation["log"].write("ダイヤグラム生成 <テリトリー:{0}> {1}".format(self.te_name, self.canvas_data.territory[self.te_name].diagram))

    def del_diagram(self,  di_name):
        self.diagram_draw(di_name, di_del=True)
        self.operation["log"].write("ダイヤグラム削除 <テリトリー:{0}> {1}".format(self.te_name, di_name))
        del self.canvas_data.territory[self.te_name].diagram[di_name]

    def edit_diagram_size(self,  di_name, x=None, y=None):
        self.canvas_data.territory[self.te_name].diagram[di_name].size = self.common_control.xy_compilation(self.canvas_data.territory[self.te_name].diagram[di_name].size, x=x, y=y)

        return copy.deepcopy(self.canvas_data.territory[self.te_name].diagram[di_name].size)

    def edit_diagram_position(self,  di_name, x=None, y=None):
        self.canvas_data.territory[self.te_name].diagram[di_name].position = self.common_control.xy_compilation(self.canvas_data.territory[self.te_name].diagram[di_name].position, x=x, y=y)

        return copy.deepcopy(self.canvas_data.territory[self.te_name].diagram[di_name].position)

    def edit_diagram_fill(self,  di_name, select, direction=None):

        if select != True and select != False:
            self.operation["error"].action(message="TrueとFalse以外入れるな")

        if direction is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].fill = [select, select]
            return

        self.canvas_data.territory[self.te_name].diagram[di_name].fill[direction] = select

    def edit_diagram_color(self,  di_name, color=None):
        if color is None or not color[0] == "#":
            color = self.GUI_alpha_color

        self.canvas_data.territory[self.te_name].diagram[di_name].color = color

    def get_diagram_contact(self,  di_name, del_mouse=False):
        pos, size = self.get_diagram_position_size(di_name)
        mouse, diagram_edge, diagram_join = self.common_control.contact_detection(pos, size, del_mouse)

        for i in range(2):
            mouse[i] -= (self.edit_territory_position()[i] + self.canvas_data.position[i])

        return mouse, diagram_edge, diagram_join

    #####################################################################################

    def add_territory_event(self,   key, func):  # event
        bind_id_list = []
        di_name_list = []

        for di_name in self.canvas_data.territory[self.te_name].diagram.keys():
            new_bind_id = self.canvas_data.canvas.tag_bind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(key), func, "+")
            bind_id_list.append(new_bind_id)
            di_name_list.append(di_name)

        self.canvas_data.territory[self.te_name].event[self.common_control.get_tag_name(key, func)] = [key, func, bind_id_list, di_name_list]

    def del_territory_event(self,   key, func):  # event
        bind_id = self.canvas_data.territory[self.te_name].event[self.common_control.get_tag_name(key, func)][2]
        di_name = self.canvas_data.territory[self.te_name].event[self.common_control.get_tag_name(key, func)][3]

        # self.operation["log"].write("bind", bind_id)
        for d, b in zip(di_name, bind_id):
            self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(d), "<{0}>".format(key), b)

    def all_add_territory_event(self, te_name):
        for v in self.canvas_data.territory[self.te_name].event.values():
            for di_name in self.canvas_data.territory[self.te_name].diagram.keys():
                v[2] = self.canvas_data.canvas.tag_bind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(v[0]), v[1], "+")

    def all_del_territory_event(self, te_name):  # canvasの再生成時の復元
        for bind in self.canvas_data.territory[self.te_name].event.values():
            for di_name, v in zip(self.canvas_data.territory[self.te_name].diagram.keys(), bind[2]):
                self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(bind[0]), v)

        self.canvas_data.territory[self.te_name].event = {}

    def get_territory_event(self, te_name):
        return self.canvas_data.territory[self.te_name].event

    #####################################################################################

    def add_diagram_event(self,  di_name, key, func):  # event
        a = self.common_control.get_tag_name(self.te_name, di_name)
        bind_id = self.canvas_data.canvas.tag_bind(a, "<{0}>".format(key), func, "+")

        # self.operation["log"].write(bind_id)

        self.canvas_data.territory[self.te_name].diagram[di_name].event[self.common_control.get_tag_name(key, func)] = [key, func, bind_id]

    def del_diagram_event(self,  di_name, key, func):  # event
        bind_name = self.common_control.get_tag_name(key, func)
        bind_id = self.canvas_data.territory[self.te_name].diagram[di_name].event[bind_name][2]
        self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(key), bind_id)
        # self.operation["log"].write("tag unbind")
        del self.canvas_data.territory[self.te_name].diagram[di_name].event[bind_name]

    def all_add_diagram_event(self,  di_name):
        for k, f in zip(self.canvas_data.territory[self.te_name].diagram[di_name].event.keys(), self.canvas_data.territory[self.te_name].diagram[di_name].event.values()):
            f[2] = self.canvas_data.territory[self.te_name].diagram[di_name].canvas.tag_bind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(f[0]), f[1], "+")

    def all_del_diagram_event(self,  di_name):  # canvasの再生成時の復元
        for k, f in zip(self.canvas_data.territory[self.te_name].diagram[di_name].event.keys(), self.canvas_data.territory[self.te_name].diagram[di_name].event.values()):
            self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(f[0]), f[2])
            # self.operation["log"].write(self.canvas_data.territory[self.te_name].diagram[di_name].event[k], f)

        self.canvas_data.territory[self.te_name].diagram[di_name].event = {}

    def get_diagram_event(self,  di_name):

        return self.canvas_data.territory[self.te_name].diagram[di_name].event

    #####################################################################################

    def territory_stack(self,  move):
        for di_name in self.canvas_data.territory[self.te_name].diagram.keys():

            tag = self.common_control.get_tag_name(self.te_name, di_name)

            # self.operation["log"].write(tag, move)
            if move == True:
                self.canvas_data.canvas.tag_raise(tag)

            elif move == False:
                self.canvas_data.canvas.tag_lower(tag)

    def diagram_stack(self,  di_name, move, target=None):
        tag = self.common_control.get_tag_name(self.te_name, di_name)

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

    def territory_draw(self,  te_del=False):
        for d in self.canvas_data.territory[self.te_name].diagram.keys():
            self.diagram_draw(d, te_del)

    def get_diagram_type(self,  di_name, data_type):
        diagram_name = str(self.canvas_data.territory[self.te_name].diagram[di_name].__class__.__name__)

        if diagram_name == data_type:
            return True
        else:
            return False

    def diagram_draw(self,  di_name, di_del=False):
        territory_data = self.canvas_data.territory[self.te_name]
        diagram_data = self.canvas_data.territory[self.te_name].diagram[di_name]

        if di_del:
            self.canvas_data.canvas.delete(self, self.common_control.get_tag_name(self.te_name, di_name))
            diagram_data.draw_tag = False
            return

        if self.get_diagram_type(di_name, "DiagramData"):
            self.__diagram_shape_draw(territory_data, diagram_data,  di_name)

        if self.get_diagram_type(di_name, "DiagramTextData"):
            self.__diagram_text_draw(territory_data, diagram_data,  di_name)

        if self.get_diagram_type(di_name, "TextBoxData"):
            self.__diagram_textbox_draw(territory_data, diagram_data,  di_name)

        diagram_data.draw_tag = True
        return

    def __diagram_shape_draw(self, territory_data, diagram_data,  di_name):

        color = diagram_data.color

        xy, size_xy = self.__left_coordinate_calculation(territory_data, diagram_data)

        self.operation["log"].write("shape", xy, size_xy,  di_name)
        if diagram_data.draw_tag:
            self.canvas_data.canvas.itemconfigure(self.common_control.get_tag_name(self.te_name, di_name), fill=color)
            self.canvas_data.canvas.coords(self.common_control.get_tag_name(self.te_name, di_name), xy[0], xy[1], size_xy[0]+xy[0], size_xy[1]+xy[1])

            #print(xy, size_xy)

        if not diagram_data.draw_tag:
            self.canvas_data.canvas.create_rectangle(xy[0], xy[1], size_xy[0]+xy[0], size_xy[1]+xy[1], fill=color, outline="", width=0, tags=self.common_control.get_tag_name(self.te_name, di_name))  # 塗りつぶし

    def __diagram_text_draw(self, territory_data, diagram_data,  di_name):

        xy = self.__center_target_calculation(territory_data, diagram_data,  di_name)

        self.operation["log"].write("text", xy, diagram_data.text)

        if diagram_data.draw_tag:
            old_text_len = self.canvas_data.canvas.index(self.common_control.get_tag_name(self.te_name, di_name), tk.END)  # 文字数の長さを取得
            self.operation["log"].write(old_text_len)
            self.canvas_data.canvas.dchars(self.common_control.get_tag_name(self.te_name, di_name), 0, old_text_len - 1)
            self.canvas_data.canvas.insert(self.common_control.get_tag_name(self.te_name, di_name), 0, diagram_data.text)

        if not diagram_data.draw_tag:
            self.canvas_data.canvas.create_text(0, 0, text="new", tags=self.common_control.get_tag_name(self.te_name, di_name))

        self.canvas_data.canvas.itemconfigure(self.common_control.get_tag_name(self.te_name, di_name), text=diagram_data.text, font=(diagram_data.font_type, diagram_data.font_size))

        if diagram_data.anchor == 1:
            text_xy, text_size = self.get_diagram_position_size(di_name)

            xy[0] -= text_size[0] / 2
            xy[1] -= diagram_data.font_size / 2

        #print("テキスト最終座標", xy[1], text_size)

        self.canvas_data.canvas.moveto(self.common_control.get_tag_name(self.te_name, di_name), xy[0], xy[1])

    def __diagram_textbox_draw(self, territory_data, diagram_data,  di_name):
        print(territory_data.position, diagram_data.position)
        xy, size_xy = self.__left_coordinate_calculation(territory_data, diagram_data)

        self.operation["log"].write_func_list(self.canvas_data.territory[self.te_name].diagram[di_name].entry.place)

        #print("テキストボックス決定座標", xy, size_xy)

        self.canvas_data.territory[self.te_name].diagram[di_name].entry.place(
            x=xy[0],
            y=xy[1],
            width=size_xy[0],
            height=size_xy[1])

    def __left_coordinate_calculation(self, territory_data, diagram_data):

        xy, size_xy = [0, 0], [0, 0]  # 領域基準
        for i in range(2):
            if diagram_data.fill[i]:
                xy[i] = territory_data.position[i]
                size_xy[i] = territory_data.size[i]

            else:
                xy[i] = territory_data.position[i] + diagram_data.position[i]
                size_xy[i] = diagram_data.size[i]

        return xy, size_xy

    def __center_target_calculatin(self, territory_data, diagram_data,  di_name):
        xy = [0, 0]  # 領域基準
        for i in range(2):
            if not diagram_data.target is None:  # ターゲットが指定さてる場合
                diagram_target = copy.deepcopy(territory_data.diagram[str(diagram_data.target)])
                if diagram_target.fill[i]:
                    diagram_target.size[i] = territory_data.size[i]

                xy[i] = diagram_target.position[i] + (diagram_target.size[i] / 2) + territory_data.position[i]

            elif diagram_data.center[i]:  # テリトリーの中心になるよう設定さてる場合
                xy[i] = territory_data.position[i] + (territory_data.size[i] / 2)
            else:  # 普通の指定
                xy[i] = (diagram_data.size[i] / 2) + diagram_data.position[i] + territory_data.position[i]

        return xy

    def get_diagram_position_size(self,  di_name):
        pos_size = self.canvas_data.canvas.bbox(self.common_control.get_tag_name(self.te_name, di_name))

        position = pos_size[0], pos_size[1]
        size = pos_size[2] - pos_size[0], pos_size[3] - pos_size[1]

        return position, size

    def tk_font_inquiry(self, font_name):
        if not font_name in self.tkFont_list:
            print("font: {0} は 使用できません".format(font_name))

        return font_name

    def popup_set(self, send):
        if not send is None:
            self.popup_list = send

    def edit_diagram_text(self,
                          di_name,
                          text=None,
                          font_size=None,
                          font_type=None,
                          x_center=None,
                          y_center=None,
                          center=None,
                          target=None,
                          anchor=None):

        if not self.get_diagram_type(di_name, "DiagramTextData"):
            self.operation["error"].action(message="これテキスト用じゃないぞ")

        if not text is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].text = str(text)
        if not font_size is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].font_size = font_size
        if not font_type is None:
            self.tk_font_inquiry(font_type)
            self.canvas_data.territory[self.te_name].diagram[di_name].font_type = font_type
        if not x_center is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].center[0] = x_center
        if not y_center is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].center[1] = y_center
        if not center is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].center = [center, center]
        if not target is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].target = target
        if not anchor is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].anchor = anchor


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
    fill = [False, False]
    draw_tag = False
    event = {}


class DiagramData(DiagramBase):
    def __init__(self):
        pass


class DiagramTextData(DiagramBase):
    def __init__(self):
        self.text = ""
        self.font_size = 0
        self.font_type = None
        self.center = [False, False]

        self.target = None
        self.anchor = 1

        # 配置可能なスペースに余裕がある場合、Widget をどこに配置するか指定します。
        # デフォルトは Tk.CENTER. そのほかに、Tk.W (左よせ）、Tk.E （右よせ）、Tk.N （上よせ）、Tk.S （下よせ）、 Tk.NW （左上）、Tk.SW （左下）、Tk.NE （右上）、Tk.SE （右下）
        # must be n, ne, e, se, s, sw, w, nw, or center

        #self.old_text_len = 0


class TextBoxData(DiagramBase):
    def __init__(self, canvas):
        self.text = ""
        self.font_size = 0
        self.target = None
        self.center = [False, False]
        self.entry = tk.Entry(canvas, highlightthickness=0, relief="flat")
