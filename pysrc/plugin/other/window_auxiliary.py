
import tkinter as tk
import tkinter.font as tkFont
import copy
import inspect


class SendWindowData:  # window生成のためのデータ
    def __init__(self, main_window, edit_control_auxiliary, UI_parts, UI_auxiliary, UI_control):
        self.tk = tk
        self.menubar_list = {}
        self.window_size = [100, 100]
        self.window_name = "tkinter"
        self.main_window = main_window
        self.operation = edit_control_auxiliary.operation
        self.edit_control_auxiliary = edit_control_auxiliary
        self.UI_control = UI_control

        self.GUI_base_color = "#1a1a1a"
        self.GUI_alpha_color = "#000000"

        self.font_data = edit_control_auxiliary.font_data

        if not self.main_window is None:
            self.window = tk.Toplevel(self.main_window)
            self.window.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())
        else:
            self.window = tk.Tk()

        self.common_control = UI_control.CommonControl(self.window, self.operation)
        self.UI_parts = UI_parts
        self.UI_auxiliary = UI_auxiliary

        self.canvas_data = {}
        self.window_event = {}

        self.tkFont = tkFont
        self.tkFont_list = list(self.tkFont.families())  # これを使うにはtk.TK()をしたあとじゃないとダメらしい

        self.window_menubar = None
        self.window_resizable = [True, True]
        #self.pull_down = {}

        self.window.configure(bg=self.GUI_base_color)

    def window_open_close(self, select):
        if select == True:
            self.window.deiconify()

        if select == False:
            self.window.withdraw()

    def get_window_view_flag(self):
        return self.window.winfo_exists()

    def add_window_event(self, key, func):  # event
        bind_id = self.window.bind("<{0}>".format(key), func, "+")
        self.window_event[self.common_control.get_tag_name(key, func)] = [key, func, bind_id]

    def del_window_event(self, key, func):  # event
        bind_name = self.common_control.get_tag_name(key, func)
        bind_id = self.window_event[bind_name][2]
        self.window.unbind("<{0}>".format(key), bind_id)
        del self.window_event[bind_name]

    def all_add_window_event(self):
        for k, f in zip(self.window_event.keys(), self.window_event.values()):
            self.window.bind("<{0}>".format(f[0]), f[1], "+")

    def all_del_window_event(self):  # canvasの再生成時の復元
        for k, f in zip(self.window_event.keys(), self.window_event.values()):
            self.window.unbind("<{0}>".format(f[0]), f[2])

        self.window_event = {}

    def get_window_event(self):
        return self.window_event

    def get_window_size(self):
        size_x = self.window.winfo_width()
        size_y = self.window.winfo_height()

        return size_x, size_y

    def get_window_position(self):
        self.window.update_idletasks()

        x = self.window.winfo_x()
        y = self.window.winfo_y()

        return x, y

    def get_window_contact(self):
        size_x, size_y = self.get_window_size()
        x, y = self.get_window_position()
        mouse, window_edge, window_join = self.common_control.contact_detection([x, y], [size_x, size_y])

        return mouse, window_edge, window_join, [x, y]

        #####################################################################################

    def new_canvas(self, name):
        self.canvas_data[name] = CanvasData(self.window)

    def del_canvas(self, name):
        del self.canvas_data[name]

    def edit_canvas_size(self, name, x=None, y=None):
        self.canvas_data[name].size = self.common_control.xy_compilation(self.canvas_data[name].size, x=x, y=y)
        ##print("ペイント", self.canvas_data[name].size)
        self.canvas_data[name].canvas.config(width=self.canvas_data[name].size[0])
        self.canvas_data[name].canvas.config(height=self.canvas_data[name].size[1])

        return self.canvas_data[name].size

    def edit_canvas_position(self, name, x=None, y=None):
        self.canvas_data[name].position = self.common_control.xy_compilation(self.canvas_data[name].position, x=x, y=y)
        self.canvas_data[name].canvas.place(x=self.canvas_data[name].position[0], y=self.canvas_data[name].position[1])
        self.common_control.set_canvas_position(self.canvas_data[name].position)

        return self.canvas_data[name].position

    def get_canvas_contact(self, name):
        mouse, canvas_edge, canvas_join = self.common_control.contact_detection(self.canvas_data[name].position, self.canvas_data[name].size)

        for i in range(2):
            mouse[i] -= self.canvas_data[name].position[i]

        return mouse, canvas_edge, canvas_join

    #####################################################################################

    def add_canvas_event(self, name, key, func):  # event
        bind_id = self.canvas_data[name].canvas.bind("<{0}>".format(key), func, "+")
        self.canvas_data[name].event[self.common_control.get_tag_name(key, func)] = [key, func, bind_id]

    def del_canvas_event(self, name, key, func):  # event
        bind_name = self.common_control.get_tag_name(key, func)
        bind_id = self.canvas_data[name].event[bind_name][2]
        self.canvas_data[name].canvas.unbind("<{0}>".format(key), bind_id)
        del self.canvas_data[name].event[bind_name]

    def all_add_canvas_event(self, name):
        for k, f in zip(self.canvas_data[name].event.keys(), self.canvas_data[name].event.values()):
            self.canvas_data[name].canvas.bind("<{0}>".format(f[0]), f[1], "+")

    def all_del_canvas_event(self, name):  # canvasの再生成時の復元
        for k, f in zip(self.canvas_data[name].event.keys(), self.canvas_data[name].event.values()):
            self.canvas_data[name].canvas.unbind("<{0}>".format(f[0]), f[2])
            ##print(self.canvas_data[name].event[k], f)

        self.canvas_data[name].event = {}

    def get_canvas_event(self, name):
        return self.canvas_data[name].event

    #####################################################################################

    def new_parts(self, name, territory_name, parts_name=None, option_data=None, base=None):

        #print("呼び出し先", inspect.stack()[1].function)

        window_event_data = {"add": self.add_window_event, "del": self.del_window_event, "all_add": self.all_add_window_event, "all_del": self.del_window_event, "get": self.get_window_event, "contact": self.get_window_contact}
        canvas_event_data = {"add": self.add_canvas_event, "del": self.del_canvas_event, "all_add": self.all_add_canvas_event, "all_del": self.del_canvas_event, "get": self.get_canvas_event, "contact": self.get_canvas_contact}

        #self.canvas_data[name].territory[territory_name].diagram = map(lambda x: copy.deepcopy(x.event), self.canvas_data[name].territory[territory_name].diagram)

        # self.canvas_data[name].territory[territory_name].diagram.values() = self.canvas_data[name].territory[territory_name].diagram.values

        #print("territory", self.canvas_data[name].territory)

        new_UIdata = self.UI_auxiliary.SendUIData(self.window,
                                                  self.canvas_data[name],
                                                  self.common_control,
                                                  self.edit_control_auxiliary,
                                                  self.UI_control,
                                                  self.GUI_base_color,
                                                  self.GUI_alpha_color,
                                                  window_event_data,
                                                  canvas_event_data,
                                                  copy.deepcopy(territory_name),
                                                  self.font_data,
                                                  self.tkFont,
                                                  self.tkFont_list,
                                                  base,
                                                  option_data,
                                                  self.get_window_contact,
                                                  self.get_window_view_flag)

        # new_UIdata.new_territory()

        #print("classIDの確認！", new_UIdata, "*******************************")

        new_parts_obj = self.UI_parts[parts_name].parts().UI_set(new_UIdata)

        del new_UIdata

        self.operation["log"].write_func_list(new_parts_obj)

        return new_parts_obj

    def display_size_get(self):
        display_size = [self.window.winfo_screenwidth(), self.window.winfo_screenheight()]
        return display_size

    def window_size_set(self, x=None, y=None, lock_x=None, lock_y=None):
        self.window_size = self.common_control.xy_compilation(self.window_size, x=x, y=y)
        self.window_resizable = self.common_control.xy_compilation(self.window_resizable, x=lock_x, y=lock_y)

        self.window.resizable(width=self.window_resizable[0], height=self.window_resizable[1])
        self.window.geometry("{0}x{1}".format(self.window_size[0], self.window_size[1]))

    def window_title_set(self, send):
        if not send is None:
            self.window_name = send
        self.window.title(self.window_name)

    def window_exit(self):
        self.window.destroy()

    # self.window.mainloop()


class CanvasData:
    def __init__(self, window):
        self.size = [0, 0]
        self.position = [0, 0]

        self.canvas = tk.Canvas(window, highlightthickness=0, width=self.size[0], height=self.size[1])

        self.territory = {}

        self.event = {}

        # #print(self.canvas)
