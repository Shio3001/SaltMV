
permission = 3  # 接触範囲許可範囲


class CommonControl:
    def __init__(self, window):
        self.window = window

    def xy_compilation(self, origin, x=None, y=None):  # 設定項目を変更する
        if not x is None:
            origin[0] = x

        if not y is None:
            origin[1] = y

        return origin

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
        mouse = [None, None]
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

        for i in range(2):
            if (data.position[i] - permission) <= mouse[i] <= (data.position[i] + data.size[i] + permission):
                join_detection[i] = True

        if join_detection[0] and join_detection[1]:
            join_detection[2] = True

        return mouse, edge_detection, join_detection

    def get_bind_name(self, key, func):
        func_name = str(func.__name__)
        name = "{0}_{1}".format(key, func_name)
        print(name)
        return func_name
