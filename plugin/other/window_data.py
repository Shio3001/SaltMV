import tkinter as tk


class SendWindowData:  # window生成のためのデータ
    def __init__(self, main_window, all_data, UI_parts, UI_auxiliary, all_UI_data):
        self.tk = tk
        self.menubar_list = {}
        self.window_size = [100, 100]
        self.window_name = "tkinter"
        self.main_window = main_window
        self.operation = all_data.operation
        self.all_data = all_data
        self.all_UI_data = all_UI_data

        self.GUI_base_color = "#1a1a1a"
        self.GUI_alpha_color = "#000000"

        if not self.main_window is None:
            self.window = tk.Toplevel(self.main_window)
        else:
            self.window = tk.Tk()

        self.common_control = all_UI_data.CommonControl(self.window, self.operation)
        self.UI_parts = UI_parts
        self.UI_auxiliary = UI_auxiliary

        self.canvas_data = {}

        self.window.configure(bg=self.GUI_base_color)

    def window_open_close(self, select):
        if select == True:
            self.window.deiconify()
        if select == False:
            self.window.withdraw()

    def window_event(self, processing=None, user_event=None):
        if not processing is None and not user_event is None:
            self.window.bind("<{0}>".format(user_event), processing, "+")

    #####################################################################################

    def new_canvas(self, name):
        self.canvas_data[name] = CanvasData(self.window)

    def del_canvas(self, name):
        del self.canvas_data[name]

    def edit_canvas_size(self, name, x=None, y=None):
        self.canvas_data[name].size = self.common_control.xy_compilation(self.canvas_data[name].size, x=x, y=y)
        print("ペイント", self.canvas_data[name].size)
        self.canvas_data[name].canvas.config(width=self.canvas_data[name].size[0])
        self.canvas_data[name].canvas.config(height=self.canvas_data[name].size[1])

    def edit_canvas_position(self, name, x=None, y=None):
        self.canvas_data[name].position = self.common_control.xy_compilation(self.canvas_data[name].position, x=x, y=y)
        self.canvas_data[name].canvas.place(x=self.canvas_data[name].position[0], y=self.canvas_data[name].position[1])

    def get_canvas_contact(self, name):
        mouse, canvas_edge, canvas_join = self.common_control.contact_detection(self.canvas_data[name])
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
            print(self.canvas_data[name].event[k], f)

        self.canvas_data[name].event = {}

    def get_canvas_event(self, name):
        return self.canvas_data[name].event

    #####################################################################################

    def new_parts(self, name, parts_name=None):
        new_parts_obj = self.UI_parts[parts_name].parts().UI_set(self.UI_auxiliary.SendUIData(self.window, self.canvas_data[name], self.common_control, self.all_data, self.all_UI_data, self.GUI_base_color, self.GUI_alpha_color))
        return new_parts_obj

    def display_size_get(self):
        display_size = [self.window.winfo_screenwidth(), self.window.winfo_screenheight()]
        return display_size

    def window_size_set(self, send):
        if not send is None:
            self.window_size = send
        self.window.resizable(width=True, height=True)
        self.window.geometry("{0}x{1}".format(self.window_size[0], self.window_size[1]))

    def window_title_set(self, send):
        if not send is None:
            self.window_name = send
        self.window.title(self.window_name)

    def menubar_set(self, send):
        if not send is None:
            self.menubar_list = send

        window_menubar = tk.Menu(self.window)

        for bar in self.menubar_list:

            main_bar = ""
            bar_name = []
            bar_prg = []
            # 奇数と偶数逆じゃん!とおもったら配列は0からはじまりました
            for i, content in enumerate(bar):
                if i == 0:
                    main_bar = content
                elif i % 2 == 0:
                    bar_prg.append(content)
                    # print("bar偶数情報", content, i)
                elif (i + 1) % 2 == 0:
                    bar_name.append(content)
                    # print("bar奇数情報", content, i)

            pull_down = tk.Menu(window_menubar, tearoff=0)

            window_menubar.add_cascade(label=main_bar, menu=pull_down)  # それぞれ

            for n, p in zip(bar_name, bar_prg):
                pull_down.add_command(label=n, command=p)
                self.operation["log"].write("メニューバー登録 {0} {1}".format(n, p))

        self.operation["log"].write("バー設定終了{0}".format(self.window))

        self.window.config(menu=window_menubar)
        self.window.update()

        # self.window.mainloop()


class CanvasData:
    def __init__(self, window):
        self.size = [0, 0]
        self.position = [0, 0]

        self.canvas = tk.Canvas(window, highlightthickness=0, width=self.size[0], height=self.size[1])

        self.territory = {}

        self.event = {}

        print(self.canvas)

    def event_link(self):
        pass
