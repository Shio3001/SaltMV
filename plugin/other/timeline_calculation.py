import copy


class TimelineCalculation:
    def __init__(self, UI_common_control, territory, direction=None, obj_length=None, debug_name=None):
        self.sta_end_px = [0, 0]  # 実数表示 タイムラインがどこからどこまでを表示するかpxで保管します
        self.sta_end_frame = [0, 0]  # フレーム実数表示 タイムラインがどこからどこまで表示するかをframeで表示します

        #self.sta_end_size_px = [0, 0]

        self.slope = [0, 0]  # pos , size

        #self.slope_size = 0
        self.sta_size_obj_px = [0, 100]
        self.sta_size_obj_f = [0, 100]
        self.common_control = UI_common_control

        if direction is None:
            direction = 0
        self.direction = direction

        self.territory = territory

        self.one_f_px = 1

        self.draw_func = None

        if obj_length is None:
            obj_length = False
        self.obj_length = obj_length

        self.debug_name = debug_name

        # モチベが000000000000000000000000000

    def px_f_func(self, px_p, px_s=None):  # 送られたpxが何フレームか計算

        if 0 in self.slope and px_s is None:
            return 0

        if 0 in self.slope and not px_s is None:
            return [0, 0]

        f_p = (px_p - self.sta_end_px[0]) * self.slope[0] + self.sta_end_frame[0]

        if px_s is None:  # posだけ計算する場合
            return f_p

        f_s = px_s * self.slope[1]
        return [f_p, f_s]

    def f_px_func(self, f_p, f_s=None):  # 送られたframeが何pxか計算

        if 0 in self.slope and f_s is None:
            return 0

        if 0 in self.slope and not f_s is None:
            return [0, 0]

        px_p = (f_p - self.sta_end_frame[0]) / self.slope[0] + self.sta_end_px[0]

        if f_s is None:  # posだけ計算する場合
            return px_p

        px_s = f_s / self.slope[1]

        return [px_p, px_s]

        # if self.slope[0] == 0:
        #    px_p = self.sta_end_px[0]
        # else:

        # if f_s is None:
        #    return px_p

        # if self.slope[0] == 0:
        #    px_s = self.sta_end_px[0] - px_p
       # else:
        #    px_s = (f_p + f_s - self.sta_end_frame[0]) / self.slope[1] + self.sta_end_px[0] - px_p

        #px_ps = [px_p, px_s]
        # print(px_ps)

        # return px_ps

    def edit_range(self, sta_px=None, end_px=None, sta_f=None, end_f=None, size_type=None):  # 画面サイズが変更された時 #end_pxはサイズじゃなくて右端座標だよ！！！気をつけて

        if not sta_px is None:
            sta_px = sta_px-self.territory.position[self.direction]

        elif not end_px is None:
            end_px = end_px-self.territory.position[self.direction]

        # if not self.obj_length:
        #    size = 0

        size = 0

        self.sta_end_px = self.common_control.xy_compilation(self.sta_end_px, x=sta_px, y=end_px)
        self.sta_end_frame = self.common_control.xy_compilation(self.sta_end_frame, x=sta_f, y=end_f)

        sta_end_frame_length = self.sta_end_frame[1] - self.sta_end_frame[0]

        if self.obj_length and size_type == "f":
            length = (self.sta_end_px[1] - self.sta_end_px[0]) * self.sta_end_frame[1] / sta_end_frame_length
            size = length
            #print("フレームによるサイズ変更", length)

        if self.obj_length and size_type == "p":
            size = self.sta_size_obj_px[1]

        end_pos_px = self.sta_end_px[1] - size

        sta_end_px_length_pos = end_pos_px - self.sta_end_px[0]
        sta_end_px_length_size = self.sta_end_px[1] - self.sta_end_px[0]

        if sta_end_px_length_pos == 0:
            self.slope[0] = 0
            self.one_f_px = 0
            return

        self.slope = [sta_end_frame_length / sta_end_px_length_pos, sta_end_frame_length / sta_end_px_length_size]

        print("傾き", self.slope, self.debug_name)

        # print(self.slope)

        self.one_f_px = self.f_px_func(0, 1)[1]

    def set_draw_func(self, func):
        self.draw_func = func

    def __draw(self):
        pos, size = self.sta_size_obj_px

        if str(type(self.draw_func)) == "<class 'function'>":
            self.draw_func(pos, size)

    def limits_size_1_frame(self, now_position=None, now_size=None):
        position = copy.deepcopy(now_position)
        size = copy.deepcopy(now_size)

        if size is None:
            size = self.sta_size_obj_px[1]

        if size < self.one_f_px and not position is None:
            # print("作動A", size)
            position = position - (self.one_f_px - size)

        elif size < self.one_f_px:
            # print("作動B", size)
            size = self.one_f_px

        return position, size

    def limits_size_max_frame(self):
        pass
        # print("反応A")

    def limits_size_1_px(self):
        if self.one_f_px > self.sta_size_obj_px[1]:  # もし1フレームぶんのpxよりサイズが小さかったら
            self.sta_size_obj_px[1] = self.one_f_px

            print("反応B", self.debug_name)

    def limits_position_0_frame(self):

        if self.sta_size_obj_f[0] < 0:  # もし0frame以下なら
            self.sta_size_obj_px[0] = self.f_px_func(0)
            self.sta_size_obj_f[0] = 0

            print("反応C", self.debug_name)

    def limits_position_max_frame(self):
        if self.sta_size_obj_f[0] > self.sta_end_frame[1]:
            self.sta_size_obj_px[0] = self.f_px_func(self.sta_end_frame[1])
            self.sta_size_obj_f[0] = self.sta_end_frame[1]

            print("反応D", self.debug_name)

    def edit_objct_motion(self, now_position=None, now_size=None):  # 移動量指定
        now_position, now_size = self.limits_size_1_frame(now_position, now_size)

        self.sta_size_obj_px = self.common_control.xy_compilation(self.sta_size_obj_px, x=now_position, y=now_size)
        self.limits_size_1_px()

        if not now_size is None:
            self.edit_range()

        self.sta_size_obj_f = self.px_f_func(self.sta_size_obj_px[0], self.sta_size_obj_px[1])

        self.limits_position_0_frame()
        self.limits_position_max_frame()

        self.__draw()

        print("移動形式A", self.debug_name)

        return

    def edit_objct_frame(self, position=None, size=None):  # フレーム実数指定
        self.sta_size_obj_f = self.common_control.xy_compilation(self.sta_size_obj_f, x=position, y=size)

        # print("反応SW")
        self.edit_range()

        self.sta_size_obj_px = self.f_px_func(self.sta_size_obj_f[0], self.sta_size_obj_f[1])

        self.limits_position_0_frame()
        self.limits_position_max_frame()
        self.__draw()

        print("移動形式B", self.debug_name)

        return
