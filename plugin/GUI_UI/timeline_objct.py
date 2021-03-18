import sys
import copy


class parts:
    def UI_set(self, data):

        data.value = 0
        data.click_flag = False

        data.new_diagram("bar")
        data.edit_diagram_size("bar", x=100, y=40)
        data.edit_diagram_position("bar", x=100, y=40)
        data.edit_diagram_color("bar", "#00ff00")
        data.territory_draw()

        def click_start(event):
            data.click_flag = True
            data.mouse_sta, data.mouse_touch_sta, data.diagram_join_sta = data.get_diagram_contact("bar")
            data.view_pos_sta = data.edit_diagram_position("bar")[0]
            data.view_size_sta = data.edit_diagram_size("bar")[0]

        def click_position(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("bar")

            now_mov = copy.deepcopy(now_mouse[0] - data.mouse_sta[0])

            if data.mouse_touch_sta[0][0]:
                pos = data.view_pos_sta+now_mov
                size = data.view_size_sta-now_mov

                data.pxf.edit_objct_motion(now_position=pos, now_size=size)
                # #print("左側移動")

            elif data.mouse_touch_sta[0][1]:
                data.pxf.edit_objct_motion(now_size=data.view_size_sta+now_mov)
                # #print("右側移動")

            elif data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                data.pxf.edit_objct_motion(now_position=now_mov+data.view_pos_sta)

        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("bar", del_mouse=True)
            _, _, data.diagram_join = data.get_diagram_contact("bar", del_mouse=True)

        data.add_diagram_event("bar", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_position)
        data.add_diagram_event("bar", "ButtonRelease-1", click_end)

        #data.edit_timeline_range = edit_timeline_range

        return data
