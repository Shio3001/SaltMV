import copy
import inspect


class parts:
    def UI_set(self, UI_data):
        UI_data.new_diagram("now")
        UI_data.edit_diagram_size("now", x=0, y=20)
        UI_data.edit_diagram_position("now", x=0, y=0)
        UI_data.edit_diagram_color("now", "#ff0000")
        UI_data.territory_draw()
        UI_data.territory_stack(False)

        UI_data.pxf = UI_data.plus_px_frame_data(direction=0, debug_name="now")
        UI_data.callback_operation = UI_data.operation["plugin"]["other"]["callback"].CallBack()

        UI_data.click_flag = True

        def draw(info):
            px_pos, _ = info
            # print("実際の描画発火")
            UI_data.edit_diagram_position("now", x=px_pos)
            UI_data.territory_draw()

        UI_data.pxf.callback_operation.set_event("draw_func", draw)

        UI_data.pxf.init_set_sta_end_f(sta=0, end=100)
        UI_data.pxf.set_sta_end_f(sta=0, end=100)
        UI_data.pxf.set_sta_end_px(sta=0, end=100)
        UI_data.pxf.set_px_ratio(size=2)

        """
        def click_start(event):
            UI_data.click_flag = True
            UI_data.mouse_sta, UI_data.mouse_touch_sta, UI_data.diagram_join_sta = UI_data.get_diagram_contact("now")
            UI_data.view_pos_sta = UI_data.edit_diagram_position("now")[0]

            UI_data.callback_operation.event("sta", info=UI_data.pxf.get_event_data())
        """

        def preview_frame_set(frame):
            UI_data.pxf.set_f_ratio(position=frame)

        def frame_set(frame):
            #print("A", inspect.stack()[1].filename, inspect.stack()[1].function)
            UI_data.pxf.set_f_ratio(position=frame)
            UI_data.callback_operation.event("mov", info=UI_data.pxf.get_event_data())

        UI_data.frame_set = frame_set
        UI_data.preview_frame_set = preview_frame_set

        #UI_data.scene_change_flag = True

        UI_data.mov_flag = False

        # mov_flagは内部用
        # click_flagは外部干渉用

        def click_start(event):
            #print("呼び出し先[nowtime申請]", inspect.stack()[1].filename, inspect.stack()[1].function)
            print("nowtime[申請] click_start")

            if not UI_data.click_flag:
                return

            if not UI_data.get_permission_elapsed_time():
                print("get_permission_elapsed_time否定")
                return

            UI_data.mov_flag = True

            print("nowtime click_start")

            click_position()

        def click_position(event=None):

            print("nowtime[申請] click_position")

            if not UI_data.mov_flag or not UI_data.click_flag:
                UI_data.mov_flag = False
                return

            print("nowtime click_position")

            now_mouse, _, UI_data.diagram_join = UI_data.get_diagram_contact("now")

            if now_mouse[0] < 0:
                now_mouse[0] = 0

            if now_mouse[0] > UI_data.edit_territory_size()[0]:
                now_mouse[0] = UI_data.edit_territory_size()[0]

            # if UI_data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
            UI_data.pxf.set_px_ratio(position=now_mouse[0])
            UI_data.callback_operation.event("mov", info=UI_data.pxf.get_event_data())

        def click_end(event):
            print("nowtime click_end")

            UI_data.mov_flag = False

        """
        def click_end(event):
            UI_data.click_flag = False
            UI_data.mouse_sta, _, UI_data.diagram_join_sta = UI_data.get_diagram_contact("now", del_mouse=True)
            _, _, UI_data.diagram_join = UI_data.get_diagram_contact("now", del_mouse=True)

            UI_data.callback_operation.event("end", info=UI_data.pxf.get_event_data())
        """

        #UI_data.canvas_event_UI_data.add_canvas_event("timeline", "Button-1", click_position)
        #UI_data.canvas_event_UI_data.add_canvas_event("timeline", "B1-Motion", click_position)
        UI_data.canvas_event_data["add"]("timeline", "Button-1", click_start)
        UI_data.canvas_event_data["add"]("timeline", "B1-Motion", click_position)
        UI_data.canvas_event_data["add"]("timeline", "ButtonRelease-1", click_end)

        return UI_data
