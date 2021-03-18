import copy


class TimelineCalculation:
    def __init__(self, UI_common_control, territory, direction=None, obj_length=None, debug_name=None):
        self.common_control = UI_common_control
        self.territory = territory
        self.obj_length = obj_length
        self.debug_name = debug_name

        self.direction = direction
        if self.direction is None:
            self.direction = 0

        self.sta_end_px = [0, 0]
        self.sta_end_f = [0, 1]

        self.ratio_px = [0, 0]  # pos,size
        self.ratio_f = [0, 0]  # pos,size

        self.convert = 1

        self.blank_space = 0

        def test(pos_size):
            print(pos_size)

        self.draw_func = test

    def set_draw_func(self, func):
        if not str(type(func)) == "<class 'function'>":
            return

        self.draw_func = func

    def stop_frame_max(self):
        if self.ratio_f[0] < self.sta_end_f[1]:
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
        self.ratio_px = self.common_control.xy_compilation(self.ratio_px, x=position, y=size)
        self.__convert_px_f()

    def set_f_ratio(self, position=None, size=None):
        self.ratio_f = self.common_control.xy_compilation(self.ratio_f, x=position, y=size)
        self.__convert_f_px()

    def __convert_px_f(self):
        self.__set_convert()
        self.ratio_f = [self.ratio_px[i] / self.convert for i in range(2)]

    def __convert_f_px(self):
        self.__set_convert()
        self.ratio_px = [self.ratio_f[i] * self.convert for i in range(2)]

    def __set_convert(self):
        self.convert = self.sta_end_px[0] / (self.sta_end_px[0] + self.ratio_px[1])

    def __draw(self):
        self.draw_func(self.ratio_px)

# 複雑にしている原因分かったかもしれない
# 原因、ストッパーの機能をpx側でもやろうとしてたからだ、普通にframe側でやればいいのでは
