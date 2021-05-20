import copy


class TimelineCalculation:
    def __init__(self, UI_common_control, territory, get_set_option_data, direction=None, debug_name=None, size_del=None):
        self.common_control = UI_common_control
        self.territory = territory

        self.debug_name = debug_name

        self.direction = direction
        if self.direction is None:
            self.direction = 0

        self.sta_end_px = [0, 0]
        self.sta_end_f = [0, 1]
        self.sta_end_f_view = [0, 1]

        self.ratio_f = [0, 0]  # pos,size]
        # self.convert = 1

        self.blank_space = 0

        def test(pos_size):
            pass
            # print(pos_size)

        self.draw_func = test
        self.draw_func_sub_point = test

        self.size_del = False
        if not size_del is None:
            self.size_del = size_del

        self.get_set_option_data = get_set_option_data

        self.sub_point_f = {}  # sub_point_name : frame_pox¥s

        print(debug_name, "===============================================")

    def set_draw_func(self, func):
        if not str(type(func)) == "<class 'function'>":
            return
        self.draw_func = func

    def set_draw_sub_point_func(self, func):
        if not str(type(func)) == "<class 'function'>":
            return
        self.draw_func_sub_point = func

    def set_sta_end_px(self, sta=None, end=None, space=None):
        if not space is None:
            self.blank_space = space

        if not sta is None:
            sta += self.blank_space

        if not end is None:
            end -= self.blank_space

        self.sta_end_px = self.common_control.xy_compilation(self.sta_end_px, x=sta, y=end)

    def set_sta_end_f(self, sta=None, end=None, view_edit=None):
        self.sta_end_f = self.common_control.xy_compilation(self.sta_end_f, x=sta, y=end)

    def init_set_sta_end_f(self, sta=None, end=None, view_edit=None):
        self.sta_end_f_view = self.common_control.xy_compilation(self.sta_end_f_view, x=sta, y=end)

    # def init_set_px_ratio_point(self,sub_name):
    #    self.sub_point_f[sub_name] = position

    def set_sub_point(self, sub_name):
        self.sub_point_f[sub_name] = 0

    def set_px_ratio_sub_point(self, sub_name, position=None):  # positionはpx入力
        if position is None:
            return

        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]
        frame_long_view = self.sta_end_f_view[1] - self.sta_end_f_view[0]

        rate = frame_long / scroll_long

        pos_f = 0

        if not position is None:
            pos_f = (position - self.blank_space) * rate + self.sta_end_f[0]

        if pos_f < self.sta_end_f_view[0]:  # posが0より手前になった
            pos_f = copy.deepcopy(self.sta_end_f_view[0])

        if pos_f > self.sta_end_f_view[1]:  # posが0より手前になった
            pos_f = copy.deepcopy(self.sta_end_f_view[1])

        self.sub_point_f[sub_name] = copy.deepcopy(pos_f)

        return self.sub_point_f[sub_name]

    def set_f_ratio_sub_point(self, sub_name, position=None):  # position は frame入力
        position = copy.deepcopy(position)  # 参照渡し防止用

        if not position is None:
            if position < self.sta_end_f_view[0]:
                position = copy.deepcopy(self.sta_end_f_view[0])

            if position > self.sta_end_f_view[1]:
                position = copy.deepcopy(self.sta_end_f_view[1])

            if not position is None:
                self.sub_point_f[sub_name] = copy.deepcopy(position)

        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]
        rate = scroll_long / frame_long
        pos_px = (self.sub_point_f[sub_name] - self.sta_end_f[0]) * rate

        return pos_px

    def set_px_ratio(self, position=None, size=None):

        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]
        frame_long_view = self.sta_end_f_view[1] - self.sta_end_f_view[0]

        rate = frame_long / scroll_long

        pos_f, size_f = None, None

        if not size is None and size < 1:
            size = 1

        if not position is None:
            self.ratio_f[0] = (position - self.blank_space) * rate + self.sta_end_f[0]

        if not size is None:
            self.ratio_f[1] = size * rate

        flag = ""

        if self.ratio_f[0] < self.sta_end_f_view[0]:  # posが0より手前になった
            self.ratio_f[0] = copy.deepcopy(self.sta_end_f_view[0])
            flag += "A"

        if self.ratio_f[1] > frame_long_view:  # sizeが幅を超えた
            self.ratio_f[0] = copy.deepcopy(self.sta_end_f_view[0])
            self.ratio_f[1] = copy.deepcopy(frame_long_view)

            flag += "B"

        if self.ratio_f[0] + self.ratio_f[1] > frame_long_view:
            self.ratio_f[0] = frame_long_view - self.ratio_f[1]
            flag += "C"

        # if self.ratio_f[0] * pos_rate / rate - self.sta_end_f[0] > self.sta_end_f_view[1]:  # posの値が幅を超えた
        #    self.ratio_f[0] = copy.deepcopy(self.sta_end_f_view[1] / pos_rate * rate + self.sta_end_f[0])
        #    flag += "C"

        #print(self.debug_name, " :pxから", "割合設定", self.ratio_f, "rate", rate, "pos_rate", pos_rate, "position", position, "size", size, "flag", flag, "sta_end_f", self.sta_end_f, "sta_end_f_view,", self.sta_end_f_view)

        if not flag == "":
            self.set_f_ratio()
            return

        self.draw_func(position, size)

    def set_f_ratio(self, position=None, size=None):
        self.ratio_f = self.common_control.xy_compilation(self.ratio_f, x=position, y=size)

        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]

        # print(self.sta_end_f)

        rate = scroll_long / frame_long
        now_view_start_f = (self.ratio_f[0] - self.sta_end_f[0])

        #pos_px = now_f * rate * pos_plus if self.size_del else now_f * rate
        pos_px = (self.ratio_f[0] - self.sta_end_f[0]) * rate
        size_px = self.ratio_f[1] * rate

        for k in self.sub_point_f.keys():
            self.set_f_ratio_sub_point(k)

        #print(self.debug_name, " :frameから", "割合設定", self.ratio_f, "rate", rate, "pos_px", pos_px, "size_px", size_px, "pos_plus", pos_plus, "now_f", now_f, "sta_end_f", self.sta_end_f)

        self.draw_func(pos_px + self.blank_space, size_px)

    def __draw(self, frame, px):
        self.draw_func(frame, px)

    def get_event_data(self):
        ratio_data = RatioData(self.get_set_option_data(), self.ratio_f, self.sta_end_f)
        return ratio_data

# 複雑にしている原因分かったかもしれない
# 原因、ストッパーの機能をpx側でもやろうとしてたからだ、普通にframe側でやればいいのでは


class RatioData:
    def __init__(self, option_data, ratio_f, sta_end_f):
        self.option_data = copy.deepcopy(option_data)
        self.ratio_f = copy.deepcopy(ratio_f)
        self.sta_end_f = copy.deepcopy(sta_end_f)
