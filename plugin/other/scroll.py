import copy


class CentralRole:
    def main(self, data, direction):

        data.direction = int(direction)

        data.new_diagram("back")
        data.new_diagram("view")

        data.edit_diagram_fill("back", True)
        data.edit_diagram_fill("view", False)

        data.edit_diagram_color("back", "#555555")
        data.edit_diagram_color("view", "#00cccc")

        data.edit_diagram_fill("view", True, direction=1-data.direction)

        # 百分率は0~100ではなく0~1でやること、100でやられるとしんどい

        data.lr_edit = False

        def set_lr_edit(select):
            data.lr_edit = select

        data.set_lr_edit = set_lr_edit
        # data.set_scroll_minimum_value_px = set_scroll_minimum_value_px

        data.pxf = data.plus_px_frame_data(direction=0, debug_name="scroll")

        def draw(px_pos, px_size):
            data.edit_diagram_position("view", x=px_pos)
            data.edit_diagram_size("view", x=px_size)

            data.territory_draw()

        data.pxf.set_sta_end_f(sta=0, end=100)
        data.pxf.set_draw_func(draw)

        data.scroll_event = None
        data.scroll_sta_event = None
        data.scroll_end_event = None

        def set_scroll_event(func):
            data.scroll_event = func
            data.scroll_event(data.pxf.ratio_f)

        def set_scroll_sta_event(func):
            data.scroll_sta_event = func
            data.scroll_event(data.pxf.ratio_f)

        def set_scroll_end_event(func):
            data.scroll_end_event = func
            data.scroll_event(data.pxf.ratio_f)

        data.set_scroll_event = set_scroll_event
        data.set_scroll_event(data.event_not_func)

        data.set_scroll_sta_event = set_scroll_sta_event
        data.set_scroll_sta_event(data.event_not_func)

        data.set_scroll_end_event = set_scroll_end_event
        data.set_scroll_end_event(data.event_not_func)

        def run_scroll_event():
            if not str(type(data.scroll_event)) == "<class 'function'>":
                return
            data.scroll_event(data.pxf.ratio_f)

        def run_scroll_sta_event():
            if not str(type(data.scroll_event)) == "<class 'function'>":
                return
            data.scroll_sta_event(data.pxf.ratio_f)

        def run_scroll_end_event():
            if not str(type(data.scroll_event)) == "<class 'function'>":
                return
            data.scroll_end_event(data.pxf.ratio_f)

            # print("pos決定", pos, size)

        data.pxf.set_draw_func(draw)

        # #print("scroll class ID", data)

        # s , a , b, e

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        data.click_flag = False

        def click_start(event):
            data.click_flag = True
            data.mouse_sta, data.mouse_touch_sta, data.diagram_join_sta = data.get_diagram_contact("view")
            data.view_pos_sta = copy.deepcopy(data.edit_diagram_position("view")[data.direction])
            data.view_size_sta = copy.deepcopy(data.edit_diagram_size("view")[data.direction])
            # クリックした場所から,パーセント起点まで、どれだけの距離があるかどうかを計算
            # 計算の基準は描画開始地点  data.drawing_area[0] : "# 配列0番 : territory起点からパーセント起点まで 実数表示!" です
            # つまりterritory起点+spaceからここまでどのぐらいの距離があるかどうかを判定します

            run_scroll_sta_event()

        def click_mov(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("view")
            now_mov = now_mouse[data.direction] - data.mouse_sta[data.direction]

            #print(now_mouse[data.direction], data.mouse_sta[data.direction])

            pos = data.view_pos_sta + now_mov

            if data.mouse_touch_sta[0][0]:  # 左側移動
                #print(now_mov, "A")
                data.pxf.set_px_ratio(position=pos, size=data.view_size_sta-now_mov)
                # #print("左側移動")

            elif data.mouse_touch_sta[0][1]:  # 右側移動
                data.pxf.set_px_ratio(size=data.view_size_sta+now_mov)
                #print(now_mov, "B")
                # #print("右側移動")

            elif data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                data.pxf.set_px_ratio(position=pos, size=data.view_size_sta)
                #print(now_mov, "C")

            run_scroll_event()

        def click_end(event):

            data.click_flag = False

            data.mouse_sta, data.mouse_touch_sta, data.diagram_join_sta = data.get_diagram_contact("view", del_mouse=True)
            _, _, data.diagram_join = data.get_diagram_contact("view", del_mouse=True)

            run_scroll_end_event()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        data.pxf.set_sta_end_px(sta=0, end=100, space=0)
        data.pxf.set_f_ratio(position=0, size=5)
        data.add_diagram_event("view", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_mov)
        data.add_diagram_event("view", "ButtonRelease-1", click_end)

        data.territory_draw()

        # data.edit_percent_movement = edit_percent_movement

        return data
