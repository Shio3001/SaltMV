import sys
import copy
import datetime


class parts:
    def UI_set(self, data):

        data.value = 0
        data.click_flag = False

        data.new_diagram("bar")
        data.edit_diagram_size("bar", x=100, y=20)
        data.edit_diagram_position("bar", x=100, y=0)
        data.edit_diagram_color("bar", "#00ff00")
        data.territory_draw()
        data.territory_stack(False)

        #data.obj_now_layer = 0

        data.timeline_objct_ID = None

        data.pxf = data.plus_px_frame_data(direction=0, debug_name="obj")

        def pos_set_y(pos_y):
            layer_pos = pos_y * data.edit_diagram_size("bar")[1]
            data.edit_diagram_position("bar", y=layer_pos)

            #print("layer_pos", layer_pos)

        #data.pos_add_y = pos_add_y

        def draw(px_pos, px_size):
            data.edit_diagram_position("bar", x=px_pos)
            data.edit_diagram_size("bar", x=px_size)

            data.territory_draw()

        data.pxf.set_draw_func(draw)

        data.callback_operation = data.operation["plugin"]["other"]["callback"].CallBack()

        def click_start(event):
            data.click_flag = True
            data.mouse_sta, data.mouse_touch_sta, data.diagram_join_sta = data.get_diagram_contact("bar")
            data.view_pos_sta = data.edit_diagram_position("bar")[0]
            data.view_size_sta = data.edit_diagram_size("bar")[0]

            data.callback_operation.event("sta", info=data.pxf.get_event_data())

        def click_position(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("bar")

            if now_mouse[0] < 0:
                now_mouse[0] = 0

            if now_mouse[0] > data.edit_territory_size()[0]:
                now_mouse[0] = data.edit_territory_size()[0]

            now_mov_x = copy.deepcopy(now_mouse[0] - data.mouse_sta[0])
            now_mov_y = copy.deepcopy(now_mouse[1] - data.mouse_sta[1])
            pos = data.view_pos_sta + now_mov_x

            if data.mouse_touch_sta[0][0]:  # 左側移動
                data.pxf.set_px_ratio(position=pos, size=data.view_size_sta-now_mov_x)

            elif data.mouse_touch_sta[0][1]:  # 右側移動
                data.pxf.set_px_ratio(position=data.view_pos_sta, size=data.view_size_sta+now_mov_x)

            elif data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                data.pxf.set_px_ratio(position=pos, size=data.view_size_sta)
                #after_pos = data.edit_diagram_position("bar")[1] + now_mov_y
                # print(after_pos)
                data.callback_operation.event("updown", info=(now_mov_y, data.option_data["media_id"], pos_set_y))

            data.callback_operation.event("mov", info=data.pxf.get_event_data())

        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("bar", del_mouse=True)
            _, _, data.diagram_join = data.get_diagram_contact("bar", del_mouse=True)

            data.callback_operation.event("end", info=data.pxf.get_event_data())

        data.add_diagram_event("bar", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_position)
        data.add_diagram_event("bar", "ButtonRelease-1", click_end)

        #data.edit_timeline_range = edit_timeline_range

        return data
