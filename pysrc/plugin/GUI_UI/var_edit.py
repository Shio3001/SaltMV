class parts:
    def UI_set(self, UI_auxiliary):

        UI_auxiliary.value = 0
        UI_auxiliary.click_flag = False
        UI_auxiliary.discount = 0.5  # (0~1~2) #高いほど感度が高くなる
        UI_auxiliary.edit_range = [-100, 100]

        UI_auxiliary.new_diagram("value", diagram_type="text")
        UI_auxiliary.edit_diagram_text("value", text=0, center=True, font_size=20)
        UI_auxiliary.territory_draw()

        def edit_value(value):

            if value < UI_auxiliary.edit_range[0]:
                value = UI_auxiliary.edit_range[0]

            if value > UI_auxiliary.edit_range[1]:
                value = UI_auxiliary.edit_range[1]

            UI_auxiliary.value = value
            UI_auxiliary.edit_diagram_text("value", text=UI_auxiliary.value)
            UI_auxiliary.territory_draw()

        def click_start(event):
            UI_auxiliary.click_flag = True
            UI_auxiliary.mouse_sta, _, UI_auxiliary.diagram_join_sta = UI_auxiliary.get_diagram_contact("value")
            UI_auxiliary.view_pos_sta = UI_auxiliary.edit_diagram_position("value")

        def click_mov(event):
            if not UI_auxiliary.click_flag:
                return
            now_mouse, _, UI_auxiliary.diagram_join = UI_auxiliary.get_diagram_contact("value")
            if UI_auxiliary.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です

                now_mov = round((now_mouse[0] - UI_auxiliary.mouse_sta[0]) * UI_auxiliary.discount)
                edit_value(UI_auxiliary.value + now_mov)

        def click_end(event):
            UI_auxiliary.click_flag = False
            UI_auxiliary.mouse_sta, _, UI_auxiliary.diagram_join_sta = UI_auxiliary.get_diagram_contact("value", del_mouse=True)
            UI_auxiliary.mouse, _, UI_auxiliary.diagram_join = UI_auxiliary.get_diagram_contact("value", del_mouse=True)

        UI_auxiliary.add_diagram_event("value", "Button-1", click_start)
        UI_auxiliary.window_event_data["add"]("Motion", click_mov)
        UI_auxiliary.add_diagram_event("value", "ButtonRelease-1", click_end)

        return UI_auxiliary
