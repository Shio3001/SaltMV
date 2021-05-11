import copy


class parts:
    def UI_set(self, data):
        data.new_diagram("now")
        data.edit_diagram_size("now", x=0, y=20)
        data.edit_diagram_position("now", x=0, y=0)
        data.edit_diagram_color("now", "#ff0000")
        data.territory_draw()
        data.territory_stack(False)

        data.pxf = data.plus_px_frame_data(direction=0, debug_name="now")
        data.callback_operation = data.operation["plugin"]["other"]["callback"].CallBack()

        data.click_flag = True

        def draw(px_pos, _):
            data.edit_diagram_position("now", x=px_pos)
            data.territory_draw()

        data.pxf.set_draw_func(draw)

        data.pxf.init_set_sta_end_f(sta=0, end=100)
        data.pxf.set_sta_end_f(sta=0, end=100)
        data.pxf.set_sta_end_px(sta=0, end=100)
        data.pxf.set_px_ratio(size=2)

        """
        def click_start(event):
            data.click_flag = True
            data.mouse_sta, data.mouse_touch_sta, data.diagram_join_sta = data.get_diagram_contact("now")
            data.view_pos_sta = data.edit_diagram_position("now")[0]

            data.callback_operation.event("sta", info=data.pxf.get_event_data())
        """

        def click_position(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("now")

            if now_mouse[0] < 0:
                now_mouse[0] = 0

            if now_mouse[0] > data.edit_territory_size()[0]:
                now_mouse[0] = data.edit_territory_size()[0]

            # if data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
            data.pxf.set_px_ratio(position=now_mouse[0])

            data.callback_operation.event("mov", info=data.pxf.get_event_data())

        """
        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("now", del_mouse=True)
            _, _, data.diagram_join = data.get_diagram_contact("now", del_mouse=True)

            data.callback_operation.event("end", info=data.pxf.get_event_data())
        """

        #data.canvas_event_data.add_canvas_event("timeline", "Button-1", click_position)
        #data.canvas_event_data.add_canvas_event("timeline", "B1-Motion", click_position)
        data.canvas_event_data["add"]("timeline", "Button-1", click_position)
        data.canvas_event_data["add"]("timeline", "B1-Motion", click_position)

        return data
