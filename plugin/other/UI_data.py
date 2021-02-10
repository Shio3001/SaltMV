import tkinter as tk
import copy

permission = 3  # 接触範囲許可範囲


class SendUIData:  # パーツひとつあたりのためのclass
    def __init__(self, window, all_data, all_UI_data, GUI_base_color, GUI_alpha_color):
        self.window = window
        self.all_data = all_data
        self.all_UI_data = all_UI_data
        self.GUI_base_color = GUI_base_color
        self.GUI_alpha_color = GUI_alpha_color

        self.common_control = CommonControl(self.window)
        self.tk = tk


class CanvasData:
    def __init__(self, window):
        self.size = [0, 0]
        self.position = [0, 0]
        self.canvas = tk.Canvas(window, highlightthickness=0, width=self.size[0], height=self.size[1])

    def event_link(self):
        pass


class TextBoxData:
    def __init__(self, window):
        self.position = [0, 0]
        self.text = ""


class TerritoryData:
    def __init__(self, canvas):
        self.size = [0, 0]
        self.position = [0, 0]


class DiagramData:
    def __init__(self, territory):
        self.size = []
        self.position = [0, 0]
        self.text = ""

    def event_link(self):
        pass


class CommonControl:
    def __init__(self, window):
        self.window = window

    def xy_compilation(self, origin, user_select):
        for o, s in zip(origin, user_select):
            if not s is None:
                o = s

        return origin

    def contact_edge(self):
        return

    def event_temporary(self):
        return

    def get_mouse_position(self):  # マウスの位置を取得
        mouse = []
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

        for j in range(2):

            if (data.position[i] - permission) <= mouse[i] <= (data.position[i] + data.size[i] + permission):
                join_detection[i] = True

            if join_detection[0] and join_detection[1]:
                join_detection[2] = True

        return edge_detection, join_detection
