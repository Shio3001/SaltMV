
import tkinter as tk
import copy
import sys
import inspect
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import uuid
from tkinter import filedialog


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self,
                 window,
                 canvas_data,
                 common_control,
                 edit_control_auxiliary,
                 UI_control,
                 GUI_base_color,
                 GUI_alpha_color,
                 window_event_data,
                 canvas_event_data,
                 territory_name,
                 font_data,
                 tkFont,
                 tkFont_list,
                 base,
                 option_data,
                 get_window_contact,
                 get_window_view_flag):

        self.get_window_contact = get_window_contact

        self.window = window
        self.canvas_data = canvas_data
        self.edit_control_auxiliary = edit_control_auxiliary
        self.operation = edit_control_auxiliary.operation
        self.UI_control = UI_control
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

        if option_data is None:
            option_data = {}

        self.option_data = option_data

        self.base = base

        # print("option_data", self.option_data)

        self.new_territory()

        self.operation["log"].write("UIdata生成")
        self.operation_timeline_calculation = self.operation["plugin"]["other"]["timeline_calculation"]

        self.uidata_id = self.edit_control_auxiliary.elements.make_id("ui_data")

        self.callback_operation = self.operation["plugin"]["other"]["callback"].CallBack()

        self.image_tk = None
        self.get_window_view_flag = get_window_view_flag

        # print(self.uidata_id, "生成しました＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊")

        # self.popup_list = None

        # self.timeline_calculation = None

        # self.operation["log"].write("UI生成")

    def make_id(self, memo):
        now_time = datetime.datetime.now()
        # new_id =
        new_id = "u"+str(uuid.uuid1()) + "t" + now_time.strftime('%y%m%H%M%S%f') + "UI_auxiliary" + str(memo)
        return copy.deepcopy(new_id)

    def event_not_func(self, event):
        pass

    # def get_set_option_data(self, option_data=None):
    #     if not option_data is None:
    #         self.option_data = option_data
    #         return

    #     return self.option_data

    def get_set_option_data(self, option_data=None, overwrite=None):
        if option_data is None:
            return self.option_data

        if not option_data is None and overwrite:
            self.option_data = option_data
            return

        elif not option_data is None:
            self.option_data.update(option_data)
            return

    def new_territory(self):
        # print("呼び出し先", inspect.stack()[1].function)
        # print("テリトリー生成", self.canvas_data.territory)
        if self.te_name in self.canvas_data.territory.keys():
            self.operation["error"].action(message="テリトリーネーム(UIパーツタグ): {0} は すでに使用されています".format(self.te_name))

        self.canvas_data.territory[self.te_name] = TerritoryData()
        self.operation["log"].write("テリトリー生成 {0}".format(self.te_name))

        if self.base != True:
            return

        self.new_diagram("base")
        self.edit_diagram_fill("base", True)
        self.edit_diagram_color("base", self.GUI_alpha_color)
        self.diagram_stack("base", False)

    def del_territory(self):
        self.territory_draw(te_del=True)
        self.all_del_territory_event()

        del self.canvas_data.territory[self.te_name]
        # for di_name in self.canvas_data.territory[self.te_name].diagram.keys():
        #    self.all_del_diagram_event(di_name)

    def plus_px_frame_data(self, direction=None, debug_name=None, size_del=None):
        send_callback_operation = self.operation["plugin"]["other"]["callback"].CallBack()
        timeline_calculation = self.operation_timeline_calculation.TimelineCalculation(
            self.common_control, send_callback_operation, self.canvas_data.territory[self.te_name], self.get_set_option_data, direction=direction, debug_name=debug_name, size_del=size_del)
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

        window_view_flag = self.get_window_view_flag()
        if not window_view_flag:
            return

        if di_name in self.canvas_data.territory[self.te_name].diagram.keys():
            self.operation["error"].action(message="ダイアグラムネーム(UI構成タグ): {0} は すでに使用されています".format(di_name))

        if diagram_type is None:
            self.canvas_data.territory[self.te_name].diagram[di_name] = DiagramData()

        if diagram_type == "TkImage":
            self.canvas_data.territory[self.te_name].diagram[di_name] = TkImageData()
            self.del_diagram("base")

        # if diagram_type == "MatplotlibImage":
        #    self.canvas_data.territory[self.te_name].diagram[di_name] = MatplotlibImageData()
        #    self.del_diagram("base")

        if diagram_type == "text":
            self.canvas_data.territory[self.te_name].diagram[di_name] = DiagramTextData(self.canvas_data.canvas)
            self.del_diagram("base")

        if diagram_type == "textbox":
            self.canvas_data.territory[self.te_name].diagram[di_name] = TextBoxData(self.canvas_data.canvas)
            self.del_diagram("base")

        # self.canvas_data.territory[self.te_name].diagram[di_name].event = {}

        # print("new_diagram_event", self.canvas_data.territory[self.te_name].diagram[di_name].event)

        self.operation["log"].write("ダイヤグラム生成 <テリトリー:{0}> {1}".format(self.te_name, self.canvas_data.territory[self.te_name].diagram))

    def del_diagram(self,  di_name):
        if not di_name in self.canvas_data.territory[self.te_name].diagram:
            return

        self.all_del_diagram_event(di_name)

        self.diagram_draw(di_name, di_del=True)
        self.operation["log"].write("ダイヤグラム削除 <テリトリー:{0}> {1}".format(self.uidata_id, self.te_name, di_name))
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

    def edit_diagram_width(self,  di_name, width, outline=None):
        self.canvas_data.territory[self.te_name].diagram[di_name].width = width

        if not outline is None and outline[0] == "#":
            self.canvas_data.territory[self.te_name].diagram[di_name].outline = outline

        self.canvas_data.canvas.itemconfigure(self.canvas_data.territory[self.te_name].diagram[di_name].tag, width=self.canvas_data.territory[self.te_name].diagram[di_name].width, outline=self.canvas_data.territory[self.te_name].diagram[di_name].outline)

    def edit_diagram_color(self,  di_name, color=None):
        if not self.get_diagram_type(di_name, "DiagramData") and not self.get_diagram_type(di_name, "DiagramTextData"):
            return

        if color is None or not color[0] == "#":
            color = copy.deepcopy(self.GUI_alpha_color)

        self.canvas_data.territory[self.te_name].diagram[di_name].color = color
        self.canvas_data.canvas.itemconfigure(self.canvas_data.territory[self.te_name].diagram[di_name].tag, fill=self.canvas_data.territory[self.te_name].diagram[di_name].color)

    def get_diagram_contact(self,  di_name, del_mouse=False):
        pos, size = self.get_diagram_position_size(di_name)
        mouse, diagram_edge, diagram_join = self.common_control.contact_detection(pos, size, del_mouse)

        for i in range(2):
            mouse[i] -= (self.edit_territory_position()[i] + self.canvas_data.position[i])

        return mouse, diagram_edge, diagram_join

    ###########

    def add_territory_event(self,   key, func):  # event
        bind_id_list = []
        di_name_list = []

        for di_name in self.canvas_data.territory[self.te_name].diagram.keys():
            new_bind_id = self.canvas_data.canvas.tag_bind(self.canvas_data.territory[self.te_name].diagram[di_name].tag, "<{0}>".format(key), func, "+")
            bind_id_list.append(new_bind_id)
            di_name_list.append(di_name)

        self.canvas_data.territory[self.te_name].event[self.common_control.get_tag_name(key, func)] = [key, func, bind_id_list, di_name_list]

    def del_territory_event(self,   key, func):  # event
        bind_id = self.canvas_data.territory[self.te_name].event[self.common_control.get_tag_name(key, func)][2]
        di_name = self.canvas_data.territory[self.te_name].event[self.common_control.get_tag_name(key, func)][3]

        # self.operation["log"].write("bind", bind_id)
        for d, b in zip(di_name, bind_id):
            self.canvas_data.canvas.tag_unbind(self.common_control.get_tag_name(d), "<{0}>".format(key), b)

    def all_add_territory_event(self):
        for v in self.canvas_data.territory[self.te_name].event.values():
            for di_name in self.canvas_data.territory[self.te_name].diagram.keys():
                v[2] = self.canvas_data.canvas.tag_bind(self.canvas_data.territory[self.te_name].diagram[di_name].tag, "<{0}>".format(v[0]), v[1], "+")

    def all_del_territory_event(self):  # canvasの再生成時の復元
        for bind in self.canvas_data.territory[self.te_name].event.values():
            for di_name, v in zip(self.canvas_data.territory[self.te_name].diagram.keys(), bind[2]):
                self.canvas_data.canvas.tag_unbind(self.canvas_data.territory[self.te_name].diagram[di_name].tag, "<{0}>".format(bind[0]), v)

        self.canvas_data.territory[self.te_name].event = {}

    def get_territory_event(self):
        return self.canvas_data.territory[self.te_name].event

    ###########

    # self.canvas_data.territory[self.te_name].diagram[di_name].function

    def add_diagram_event(self,  di_name, key, func):  # event

        print(key, func)

        tag = self.canvas_data.territory[self.te_name].diagram[di_name].tag
        bind_id = self.canvas_data.canvas.tag_bind(tag, "<{0}>".format(key), func, "+")

        # ##print(self.canvas_data.territory)

        # print("テリトリーの数", len(self.canvas_data.territory))

        self.canvas_data.territory[self.te_name].diagram[di_name].event[self.common_control.get_tag_name(key, func)] = [copy.deepcopy(key), func, copy.deepcopy(bind_id), copy.deepcopy(tag)]
        # print("追加事項", self.canvas_data.territory[self.te_name].diagram[di_name].event[self.common_control.get_tag_name(key, func)])

    def del_diagram_event(self,  di_name, key, func):  # event
        bind_name = self.common_control.get_tag_name(key, func)
        bind_id = self.canvas_data.territory[self.te_name].diagram[di_name].event[bind_name][2]
        self.canvas_data.canvas.tag_unbind(self.canvas_data.territory[self.te_name].diagram[di_name].tag, "<{0}>".format(key), bind_id)

        # print(bind_id, self.uidata_id, self.te_name, di_name)
        # ##print(self.canvas_data.territory[self.te_name].diagram[di_name].event)
        # self.operation["log"].write("tag unbind")
        del self.canvas_data.territory[self.te_name].diagram[di_name].event[bind_name]

    # def all_add_diagram_event(self,  di_name):
    #    for k, f in zip(self.canvas_data.territory[self.te_name].diagram[di_name].event.keys(), self.canvas_data.territory[self.te_name].diagram[di_name].event.values()):
    #        f[2] = self.canvas_data.territory[self.te_name].diagram[di_name].canvas.tag_bind(self.canvas_data.territory[self.te_name].diagram[di_name].tag, "<{0}>".format(f[0]), f[1], "+")

    def all_del_diagram_event(self,  di_name):  # canvasの再生成時の復元
        # #print(self.canvas_data.territory[self.te_name].diagram[di_name].event)
        for f in self.canvas_data.territory[self.te_name].diagram[di_name].event.values():
            # #print(f)
            self.canvas_data.canvas.tag_unbind(f[3], "<{0}>".format(f[0]), f[2])
        # print("削除物", self.uidata_id, self.te_name, di_name)
        self.canvas_data.territory[self.te_name].diagram[di_name].event = {}

    def get_diagram_event(self,  di_name):

        return self.canvas_data.territory[self.te_name].diagram[di_name].event

    ###########

    def territory_stack(self,  move):
        for di_name in self.canvas_data.territory[self.te_name].diagram.keys():
            tag = self.canvas_data.territory[self.te_name].diagram[di_name].tag

            # self.operation["log"].write(tag, move)
            if move == True:
                self.canvas_data.canvas.tag_raise(tag)

            elif move == False:
                self.canvas_data.canvas.tag_lower(tag)

    def diagram_stack(self,  di_name, move, target=None):
        tag = self.canvas_data.territory[self.te_name].diagram[di_name].tag

        # print("diagram_stack 変更")

        if move == True and target == None:
            self.canvas_data.canvas.tag_raise(tag)
            return

        elif move == False and target == None:
            self.canvas_data.canvas.tag_lower(tag)
            return

        target_tag = self.canvas_data.territory[self.te_name].diagram[target].tag

        if move == True:
            self.canvas_data.canvas.tag_raise(tag, target_tag)
            return

        elif move == False:
            self.canvas_data.canvas.tag_lower(tag, target_tag)
            return

    def territory_draw(self,  te_del=False):

        if not self.te_name in self.canvas_data.territory.keys():
            return

        for d in self.canvas_data.territory[self.te_name].diagram.keys():
            # print("territory_draw", self.te_name, te_del)
            self.diagram_draw(d, te_del)

    def get_diagram_type(self,  di_name, data_type):
        diagram_name = str(self.canvas_data.territory[self.te_name].diagram[di_name].__class__.__name__)

        if diagram_name == data_type:
            return True
        else:
            return False

    def set_shape_rhombus(self, di_name, size, center_x, center_y):  # ひし形
        if not self.get_diagram_type(di_name, "DiagramData"):
            return

        shape_point = [center_x - size/2,
                       center_y,
                       center_x,
                       center_y - size/2,
                       center_x + size/2,
                       center_y,
                       center_x,
                       center_y + size/2
                       ]

        self.canvas_data.territory[self.te_name].diagram[di_name].shape_point = shape_point

        return copy.deepcopy(self.canvas_data.territory[self.te_name].diagram[di_name].shape_point)

    def set_shape_point(self, di_name, shape_point, del_point=None, plus=None):
        if not self.get_diagram_type(di_name, "DiagramData"):
            return

        if del_point:
            self.canvas_data.territory[self.te_name].diagram[di_name].shape_point = None
            return

        if int(len(shape_point)) % 2 == 0:
            # 偶数個ではないので設定不可
            return

        if plus:
            self.canvas_data.territory[self.te_name].diagram[di_name].shape_point.append(shape_point)
        else:
            self.canvas_data.territory[self.te_name].diagram[di_name].shape_point = copy.deepcopy(shape_point)

        return copy.deepcopy(self.canvas_data.territory[self.te_name].diagram[di_name].shape_point)

    # tkinter.NORMAL：通常状態
    # tkinter.DISABLED：無効状態（マウスイベント発生しない）
    # tkinter.HIDDEN：非表示状態（画面に表示されない）

    # def diagram_draw_temp_del(slef, di_name):
    #    self.canvas_data.canvas(state=state)

    def diagram_draw(self,  di_name, di_del=False, image_tk=None):

        territory_data = self.canvas_data.territory[self.te_name]
        diagram_data = self.canvas_data.territory[self.te_name].diagram[di_name]

        if self.get_diagram_type(di_name, "DiagramData"):
            self.__diagram_shape_draw(territory_data, diagram_data,  di_name, di_del)

        if self.get_diagram_type(di_name, "DiagramTextData"):
            self.__diagram_text_draw(territory_data, diagram_data,  di_name, di_del)

        if self.get_diagram_type(di_name, "TextBoxData"):
            self.__diagram_textbox_draw(territory_data, diagram_data,  di_name, di_del, diagram_data.forget)

        if self.get_diagram_type(di_name, "TkImageData"):
            self.__diagram_tkimage_draw(territory_data, diagram_data,  di_name, di_del, image_tk)

        # if self.get_diagram_type(di_name, "MatplotlibImageData"):
        #    self.__diagram_matplotlibimage_draw(territory_data, diagram_data,  di_name, di_del, image_tk)

        self.callback_operation.event("diagram_draw", info=(territory_data, diagram_data, di_name))

        diagram_data.draw_tag = True
        return

    def diagram_shape_view_status(self, di_name, view):
        self.canvas_data.territory[self.te_name].diagram[di_name].view_state = copy.deepcopy(view)

    def __diagram_tkimage_draw(self, territory_data, diagram_data,  di_name, di_del, image_tk):

        self.image_tk = image_tk

        x_pos = territory_data.position[0] + territory_data.size[0] / 2
        y_pos = territory_data.position[1] + territory_data.size[1] / 2

        print("__diagram_tkimage_draw", x_pos, y_pos)

        if di_del:
            self.canvas_data.canvas.delete(self, self.canvas_data.territory[self.te_name].diagram[di_name].tag)
            diagram_data.draw_tag = False
            return

        if self.image_tk is None:
            return

        print("image_tk ******", type(self.image_tk), diagram_data.draw_tag)

        if not diagram_data.draw_tag:
            self.canvas_data.territory[self.te_name].diagram[di_name].tag = self.common_control.get_tag_name(self.uidata_id, self.te_name, di_name)
            self.canvas_data.canvas.create_image(
                x_pos,       # 画像表示位置(Canvasの中心)
                y_pos,
                tags=self.canvas_data.territory[self.te_name].diagram[di_name].tag  # tag
            )
            print("not diagram_data.draw_tag")

        self.canvas_data.canvas.itemconfigure(self.canvas_data.territory[self.te_name].diagram[di_name].tag, image=self.image_tk)
        self.canvas_data.canvas.coords(self.canvas_data.territory[self.te_name].diagram[di_name].tag, x_pos, y_pos)

        print("表示", type(self.image_tk), diagram_data.draw_tag)

    def __diagram_shape_draw(self, territory_data, diagram_data,  di_name, di_del):

        if di_del:
            self.canvas_data.canvas.delete(self, self.canvas_data.territory[self.te_name].diagram[di_name].tag)
            diagram_data.draw_tag = False
            return

        color = diagram_data.color
        xy, size_xy = self.__left_coordinate_calculation(territory_data, diagram_data)
        self.operation["log"].write("shape", xy, size_xy,  di_name)
        if diagram_data.draw_tag and not diagram_data.shape_point is None:
            pos, size = self.get_diagram_position_size(di_name)
            self.canvas_data.canvas.moveto(self.canvas_data.territory[self.te_name].diagram[di_name].tag, xy[0]-size[0]/2, xy[1]-size[1]/2)

        elif diagram_data.draw_tag:
            view_state = self.canvas_data.territory[self.te_name].diagram[di_name].view_state
            tk_view = {0: tk.NORMAL, 1: tk.DISABLED, 2: tk.HIDDEN}
            state = tk_view[view_state]
            self.canvas_data.canvas.itemconfigure(self.canvas_data.territory[self.te_name].diagram[di_name].tag, fill=color, state=state)
            self.canvas_data.canvas.coords(self.canvas_data.territory[self.te_name].diagram[di_name].tag, xy[0], xy[1], size_xy[0]+xy[0], size_xy[1]+xy[1])

        if not diagram_data.draw_tag and not diagram_data.shape_point is None:
            # #print(diagram_data.shape_point)
            self.canvas_data.territory[self.te_name].diagram[di_name].tag = self.common_control.get_tag_name(self.uidata_id, self.te_name, di_name)
            self.canvas_data.canvas.create_polygon(diagram_data.shape_point, fill=color, outline=diagram_data.outline, width=diagram_data.width, tags=self.canvas_data.territory[self.te_name].diagram[di_name].tag, joinstyle=tk.BEVEL)

        elif not diagram_data.draw_tag:
            self.canvas_data.territory[self.te_name].diagram[di_name].tag = self.common_control.get_tag_name(self.uidata_id, self.te_name, di_name)
            self.canvas_data.canvas.create_rectangle(xy[0], xy[1], size_xy[0]+xy[0], size_xy[1]+xy[1], fill=color, outline=diagram_data.outline, width=diagram_data.width, tags=self.canvas_data.territory[self.te_name].diagram[di_name].tag)  # 塗りつぶし

    def __diagram_text_draw(self, territory_data, diagram_data,  di_name, di_del):

        if di_del:
            self.canvas_data.canvas.delete(self, self.canvas_data.territory[self.te_name].diagram[di_name].tag)
            diagram_data.draw_tag = False
            return

        xy = self.__center_target_calculation(territory_data, diagram_data)

        self.operation["log"].write("text", xy, diagram_data.text)

        if diagram_data.draw_tag:
            old_text_len = self.canvas_data.canvas.index(self.canvas_data.territory[self.te_name].diagram[di_name].tag, tk.END)  # 文字数の長さを取得
            self.operation["log"].write(old_text_len)
            self.canvas_data.canvas.dchars(self.canvas_data.territory[self.te_name].diagram[di_name].tag, 0, old_text_len - 1)
            self.canvas_data.canvas.insert(self.canvas_data.territory[self.te_name].diagram[di_name].tag, 0, diagram_data.text)

        if not diagram_data.draw_tag:
            self.canvas_data.territory[self.te_name].diagram[di_name].tag = self.common_control.get_tag_name(self.uidata_id, self.te_name, di_name)
            self.canvas_data.canvas.create_text(0, 0, text="new", tags=self.canvas_data.territory[self.te_name].diagram[di_name].tag)

        # print("色情報", diagram_data.color)
        self.canvas_data.canvas.itemconfigure(self.canvas_data.territory[self.te_name].diagram[di_name].tag, text=diagram_data.text, font=(
            diagram_data.font_type, diagram_data.font_size), fill=diagram_data.color)
        # self.canvas_data.canvas.tag_config(self.canvas_data.territory[self.te_name].diagram[di_name].tag)

        if diagram_data.anchor == 1:
            text_xy, text_size = self.get_diagram_position_size(di_name)

            xy[0] -= text_size[0] / 2
            xy[1] -= text_size[1] / 2

        print("テキスト最終座標", xy)

        # print("テキスト最終座標", xy)

        self.canvas_data.canvas.moveto(self.canvas_data.territory[self.te_name].diagram[di_name].tag, xy[0], xy[1])

    def __diagram_textbox_draw(self, territory_data, diagram_data,  di_name, di_del, forget):
        if di_del:
            self.canvas_data.territory[self.te_name].diagram[di_name].entry.destroy()
            return

        if forget:
            self.canvas_data.territory[self.te_name].diagram[di_name].entry.place_forget()
            return

        xy, size_xy = self.__left_coordinate_calculation(territory_data, diagram_data)

        self.operation["log"].write_func_list(self.canvas_data.territory[self.te_name].diagram[di_name].entry.place)

        self.canvas_data.territory[self.te_name].diagram[di_name].entry.place(
            x=xy[0],
            y=xy[1],
            width=size_xy[0],
            height=size_xy[1])

        old_text_len = int(len(self.get_textbox_text(di_name)))
        self.operation["log"].write(old_text_len)

        if not diagram_data.draw_tag:
            self.canvas_data.territory[self.te_name].diagram[di_name].tag = self.common_control.get_tag_name(self.uidata_id, self.te_name, di_name)

        self.canvas_data.territory[self.te_name].diagram[di_name].entry.delete(0, "end")
        self.canvas_data.territory[self.te_name].diagram[di_name].entry.insert(0, copy.deepcopy(diagram_data.text))

        # print("text", diagram_data.text)

        read = {True: "readonly", False: "normal"}
        state = read[diagram_data.readonly]
        # print("state", state)
        text_color = self.canvas_data.territory[self.te_name].diagram[di_name].text_color
        back_ground_color = self.canvas_data.territory[self.te_name].diagram[di_name].back_ground_color
        self.canvas_data.territory[self.te_name].diagram[di_name].entry.configure(state=state, fg=text_color, bg=back_ground_color)

    def diagram_forget(self, di_name, forget):
        self.canvas_data.territory[self.te_name].diagram[di_name].forget = forget

    def __left_coordinate_calculation(self, territory_data, diagram_data):  # 中心部から左上への座標計算用 #主にshape向け

        xy, size_xy = [0, 0], [0, 0]  # 領域基準
        for i in range(2):
            if diagram_data.fill[i]:
                xy[i] = copy.deepcopy(territory_data.position[i])
                size_xy[i] = copy.deepcopy(territory_data.size[i])

            else:
                xy[i] = territory_data.position[i] + diagram_data.position[i]
                size_xy[i] = copy.deepcopy(diagram_data.size[i])

        return xy, size_xy

    def __center_target_calculation(self, territory_data, diagram_data):

        xy = [0, 0]  # 領域基準
        for i in range(2):
            # xy[i] = diagram_data.position[i] + territory_data.position[i]
            if diagram_data.center[i]:  # テリトリーの中心になるよう設定さてる場合
                xy[i] = territory_data.position[i] + (territory_data.size[i] / 2)
            else:  # 普通の指定
                xy[i] = (diagram_data.size[i] / 2) + diagram_data.position[i] + territory_data.position[i]

        return xy

    def get_textbox_text(self, di_name):
        text = self.canvas_data.territory[self.te_name].diagram[di_name].entry.get()
        return text

    def get_diagram_position_size(self,  di_name):
        pos_size = self.canvas_data.canvas.bbox(self.canvas_data.territory[self.te_name].diagram[di_name].tag)

        position = pos_size[0], pos_size[1]
        size = pos_size[2] - pos_size[0], pos_size[3] - pos_size[1]

        return position, size

    def tk_font_inquiry(self, font_name):
        if not font_name in self.tkFont_list:
            pass
            # print("font: {0} は 使用できません".format(font_name))

        return font_name

    def popup_set(self, send):
        if not send is None:
            self.popup_list = send

    def get_text(self, di_name):
        return copy.deepcopy(self.canvas_data.territory[self.te_name].diagram[di_name].text)

    def run_entry_event_callback(self, di_name):
        self.canvas_data.territory[self.te_name].diagram[di_name].entry_event_callback(self.get_text(di_name))

    def edit_diagram_text(self,
                          di_name,
                          text=None,
                          font_size=None,
                          font_type=None,
                          x_center=None,
                          y_center=None,
                          center=None,
                          anchor=None,
                          readonly=None,
                          entry_event=None,
                          set_int_type=None,
                          text_color=None,
                          back_ground_color=None):

        if not self.get_diagram_type(di_name, "TextBoxData") and not self.get_diagram_type(di_name, "DiagramTextData"):
            self.operation["error"].action(message="これテキスト用じゃないぞ")

        territory_data = self.canvas_data.territory[self.te_name]
        diagram_data = self.canvas_data.territory[self.te_name].diagram[di_name]

        if not text is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].text = copy.deepcopy(str(text))
        if not font_size is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].font_size = copy.deepcopy(font_size)
        if not font_type is None:
            self.tk_font_inquiry(font_type)
            self.canvas_data.territory[self.te_name].diagram[di_name].font_type = copy.deepcopy(font_type)
        if not x_center is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].center[0] = copy.deepcopy(x_center)
        if not y_center is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].center[1] = copy.deepcopy(y_center)
        if not center is None:
            self.canvas_data.territory[self.te_name].diagram[di_name].center = copy.deepcopy([center, center])

        if not anchor is None and self.get_diagram_type(di_name, "DiagramTextData"):
            self.canvas_data.territory[self.te_name].diagram[di_name].anchor = copy.deepcopy(anchor)
        if not readonly is None and self.get_diagram_type(di_name, "TextBoxData"):
            self.canvas_data.territory[self.te_name].diagram[di_name].readonly = copy.deepcopy(bool(readonly))
        if not entry_event is None and self.get_diagram_type(di_name, "TextBoxData"):
            self.canvas_data.territory[self.te_name].diagram[di_name].entry_event_callback = entry_event

        if not text_color is None and self.get_diagram_type(di_name, "TextBoxData"):
            self.canvas_data.territory[self.te_name].diagram[di_name].text_color = copy.deepcopy(text_color)
        if not back_ground_color is None and self.get_diagram_type(di_name, "TextBoxData"):
            self.canvas_data.territory[self.te_name].diagram[di_name].back_ground_color = copy.deepcopy(back_ground_color)

        self.diagram_draw(di_name)

    def open_file_select(self, default):

        if default is None:
            default = "~/"

        file_name = filedialog.askopenfilename(initialdir=default)
        return file_name

    def open_folder_select(self, default):

        if default is None:
            default = "~/"

        file_name = filedialog.askdirectory(initialdir=default)
        return file_name

    # folder


