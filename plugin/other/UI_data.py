import tkinter as tk

import copy
import inspect
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
                 tkFont_list):

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

        self.new_territory()

        print("クラスが生成されました")

        # print("UI生成")

    def event_not_func(self, event):
        print("テストイベント")

    def new_territory(self):
        if self.te_name in self.canvas_data.territory.keys():
            self.operation["error"].action(message="テリトリーネーム(UIパーツタグ): {0} は すでに使用されています".format(self.te_name))

        self.canvas_data.territory[self.te_name] = TerritoryData()
        print("テリトリー生成 {0}".format(self.te_name))

        print(self.canvas_data.territory)

        self.new_diagram("base")
        self.edit_diagram_fill("base", True)
        self.edit_diagram_color("base", "#000000")

    def del_territory(self):
        self.territory_draw(te_del=True)

        del self.canvas_data.territory[self.te_name]

    def edit_territory_size(self, x=None, y=None):
        self.canvas_data.territory[self.te_name].size = self.common_control.xy_compilation(self.canvas_data.territory[self.te_name].size, x=x, y=y)
        return copy.deepcopy(self.canvas_data.territory[self.te_name].size)

    def edit_territory_position(self, x=None, y=None):
        self.canvas_data.territory[self.te_name].position = self.common_control.xy_compilation(self.canvas_data.territory[self.te_name].position, x=x, y=y)
        print(self.canvas_data.territory)
        return copy.deepcopy(self.canvas_data.territory[self.te_name].position)

    def get_territory_contact(self, del_mouse=False):
        mouse, territory_edge, territory_join = self.common_control.contact_detection(self.canvas_data.territory[self.te_name].position, self.canvas_data.territory[self.te_name].size, del_mouse)
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

        print("ダイヤグラム生成 <テリトリー:{0}> {1}".format(self.te_name, self.canvas_data.territory[self.te_name].diagram))

    def del_diagram(self,  di_name):
        self.diagram_draw(di_name, di_del=True)
        print("ダイヤグラム削除 <テリトリー:{0}> {1}".format(self.te_name, di_name))
        del self.canvas_data.territory[self.te_name].diagram[di_name]

    def edit_diagram_size(self,  di_name, x=None, y=None):
        self.canvas_data.territory[self.te_name].diagram[di_name].size = self.common_control.xy_compilation(self.canvas_data.territory[self.te_name].diagram[di_name].size, x=x, y=y)

        return copy.deepcopy(self.canvas_data.territory[self.te_name].diagram[di_name].size)

    def edit_diagram_position(self,  di_name, x=None, y=None):
        print(self.canvas_data.territory["i"].diagram["view"].position, "c")
        print(self.te_name, di_name)
        self.canvas_data.territory[self.te_name].diagram[di_name].position = self.common_control.xy_compilation(self.canvas_data.territory[self.te_name].diagram[di_name].position, x=x, y=y)
        print(self.canvas_data.territory["i"].diagram["view"].position, "d")
        # print(self.canvas_data.territory["textbox"].diagram["view"].position)

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

        # print("bind", bind_id)
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

        # print(bind_id)

        self.canvas_data.territory[self.te_name].diagram[di_name].event[self.common_control.get_tag_name(key, func)] = [key, func, bind_id]

    def del_diagram_event(self,  di_name, key, func):  # event
        bind_name = self.common_control.get_tag_name(key, func)
        bind_id = self.canvas_data.territory[self.te_name].diagram[di_name].event[bind_name][2]
        self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(key), bind_id)
        # print("tag unbind")
        del self.canvas_data.territory[self.te_name].diagram[di_name].event[bind_name]

    def all_add_diagram_event(self,  di_name):
        for k, f in zip(self.canvas_data.territory[self.te_name].diagram[di_name].event.keys(), self.canvas_data.territory[self.te_name].diagram[di_name].event.values()):
            f[2] = self.canvas_data.territory[self.te_name].diagram[di_name].canvas.tag_bind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(f[0]), f[1], "+")

    def all_del_diagram_event(self,  di_name):  # canvasの再生成時の復元
        for k, f in zip(self.canvas_data.territory[self.te_name].diagram[di_name].event.keys(), self.canvas_data.territory[self.te_name].diagram[di_name].event.values()):
            self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(self.te_name, di_name), "<{0}>".format(f[0]), f[2])
            # print(self.canvas_data.territory[self.te_name].diagram[di_name].event[k], f)

        self.canvas_data.territory[self.te_name].diagram[di_name].event = {}

    def get_diagram_event(self,  di_name):
        return self.canvas_data.territory[self.te_name].diagram[di_name].event

    #####################################################################################

    def territory_stack(self,  move):
        for di_name in self.canvas_data.territory[self.te_name].diagram.keys():

            tag = self.common_control.get_tag_name(self.te_name, di_name)

            # print(tag, move)
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
        for k in self.canvas_data.territory[self.te_name].diagram.keys():
            self.diagram_draw(k, te_del)

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
        xy, size_xy = [0, 0], [0, 0]  # 領域基準

        color = diagram_data.color

        for i in range(2):
            if not False in diagram_data.fill:  # 座標の計算
                xy[i] = territory_data.position[i]
                size_xy[i] = territory_data.size[i]

            elif diagram_data.fill[i]:
                xy[i] = territory_data.position[i]
                size_xy[i] = territory_data.size[i]

            else:
                xy[i] = territory_data.position[i] + diagram_data.position[i]
                size_xy[i] = diagram_data.size[i]

        print("shape", xy, size_xy,  di_name)
        if diagram_data.draw_tag:
            self.canvas_data.canvas.coords(self.common_control.get_tag_name(self.te_name, di_name), xy[0], xy[1], size_xy[0]+xy[0], size_xy[1]+xy[1])

        if not diagram_data.draw_tag:
            self.canvas_data.canvas.create_rectangle(xy[0], xy[1], size_xy[0]+xy[0], size_xy[1]+xy[1], fill=color, outline="", width=0, tags=self.common_control.get_tag_name(self.te_name, di_name))  # 塗りつぶし

    def __diagram_text_draw(self, territory_data, diagram_data,  di_name):

        xy = self.__center_target_calculation(territory_data, diagram_data,  di_name)

        print("text", xy, diagram_data.text)

        if diagram_data.draw_tag:
            old_text_len = self.canvas_data.canvas.index(self.common_control.get_tag_name(self.te_name, di_name), tk.END)  # 文字数の長さを取得
            print(old_text_len)
            self.canvas_data.canvas.dchars(self.common_control.get_tag_name(self.te_name, di_name), 0, old_text_len - 1)
            self.canvas_data.canvas.insert(self.common_control.get_tag_name(self.te_name, di_name), 0, diagram_data.text)

        if not diagram_data.draw_tag:
            self.canvas_data.canvas.create_text(0, 0, text="new", tags=self.common_control.get_tag_name(self.te_name, di_name))

        self.canvas_data.canvas.itemconfigure(self.common_control.get_tag_name(self.te_name, di_name), text=diagram_data.text, font=(diagram_data.font_type, diagram_data.font_size))
        _, text_size = self.get_diagram_position_size(di_name)  # 生成する時テキストは真ん中の癖に変更しようとしたら左上指定になるのでサイズを取ってきてひく

        if 0 in text_size:
            return

        xy_l = [xy - (ts/2) for xy, ts in zip(xy, text_size)]
        print("テキスト最終位置", xy_l)
        self.canvas_data.canvas.moveto(self.common_control.get_tag_name(self.te_name, di_name), xy_l[0], xy_l[1])

    def __diagram_textbox_draw(self, territory_data, diagram_data,  di_name):
        xy = self.__center_target_calculation(territory_data, diagram_data,  di_name)

        if diagram_data.draw_tag:
            pass
            print("すでに生成済み:textbox")

        if not diagram_data.draw_tag:

            size = round(diagram_data.size[0] / 10)

            if diagram_data.fill[0]:
                print("テリトリー引継ぎ")

            #size = round(size/10)

            print("entry情報", xy, size)
            print("初回:textbox")

            entry = self.tk.Entry(self.canvas_data.canvas, width=size, highlightthickness=0, relief="flat")
            self.canvas_data.canvas.create_window(0, 0, tags=self.common_control.get_tag_name(self.te_name, di_name), window=entry)

        _, obj_size = self.get_diagram_position_size(di_name)  # 生成する時テキストは真ん中の癖に変更しようとしたら左上指定になるのでサイズを取ってきてひく
        xy_l = [xy + (ob/2) for xy, ob in zip(xy, obj_size)]

        print("テキストボックス決定値 : ", xy_l, obj_size)

        self.canvas_data.canvas.moveto(self.common_control.get_tag_name(self.te_name, di_name), xy_l[0], xy_l[1])

    def __center_target_calculation(self, territory_data, diagram_data,  di_name):
        xy = [0, 0]  # 領域基準
        for i in range(2):

            if not diagram_data.target is None:  # ターゲットが指定さてる場合
                diagram_target = copy.deepcopy(territory_data.diagram[str(diagram_data.target)])
                if diagram_target.fill[i]:
                    diagram_target.size[i] = territory_data.size[i]

                xy[i] = diagram_target.position[i] + (diagram_target.size[i] / 2) + territory_data.position[i]
                print(diagram_target.position[i], diagram_target.size[i], territory_data.position[i])
                print("ターゲット指定")

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

    def edit_diagram_text(self,
                          di_name,
                          text=None,
                          font_size=None,
                          font_type=None,
                          x_center=None,
                          y_center=None,
                          center=None,
                          target=None):

        if not self.get_diagram_type(di_name, "DiagramTextData"):
            self.operation["error"].action(message="これテキスト用じゃないぞ")

        if not text is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].text = text
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


class DiagramData(DiagramBase):
    def __init__(self):
        self.event = {}


class DiagramTextData(DiagramBase):
    def __init__(self):
        self.text = ""
        self.font_size = 0
        self.font_type = None
        self.center = [False, False]

        self.target = None

        #self.old_text_len = 0


class TextBoxData(DiagramBase):
    def __init__(self, territory):
        self.text = ""
        self.font_size = 0
        self.target = None
        self.center = [False, False]
