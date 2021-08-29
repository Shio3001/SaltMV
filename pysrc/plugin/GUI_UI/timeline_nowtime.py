import copy
import inspect


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

        def draw(info):
            px_pos, _ = info
            # print("実際の描画発火")
            data.edit_diagram_position("now", x=px_pos)
            data.territory_draw()

        data.pxf.callback_operation.set_event("draw_func", draw)

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

        def preview_frame_set(frame):
            data.pxf.set_f_ratio(position=frame)

        def frame_set(frame):
            #print("A", inspect.stack()[1].filename, inspect.stack()[1].function)
            data.pxf.set_f_ratio(position=frame)
            data.callback_operation.event("mov", info=data.pxf.get_event_data())

        data.frame_set = frame_set
        data.preview_frame_set = preview_frame_set

        #data.scene_change_flag = True

        data.mov_flag = False

        # mov_flagは内部用
        # click_flagは外部干渉用

        def click_start(event):
            if not data.click_flag:
                return

            data.mov_flag = True

            click_position()

        def click_position(event=None):

            if not data.mov_flag or not data.click_flag:
                data.mov_flag = False
                return

            now_mouse, _, data.diagram_join = data.get_diagram_contact("now")

            if now_mouse[0] < 0:
                now_mouse[0] = 0

            if now_mouse[0] > data.edit_territory_size()[0]:
                now_mouse[0] = data.edit_territory_size()[0]

            # if data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
            data.pxf.set_px_ratio(position=now_mouse[0])
            data.callback_operation.event("mov", info=data.pxf.get_event_data())

        def click_end(event):
            data.mov_flag = False

        """
        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("now", del_mouse=True)
            _, _, data.diagram_join = data.get_diagram_contact("now", del_mouse=True)

            data.callback_operation.event("end", info=data.pxf.get_event_data())
        """

        #data.canvas_event_data.add_canvas_event("timeline", "Button-1", click_position)
        #data.canvas_event_data.add_canvas_event("timeline", "B1-Motion", click_position)
        data.canvas_event_data["add"]("timeline", "Button-1", click_start)
        data.canvas_event_data["add"]("timeline", "B1-Motion", click_position)
        data.canvas_event_data["add"]("timeline", "ButtonRelease-1", click_end)

        return data
