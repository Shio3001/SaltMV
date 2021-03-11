import copy


class TimelineCalculation:
    def __init__(self, UI_common_control, territory, direction=0, mi=None):
        self.sta_end_px = [0, 0]  # 実数表示 タイムラインがどこからどこまでを表示するかpxで保管します
        self.sta_end_frame = [0, 0]  # フレーム実数表示 タイムラインがどこからどこまで表示するかをframeで表示します
        self.slope = 0
        self.sta_end_obj_px = [0, 100]
        self.sta_end_obj_f = [self.px_f_func(self.sta_end_obj_px[0]), self.px_f_func(self.sta_end_obj_px[1])]
        self.common_control = UI_common_control
        #self.UI_data = UI_data
        self.direction = direction
        print("t", territory)
        print(mi)
        self.territory = territory
        # print(self.territory)

        self.one_f_px = 1

        self.draw_func = None

    def px_f_func(self, px_p, px_s=None):  # 送られたpxが何フレームか計算
        f_p = (px_p - self.territory.position[self.direction] - self.sta_end_px[0]) * self.slope + self.sta_end_frame[0]

        if px_s is None:
            return f_p

        f_s = (px_p + px_s - self.sta_end_px[0]) * self.slope + self.sta_end_frame[0] - f_p
        f_ps = [f_p, f_s]
        return f_ps

    def f_px_func(self, f_p, f_s=None):  # 送られたframeが何pxか計算
        if self.slope == 0:
            px_p = self.sta_end_px[0]
        else:
            px_p = (f_p - self.sta_end_frame[0]) / self.slope + self.sta_end_px[0]
        if f_s is None:
            return px_p - self.territory.position[self.direction]

        if self.slope == 0:
            px_s = self.sta_end_px[0] - px_p
        else:
            px_s = (f_p + f_s - self.sta_end_frame[0]) / self.slope + self.sta_end_px[0] - px_p

        px_ps = [px_p - self.territory.position[self.direction], px_s]
        print(px_ps)

        return px_ps

    def edit_range(self, sta_px=None, end_px=None, sta_f=None, end_f=None):  # 画面サイズが変更された時 #end_pxはサイズじゃなくて右端座標だよ！！！気をつけて
        self.sta_end_px = self.common_control.xy_compilation(self.sta_end_px, x=sta_px, y=end_px)
        self.sta_end_frame = self.common_control.xy_compilation(self.sta_end_frame, x=sta_f, y=end_f)
        self.slope = (self.sta_end_frame[1] - self.sta_end_frame[0]) / (self.sta_end_px[1] - self.sta_end_px[0])  # 一次関数を計算

        print(self.slope)

        self.one_f_px = self.f_px_func(0, 1)[1]

    def set_draw_func(self, func):
        self.draw_func = func

    def __draw(self):
        pos, size = self.sta_end_obj_px

        if str(type(self.draw_func)) == "<class 'function'>":
            self.draw_func(pos, size)

    def limits_size_1_frame(self, now_position=None, now_size=None):
        position = copy.deepcopy(now_position)
        size = copy.deepcopy(now_size)

        # posの変更によって1フレームを下回らないようにする
        if position is None:
            return position, size

        if size is None:
            size = self.sta_end_obj_px[1]

        if size < self.one_f_px:
            position = position - (self.one_f_px - size)

        return position, size

    def limits_size_max_frame(self):
        pass

    def limits_size_1_px(self):
        if self.one_f_px > self.sta_end_obj_px[1]:  # もし1フレームぶんのpxよりサイズが小さかったら
            self.sta_end_obj_px[1] = self.one_f_px

    def limits_position_0_frame(self):
        if self.sta_end_obj_f[0] < 0:  # もし0frame以下なら
            self.sta_end_obj_px[0] = self.f_px_func(0)
            self.sta_end_obj_f[0] = 0

    def limits_position_max_frame(self):
        pass

    def edit_objct_motion(self, now_position=None, now_size=None):  # 移動量指定
        now_position, now_size = self.limits_size_1_frame(now_position, now_size)
        self.sta_end_obj_px = self.common_control.xy_compilation(self.sta_end_obj_px, x=now_position, y=now_size)
        self.sta_end_obj_f = self.px_f_func(self.sta_end_obj_px[0], self.sta_end_obj_px[1])

        self.limits_position_0_frame()
        self.__draw()
        return

    def edit_objct_frame(self, position=None, size=None):  # フレーム実数指定
        self.sta_end_obj_f = self.common_control.xy_compilation(self.sta_end_obj_f, x=position, y=size)
        self.sta_end_obj_px = self.f_px_func(self.sta_end_obj_f[0], self.sta_end_obj_f[1])
        self.limits_position_0_frame()
        self.__draw()

        return
