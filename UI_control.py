import copy
import os

# timeline_operation_range = [100, 30]  # タイムライン操作開始地点
timeline_size = 30  # タイムライン幅

#user_timeline_selection = [0, 0]
permission = 3  # 接触範囲許可範囲


class CommonControl:
    def __init__(self, window, operation):
        self.window = window
        self.operation = operation
        self.canvas_position = [0, 0]

    def set_canvas_position(self, p):
        self.canvas_position = p

    def xy_compilation(self, origin, x=None, y=None):  # 設定項目を変更する
        calculation = list(copy.deepcopy(origin))
        if not x is None:
            calculation[0] = x

        if not y is None:
            calculation[1] = y

        return copy.deepcopy(calculation)

    def get_mouse_position(self):  # マウスの位置を取得
        mouse = [None, None]
        mouse[0] = self.window.winfo_pointerx() - self.window.winfo_rootx()
        mouse[1] = self.window.winfo_pointery() - self.window.winfo_rooty()

        return mouse

    def contact_detection(self, position, size, del_mouse=None):  # 辺に触れているか
        mouse = self.get_mouse_position()
        #position, size = self.get_position_size(data)

        position = [p + cp for p, cp in zip(position, self.canvas_position)]

        edge_detection = [[False, False], [False, False]]  # 辺に対する #x左,x右,y上,y下
        join_detection = [False, False, False]  # 中に対する #x , y, xy

        if not del_mouse is None and del_mouse:
            return mouse, edge_detection, join_detection

        for i in range(2):
            if (position[i] - permission) <= mouse[i] <= (position[i] + permission):
                edge_detection[i][0] = True

            if (position[i] + size[i] - permission) <= mouse[i] <= (position[i] + size[i] + permission):
                edge_detection[i][1] = True

        for i in range(2):
            if (position[i] - permission) <= mouse[i] <= (position[i] + size[i] + permission):
                join_detection[i] = True

        if join_detection[0] and join_detection[1]:
            join_detection[2] = True

        return mouse, edge_detection, join_detection

    # def get_bind_name(self, key, func):
    #    func_name = str(func.__name__)
    ##    name = "{0}_{1}".format(key, func_name)
    #    # print(name)
    #    return name

    def get_tag_name(self, *text):

        name = ""

        for t in text:
            name = "{0}_{1}".format(name, str(t))
        #name = "{0}_{1}".format(te_name, di_name)
        # print(name)
        return name
