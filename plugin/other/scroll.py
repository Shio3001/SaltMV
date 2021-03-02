class CentralRole:
    def main(self, data, direction):

        data.direction = int(direction)

        data.new_territory("main")
        data.new_diagram("main", "back")
        data.new_diagram("main", "view")

        data.edit_diagram_fill("main", "back", True)
        data.edit_diagram_fill("main", "view", False)

        data.edit_diagram_color("main", "view", "#00ffff")

        data.edit_diagram_fill("main", "view", True, direction=1-data.direction)

        # 百分率は0~100ではなく0~1でやること、100でやられるとしんどい

        data.drawing_area = [0, 0]
        # territory左上を0,0とした基準で、描画可能範囲を記入します
        # 配列0番 : territory+space起点からパーセント起点まで 実数表示!
        # 配列1番 : territory+space起点からterritory終点-spaceまで 実数表示!

        data.pos_drawing_area = [0, 0]  # 実数表示!
        # data.drawing_areaを元にした座標の移動範囲を計算します
        # 計算方法は (1 - サイズ割合)をかけることです

        data.percent_range = [0, 0]
        # 配列0番 : territory起点からパーセント中心まで 割合表示！
        # 配列1番 : パーセントのサイズ 割合表示！

        data.click_distance = 0
        # クリックした場所から,パーセント起点まで、どれだけの距離があるかどうかを計算 実数表示！

        data.brack_space = 0
        # data.directionによって指定された方向の両側に,data.brack_spaceのスペースを作ります
        # これにより描画禁止領域をdiagramに設定することができます

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        def eidt_size(x=None, y=None, space=None):

            if not space is None:
                data.brack_space = space

            data.edit_territory_size("main", x=x, y=y)

            data.drawing_area[0] = data.edit_territory_position("main")[data.direction] + data.brack_space
            data.drawing_area[1] = data.edit_territory_position("main")[data.direction] + data.edit_territory_size("main")[data.direction] - data.brack_space

            edit_percent()

            data.territory_draw("main")

        def edit_percent(position=None, size=None):
            data.percent_range = data.common_control.xy_compilation(data.percent_range, x=position, y=size)

            data.pos_drawing_area[0] = data.drawing_area[0]
            data.pos_drawing_area[1] = data.drawing_area[1] * (1 - data.percent_range[1])

            print(data.drawing_area, data.pos_drawing_area)

            pos_length = data.pos_drawing_area[1] - data.pos_drawing_area[0]
            size_length = data.drawing_area[1] - data.drawing_area[0]

            sta = pos_length * data.percent_range[0]
            end = size_length * data.percent_range[1]

            sta_xy = [None, None]
            end_xy = [None, None]

            sta_xy[data.direction] = sta
            end_xy[data.direction] = end

            print(sta, end, data.percent_range)

            data.edit_diagram_position("main", "view", x=sta_xy[0], y=sta_xy[1])
            data.edit_diagram_size("main", "view", x=end_xy[0], y=end_xy[1])

            # print(data.pos_drawing_area)

            data.territory_draw("main")

            return

        data.click_flag = False

        def click_start(event):
            data.click_flag = True
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("main", "view")
            data.click_distance = data.mouse_sta[data.direction] - data.drawing_area[0]
            # クリックした場所から,パーセント起点まで、どれだけの距離があるかどうかを計算
            # 計算の基準は描画開始地点  data.drawing_area[0] : "# 配列0番 : territory起点からパーセント起点まで 実数表示!" です
            # つまりterritory起点+spaceからここまでどのぐらいの距離があるかどうかを判定します

        def click_mov(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("main", "view")
            if data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                now_pos = (now_mouse[data.direction] - data.drawing_area[0]) / (data.drawing_area[1] - data.drawing_area[0])

                edit_percent(position=now_pos)

        def click_end(event):

            data.click_flag = False

            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("main", "view", del_mouse=True)
            data.mouse, _, data.diagram_join = data.get_diagram_contact("main", "view", del_mouse=True)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        eidt_size(x=20, y=400)
        edit_percent(position=0.25, size=0.25)
        data.add_diagram_event("main", "view", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_mov)
        data.add_diagram_event("main", "view", "ButtonRelease-1", click_end)

        data.territory_draw("main")

        return data
