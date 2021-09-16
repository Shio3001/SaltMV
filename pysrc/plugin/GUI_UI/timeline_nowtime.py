import copy
import inspect


class parts:
    def UI_set(self, UI_auxiliary):
        UI_auxiliary.new_diagram("now")
        UI_auxiliary.edit_diagram_size("now", x=0, y=20)
        UI_auxiliary.edit_diagram_position("now", x=0, y=0)
        UI_auxiliary.edit_diagram_color("now", "#ff0000")
        UI_auxiliary.territory_draw()
        UI_auxiliary.territory_stack(False)

        UI_auxiliary.pxf = UI_auxiliary.plus_px_frame_data(direction=0, debug_name="now")
        UI_auxiliary.callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()

        UI_auxiliary.click_flag = True

        def draw(info):
            px_pos, _ = info
            # print("実際の描画発火")
            UI_auxiliary.edit_diagram_position("now", x=px_pos)
            UI_auxiliary.territory_draw()

        UI_auxiliary.pxf.callback_operation.set_event("draw_func", draw)

        UI_auxiliary.pxf.init_set_sta_end_f(sta=0, end=100)
        UI_auxiliary.pxf.set_sta_end_f(sta=0, end=100)
        UI_auxiliary.pxf.set_sta_end_px(sta=0, end=100)
        UI_auxiliary.pxf.set_px_ratio(size=2)

        """
        def click_start(event):
            UI_auxiliary.click_flag = True
            UI_auxiliary.mouse_sta, UI_auxiliary.mouse_touch_sta, UI_auxiliary.diagram_join_sta = UI_auxiliary.get_diagram_contact("now")
            UI_auxiliary.view_pos_sta = UI_auxiliary.edit_diagram_position("now")[0]

            UI_auxiliary.callback_operation.event("sta", info=UI_auxiliary.pxf.get_event_data())
        """

        def preview_frame_set(frame):
            UI_auxiliary.pxf.set_f_ratio(position=frame)

        def frame_set(frame):
            #print("A", inspect.stack()[1].filename, inspect.stack()[1].function)
            UI_auxiliary.pxf.set_f_ratio(position=frame)
            UI_auxiliary.callback_operation.event("mov", info=UI_auxiliary.pxf.get_event_data())

        UI_auxiliary.frame_set = frame_set
        UI_auxiliary.preview_frame_set = preview_frame_set

        #UI_auxiliary.scene_change_flag = True

        UI_auxiliary.mov_flag = False
        UI_auxiliary.click_flag = True

        # mov_flagは内部用
        # click_flagは外部干渉用

        def one_lock():
            UI_auxiliary.click_flag = False

        UI_auxiliary.one_lock = one_lock

        def click_start(event):
            #print("呼び出し先[nowtime申請]", inspect.stack()[1].filename, inspect.stack()[1].function)
            print("nowtime[申請] click_start")

            if not UI_auxiliary.click_flag:
                UI_auxiliary.click_flag = True
                return

            if not UI_auxiliary.get_permission_elapsed_time():
                print("get_permission_elapsed_time否定")
                return

            UI_auxiliary.mov_flag = True

            print("nowtime click_start")

            click_position()

        def click_position(event=None):

            print("nowtime[申請] click_position")

            if not UI_auxiliary.mov_flag or not UI_auxiliary.click_flag:
                UI_auxiliary.mov_flag = False
                return

            print("nowtime click_position")

            now_mouse, _, UI_auxiliary.diagram_join = UI_auxiliary.get_diagram_contact("now")

            if now_mouse[0] < 0:
                now_mouse[0] = 0

            if now_mouse[0] > UI_auxiliary.edit_territory_size()[0]:
                now_mouse[0] = UI_auxiliary.edit_territory_size()[0]

            # if UI_auxiliary.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
            UI_auxiliary.pxf.set_px_ratio(position=now_mouse[0])
            UI_auxiliary.callback_operation.event("mov", info=UI_auxiliary.pxf.get_event_data())

        def click_end(event):
            print("nowtime click_end")

            UI_auxiliary.mov_flag = False

        """
        def click_end(event):
            UI_auxiliary.click_flag = False
            UI_auxiliary.mouse_sta, _, UI_auxiliary.diagram_join_sta = UI_auxiliary.get_diagram_contact("now", del_mouse=True)
            _, _, UI_auxiliary.diagram_join = UI_auxiliary.get_diagram_contact("now", del_mouse=True)

            UI_auxiliary.callback_operation.event("end", info=UI_auxiliary.pxf.get_event_data())
        """

        #UI_auxiliary.canvas_event_UI_auxiliary.add_canvas_event("timeline", "Button-1", click_position)
        #UI_auxiliary.canvas_event_UI_auxiliary.add_canvas_event("timeline", "B1-Motion", click_position)
        UI_auxiliary.canvas_event_data["add"]("timeline", "Button-1", click_start)
        UI_auxiliary.canvas_event_data["add"]("timeline", "B1-Motion", click_position)
        UI_auxiliary.canvas_event_data["add"]("timeline", "ButtonRelease-1", click_end)

        return UI_auxiliary
