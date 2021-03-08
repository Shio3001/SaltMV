class parts:
    def UI_set(self, data):

        data.value = 0
        data.click_flag = False
        data.discount = 0.5  # (0~1~2) #高いほど感度が高くなる
        data.edit_range = [-100, 100]

        data.new_diagram("value", diagram_type="text")
        data.edit_diagram_text("value", text=0, center=True, font_size=20)
        data.territory_draw()

        def edit_value(value):

            if value < data.edit_range[0]:
                value = data.edit_range[0]

            if value > data.edit_range[1]:
                value = data.edit_range[1]

            data.value = value
            data.edit_diagram_text("value", text=data.value)
            data.territory_draw()

        def click_start(event):
            data.click_flag = True
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("value")
            data.view_pos_sta = data.edit_diagram_position("value")

        def click_mov(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("value")
            if data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です

                now_mov = round((now_mouse[0] - data.mouse_sta[0]) * data.discount)
                edit_value(data.value + now_mov)

        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("value", del_mouse=True)
            data.mouse, _, data.diagram_join = data.get_diagram_contact("value", del_mouse=True)

        data.add_diagram_event("value", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_mov)
        data.add_diagram_event("value", "ButtonRelease-1", click_end)

        return data
