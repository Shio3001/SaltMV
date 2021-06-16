import tkinter as tk


class MenuPopup:
    def __init__(self, targe, popup=None):
        self.target = targe
        self.target_menubar = tk.Menu(self.target)
        if not popup is True:
            self.target.config(menu=self.target_menubar)
        self.pull_down = {}

    def set(self, send=None):
        if not send is None:
            self.menubar_list = send

        for bar in self.menubar_list:
            if len(bar) == 2:
                main_bar = bar[0]
                bar_prg = bar[1]

                self.target_menubar.add_command(label=main_bar, command=bar_prg)

            if len(bar) > 2:
                # 奇数と偶数逆じゃん!とおもったら配列は0からはじまりました
                main_bar = ""
                bar_name = []
                bar_prg = []

                for i, content in enumerate(bar):
                    if i == 0:
                        main_bar = content

                    elif (i + 1) % 2 == 0:
                        bar_name.append(content)

                    elif i % 2 == 0:
                        bar_prg.append(content)

                self.pull_down[main_bar] = tk.Menu(self.target_menubar, tearoff=0)
                for n, p in zip(bar_name, bar_prg):
                    self.pull_down[main_bar].add_command(label=n, command=p)
                    self.pull_down[main_bar].update()
                self.target_menubar.add_cascade(label=main_bar, menu=self.pull_down[main_bar])  # それぞれ

        # self.operation["log"].write("バー設定終了{0}".format(self.target))

        self.target.update()
        self.target_menubar.update()

        # self.data.window.update()

        print("tkinter update", self.target.update)

    def show(self, x, y):
        self.target_menubar.post(x, y)

    def edit_bool(self, main_bar, name, bool_data):
        tk_bool = {True: tk.NORMAL, False: tk.DISABLED}
        self.pull_down[main_bar].entryconfigure(name, state=tk_bool[bool_data])

    def edit_bool_twice(self, name, bool_data):
        tk_bool = {True: tk.NORMAL, False: tk.DISABLED}
        self.target_menubar.entryconfigure(name, state=tk_bool[bool_data])
