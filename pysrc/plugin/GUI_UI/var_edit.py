class parts:
    def UI_set(self, UI_data):

        UI_data.value = 0
        UI_data.click_flag = False
        UI_data.discount = 0.5  # (0~1~2) #高いほど感度が高くなる
        UI_data.edit_range = [-100, 100]

        UI_data.new_diagram("value", diagram_type="text")
        UI_data.edit_diagram_text("value", text=0, center=True, font_size=20)
        UI_data.territory_draw()

        def edit_value(value):

            if value < UI_data.edit_range[0]:
                value = UI_data.edit_range[0]

            if value > UI_data.edit_range[1]:
                value = UI_data.edit_range[1]

            UI_data.value = value
            UI_data.edit_diagram_text("value", text=UI_data.value)
            UI_data.territory_draw()

        def click_start(event):
            UI_data.click_flag = True
            UI_data.mouse_sta, _, UI_data.diagram_join_sta = UI_data.get_diagram_contact("value")
            UI_data.view_pos_sta = UI_data.edit_diagram_position("value")

        def click_mov(event):
            if not UI_data.click_flag:
                return
            now_mouse, _, UI_data.diagram_join = UI_data.get_diagram_contact("value")
            if UI_data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です

                now_mov = round((now_mouse[0] - UI_data.mouse_sta[0]) * UI_data.discount)
                edit_value(UI_data.value + now_mov)

        def click_end(event):
            UI_data.click_flag = False
            UI_data.mouse_sta, _, UI_data.diagram_join_sta = UI_data.get_diagram_contact("value", del_mouse=True)
            UI_data.mouse, _, UI_data.diagram_join = UI_data.get_diagram_contact("value", del_mouse=True)

        UI_data.add_diagram_event("value", "Button-1", click_start)
        UI_data.window_event_data["add"]("Motion", click_mov)
        UI_data.add_diagram_event("value", "ButtonRelease-1", click_end)

        return UI_data
