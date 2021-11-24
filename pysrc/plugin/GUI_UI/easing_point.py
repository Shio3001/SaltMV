import copy


class parts:
    def UI_set(self, UI_auxiliary):
        UI_auxiliary.edit_territory_position(x=0, y=0)
        UI_auxiliary.edit_territory_size(x=10, y=10)
        UI_auxiliary.new_diagram("point")
        UI_auxiliary.edit_diagram_size("point", 10, 10)
        UI_auxiliary.edit_diagram_fill("point", False)
        UI_auxiliary.edit_diagram_color("point", UI_auxiliary.GUI_alpha_color)
        UI_auxiliary.territory_draw()

        UI_auxiliary.mov_flag = False

        def click_start(e=None):
            UI_auxiliary.mov_flag = True
            UI_auxiliary.mouse_sta, _, _ = UI_auxiliary.get_diagram_contact("point")

            UI_auxiliary.view_pos_sta_x = copy.deepcopy(UI_auxiliary.edit_diagram_position("point")[0])
            UI_auxiliary.view_pos_sta_y = copy.deepcopy(UI_auxiliary.edit_diagram_position("point")[1])

        def click_mov(e=None):
            if not UI_auxiliary.mov_flag:
                return
            now_mouse, _, _ = UI_auxiliary.get_diagram_contact("point")
            now_mov_x = UI_auxiliary.view_pos_sta_x + now_mouse[0] - UI_auxiliary.mouse_sta[0]
            now_mov_y = UI_auxiliary.view_pos_sta_y + now_mouse[1] - UI_auxiliary.mouse_sta[1]

            print(now_mov_x, UI_auxiliary.view_pos_sta_x, now_mouse[0], UI_auxiliary.mouse_sta[0])

            UI_auxiliary.edit_diagram_position("point", x=now_mov_x, y=now_mov_y)
            UI_auxiliary.territory_draw()

        def click_end(e=None):
            if not UI_auxiliary.mov_flag:
                return
            UI_auxiliary.mov_flag = False

        UI_auxiliary.add_diagram_event("point", "Button-1", click_start)
        UI_auxiliary.window_event_data["add"]("Motion", click_mov)
        UI_auxiliary.add_diagram_event("point", "ButtonRelease-1", click_end)

        return UI_auxiliary
