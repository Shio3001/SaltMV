import copy


class TimelineCalculation:
    def __init__(self, UI_common_control, callback_operation, territory, get_set_option_data, direction=None, debug_name=None, size_del=None):
        self.common_control = UI_common_control
        self.territory = territory

        self.debug_name = debug_name
        self.callback_operation = callback_operation

        self.direction = direction
        if self.direction is None:
            self.direction = 0

        self.sta_end_px = [0, 0]
        self.sta_end_f = [0, 1]
        self.sta_end_f_init = [0, 1]

        self.ratio_f = [0, 0]  # pos,size]
        # self.convert = 1

        self.blank_space = 0

        def test(pos_size):
            pass
            # #print(pos_size)

        #self.draw_func = test

        self.size_del = False
        if not size_del is None:
            self.size_del = size_del

        self.get_set_option_data = get_set_option_data

        self.sub_point_f = {}  # sub_point_name : frame_pox¥s

        #print(debug_name, "===============================================")

    """

    def set_draw_func(self, func):
        if not str(type(func)) == "<class 'function'>":
            return
        self.draw_func = func

    def set_draw_sub_point_func(self, func):
        if not str(type(func)) == "<class 'function'>":
            return
        self.draw_func_sub_point = func
    """

    def get_extremity_f(self):
        minimum = 0
        maximum = 0

        point_values = self.sub_point_f.values()

        if len(point_values) <= 0:
            return None

        minimum = min(point_values)
        maximum = max(point_values)

        return minimum, maximum

    def get_extremity_px(self):
        minimum = 0
        maximum = 0

        point_values = self.sub_point_f.values()

        if len(point_values) <= 0:
            return None

        minimum = self.f_to_px(min(point_values))
        maximum = self.f_to_px(max(point_values))

        return minimum, maximum

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

    def init_set_sta_end_f(self, sta=None, end=None):
        self.sta_end_f_init = self.common_control.xy_compilation(self.sta_end_f_init, x=sta, y=end)

    # def init_set_px_ratio_point(self,sub_name):
    #    self.sub_point_f[sub_name] = position

    def px_to_f(self, pos_px, size_bool=None):
        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]
        #frame_long_init = self.sta_end_f_init[1] - self.sta_end_f_init[0]
        rate = frame_long / scroll_long

        pos_f = pos_px * rate if size_bool else (pos_px - self.blank_space) * rate + self.sta_end_f[0]

        return pos_f

    def f_to_px(self, pos_f, size_bool=None):
        scroll_long = self.sta_end_px[1] - self.sta_end_px[0]
        frame_long = self.sta_end_f[1] - self.sta_end_f[0]
        #frame_long_init = self.sta_end_f_init[1] - self.sta_end_f_init[0]
        rate = scroll_long / frame_long

        pos_px = pos_f * rate if size_bool else (pos_f - self.sta_end_f[0]) * rate

        return pos_px

    def set_sub_point(self, sub_name):
        self.sub_point_f[sub_name] = 0

    def set_px_ratio_sub_point(self, sub_name, position=None):  # positionはpx入力
        # print("positionからの設定")
        if position is None:
            return

        #print("座標指定", position)

        pos_f = self.px_to_f(position)
        self.sub_point_f[sub_name] = copy.deepcopy(pos_f)

        pos_px = self.f_to_px(self.sub_point_f[sub_name])
        #print("positionからの設定pos_px", pos_px)
        self.callback_operation.event("obj_sub_point", info=(sub_name, pos_px))  # 送るものはpx_pos

    def set_f_ratio_sub_point(self, sub_name, position=None, add=None):  # position は frame入力
        # print("frameからの設定")
        position = copy.deepcopy(position)  # 参照渡し防止用

        if not add is None:
            self.sub_point_f[sub_name] += add

        if not position is None:
            self.sub_point_f[sub_name] = copy.deepcopy(position)

        pos_px = self.f_to_px(self.sub_point_f[sub_name])
        #print("frameからの設定pos_px", pos_px)
        self.callback_operation.event("obj_sub_point", info=(sub_name, pos_px))  # 送るものはpx_pos
        return pos_px

    def set_px_ratio(self, position=None, size=None, sub_mov=False, left_move=False, right_move=False):
        frame_long_init = self.sta_end_f_init[1] - self.sta_end_f_init[0]

        old_ratio_f_pos = copy.deepcopy(self.ratio_f)

        pos_f, size_f = None, None

        # if not size is None and size < 1:
        #    size = 1

        if not position is None:
            self.ratio_f[0] = self.px_to_f(position)

        if not size is None:
            self.ratio_f[1] = self.px_to_f(size, size_bool=True)

        flag = ""

        if self.ratio_f[0] < self.sta_end_f_init[0]:  # posが0より手前になった
            old_pos = copy.deepcopy(self.ratio_f[0])
            self.ratio_f[0] = copy.deepcopy(self.sta_end_f_init[0])
            self.ratio_f[1] -= self.ratio_f[0] - old_pos if left_move else 0
            flag += "A"

        if self.ratio_f[1] > frame_long_init:  # sizeが幅を超えた
            self.ratio_f[0] = copy.deepcopy(self.sta_end_f_init[0])
            self.ratio_f[1] = copy.deepcopy(frame_long_init)

            flag += "B"

        if self.ratio_f[0] + self.ratio_f[1] > frame_long_init:
            self.ratio_f[0] = frame_long_init - self.ratio_f[1]
            flag += "C"

        if not flag == "":
            self.set_f_ratio(sub_mov=sub_mov)
            print(flag)
            return

        new_ratio_f_pos = copy.deepcopy(self.ratio_f)
        difference = new_ratio_f_pos[0] - old_ratio_f_pos[0] if sub_mov else 0

        for k in self.sub_point_f.keys():
            self.set_f_ratio_sub_point(k, add=difference)

        pos_completed = self.f_to_px(new_ratio_f_pos[0])
        size_completed = self.f_to_px(new_ratio_f_pos[1], size_bool=True)

        self.callback_operation.event("draw_func", info=(pos_completed, size_completed))
        #self.draw_func(position, size)

    def set_f_ratio(self, position=None, size=None, sub_mov=False):

        old_ratio_f_pos = copy.deepcopy(self.ratio_f)

        self.ratio_f = self.common_control.xy_compilation(self.ratio_f, x=position, y=size)

        pos_px = self.f_to_px(self.ratio_f[0])
        size_px = self.f_to_px(self.ratio_f[1], size_bool=True)

        new_ratio_f_pos = copy.deepcopy(self.ratio_f)
        difference = new_ratio_f_pos[0] - old_ratio_f_pos[0] if sub_mov else 0

        for k in self.sub_point_f.keys():
            self.set_f_ratio_sub_point(k, add=difference)

        self.callback_operation.event("draw_func", info=(pos_px + self.blank_space, size_px))

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
