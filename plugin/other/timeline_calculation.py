import copy


class TimelineCalculation:
    def __init__(self, UI_common_control, territory, direction=None, debug_name=None):
        self.common_control = UI_common_control
        self.territory = territory

        self.debug_name = debug_name

        self.direction = direction
        if self.direction is None:
            self.direction = 0

        self.sta_end_px = [0, 0]
        self.sta_end_f = [0, 1]

        self.ratio_f = [0, 0]  # pos,size]

        # self.convert = 1

        self.blank_space = 0

        def test(pos_size):
            pass
            # print(pos_size)

        self.draw_func = test

        print(debug_name, "===============================================")

    def set_draw_func(self, func):
        if not str(type(func)) == "<class 'function'>":
            return

        self.draw_func = func

    def stop_frame_max(self):
        if self.ratio_f[0] > self.sta_end_f[1]:
            self.ratio_f[0] = self.sta_end_f[1]

    def set_sta_end_px(self, sta=None, end=None, space=None):
        if not space is None:
            self.blank_space = space

        if not sta is None:
            sta += self.blank_space

        if not end is None:
            end -= self.blank_space

        self.sta_end_px = self.common_control.xy_compilation(self.sta_end_px, x=sta, y=end)

    def set_sta_end_f(self, sta=None, end=None):
        self.sta_end_f = self.common_control.xy_compilation(self.sta_end_f, x=sta, y=end)

    def set_px_ratio(self, position=None, size=None):

        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]

        rate = frame_long / scroll_long

        if scroll_long != size:
            pos_rate = frame_long / (scroll_long - size)

        else:
            pos_rate = 0

        pos_f, size_f = None, None

        if not size is None and size < 1:
            size = 1

        if not position is None:
            self.ratio_f[0] = (position - self.blank_space) * pos_rate

        if not size is None:
            self.ratio_f[1] = size * rate

        flag = False

        if self.ratio_f[0] < self.sta_end_f[0]:  # posが0より手前になった
            self.ratio_f[0] = 0
            flag = True

        if self.ratio_f[1] > frame_long:  # sizeが幅を超えた
            self.ratio_f[1] = frame_long
            flag = True

        if self.ratio_f[0] > self.sta_end_f[1]:  # posの値が幅を超えた
            self.ratio_f[0] = copy.deepcopy(self.sta_end_f[1])
            flag = True

        print("pxから", "割合設定", self.ratio_f, "rate", rate, "pos_rate", pos_rate, "position", position, "size", size)

        if flag:
            self.set_f_ratio()
            return

        self.draw_func(position, size)

    def set_f_ratio(self, position=None, size=None):
        self.ratio_f = self.common_control.xy_compilation(self.ratio_f, x=position, y=size)

        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]

        rate = scroll_long / frame_long
        pos_rate = scroll_long / (frame_long - self.ratio_f[1])

        pos_plus = (frame_long - self.ratio_f[1]) / frame_long

        pos_px = self.ratio_f[0] * rate * pos_plus
        size_px = self.ratio_f[1] * rate

        print("frameから", "割合設定", self.ratio_f, "rate", rate, "pos_rate", pos_rate, "pos_px", pos_px, "size_px", size_px)

        self.draw_func(pos_px + self.blank_space, size_px)

    def __draw(self, frame, px):

        self.draw_func(frame, px)

# 複雑にしている原因分かったかもしれない
# 原因、ストッパーの機能をpx側でもやろうとしてたからだ、普通にframe側でやればいいのでは
