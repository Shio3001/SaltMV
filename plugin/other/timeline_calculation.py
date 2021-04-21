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
        pos_rate = (scroll_long + size) / scroll_long

        pos_f, size_f = None, None

        if not position is None:
            pos_f = position * rate * pos_rate
        if not size is None:
            size_f = size * rate

        print(pos_f, size_f)

        self.draw_func(position, size)

    def set_f_ratio(self, position=None, size=None):
        self.ratio_f = self.common_control.xy_compilation(self.ratio_f, x=position, y=size)

        self.draw_func(20, 10)

        """
        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]

        rate = scroll_long / frame_long
        pos_rate = (scroll_long + self.ratio_f[1]) / frame_long

        self.draw_func(self.ratio_f[0], self.ratio_f[1])
        """

        # self.__draw()

    """
    def __convert_px_f(self, px):
        self.ratio_f =

    def __convert_f_px(self):
        return ratio_px
    """

    """
    def __set_convert(self):
        px_lengh = sta_end_px[1] - sta_end_px[0]

        self.convert =
    """

    def __draw(self, frame, px):

        self.draw_func(frame, px)

# 複雑にしている原因分かったかもしれない
# 原因、ストッパーの機能をpx側でもやろうとしてたからだ、普通にframe側でやればいいのでは