class TerritoryData:
    def __init__(self):
        self.size = [0, 0]
        self.position = [0, 0]
        self.diagram = {}
        self.event = {}
        self.blank_space = [0, 0]

        # ##print("生成")


# diagram_base = DiagramBase()


class TkImageData():
    def __init__(self):
        self.size = [0, 0]
        self.position = [0, 0]
        self.color = None
        self.fill = [False, False]
        self.draw_tag = False
        self.event = {}
        self.shape_point = None
        self.view_state = 0  # 0,1,2 #通常 #選択不可 #非表示
        self.tag = None


class DiagramData():
    def __init__(self):
        self.size = [0, 0]
        self.position = [0, 0]
        self.color = None
        self.fill = [False, False]
        self.draw_tag = False
        self.event = {}
        self.shape_point = None

        self.view_state = 0  # 0,1,2 #通常 #選択不可 #非表示

        self.tag = None

        self.width = 0
        self.outline = "#ffffff"

        #self.function = {}


class DiagramTextData():
    def __init__(self, canvas):
        self.size = [0, 0]
        self.position = [0, 0]
        self.color = None
        self.fill = [False, False]
        self.draw_tag = False
        self.event = {}

        self.text = ""
        self.font_size = 0
        self.font_type = None
        self.center = [False, False]

        # self.target = None
        self.anchor = 1

        self.tag = None

        # self.label = tk.Label(canvas, text="None")

        # 配置可能なスペースに余裕がある場合、Widget をどこに配置するか指定します。
        # デフォルトは Tk.CENTER. そのほかに、Tk.W (左よせ）、Tk.E （右よせ）、Tk.N （上よせ）、Tk.S （下よせ）、 Tk.NW （左上）、Tk.SW （左下）、Tk.NE （右上）、Tk.SE （右下）
        # must be n, ne, e, se, s, sw, w, nw, or center

        # self.old_text_len = 0


class TextBoxData():
    def __init__(self, canvas):
        self.size = [0, 0]
        self.position = [0, 0]
        self.text_color = None
        self.back_ground_color = None
        self.fill = [False, False]
        self.draw_tag = False
        self.event = {}

        self.text = ""
        self.font_size = 0
        # self.target = None
        self.center = [False, False]
        self.entry = tk.Entry(canvas, highlightthickness=0, relief="flat")
        self.readonly = False
        self.forget = False

        self.entry.bind("<{0}>".format("Return"), self.entry_event, "+")
        self.entry.bind("<{0}>".format("KeyPress"), self.entry_event_push_ban, "+")
        self.entry.bind("<{0}>".format("KeyRelease"), self.entry_event, "+")

        self.tag = None
        self.entry_event_callback = self.not_event
        self.block_key = {}

        self.push_key = {}

        self.type_int = False

        self.event_ban_set()

    def event_ban_set(self):
        self.block_key = {"Meta": False, "Control": False, "Alt": False, "Shift": False}

        # print("破棄再生")

    def entry_event_push_ban(self, event):
        # print("検査")
        for k in self.block_key.keys():
            if k in event.keysym:
                self.block_key[k] = True

        self.push_key[event.keysym] = True in list(self.block_key.values())

    def entry_event(self, event):  # event.keysym
        # print("終了したもの", event.keysym)

        flag = False

        if event.keysym in list(self.push_key.keys()) and self.push_key[event.keysym]:
            del self.push_key[event.keysym]

            flag = True

        if True in list(self.block_key.values()):
            # print("返却")
            for k in self.block_key.keys():
                if k in event.keysym:
                    self.block_key[k] = False

            flag = True

        if flag:
            return

        get_text = copy.deepcopy(self.entry.get())
        self.text = copy.deepcopy(get_text)
        self.entry_event_callback(copy.deepcopy(get_text))

    def not_event(self, text):
        pass

        # <br/>があれば改行にしたいね
