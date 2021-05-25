import sys
import copy
import datetime
import threading
import uuid


class KeyFrame:
    def __init__(self, data, size, center_x, center_y):
        self.data = data
        self.uu_id = self.data.all_data.elements.make_id("keyframe")
        data.new_diagram(self.uu_id)
        data.set_shape_rhombus(self.uu_id, size, 100, 100)  # ひし形
        data.diagram_draw(self.uu_id)
        data.edit_diagram_color(self.uu_id, "#ffff00")

        now_mouse, _, _ = data.get_diagram_contact(self.uu_id)

        data.pxf.set_sub_point(self.uu_id)
        data.pxf.set_px_ratio_sub_point(self.uu_id, now_mouse[0])

        print("KeyFrame生成")

        def draw(send):
            sub_name, pos_px = send
            data.edit_diagram_position(sub_name, x=pos_px)
            print("KeyFrame描画", pos_px)

        data.pxf.callback_operation.set_event("obj_sub_point", draw)


class parts:
    def UI_set(self, data):  # data ←継承元(ファイルが違う＋プラグイン形式なのでこのような形に)

        data.value = 0
        data.click_flag = False

        data.new_diagram("bar")
        data.edit_diagram_size("bar", x=100, y=20)
        data.edit_diagram_position("bar", x=100, y=0)
        data.edit_diagram_color("bar", "#00ff00")
        data.territory_draw()
        data.territory_stack(False)

        # data.obj_now_layer = 0

        # data.timeline_object_ID = None

        data.pxf = data.plus_px_frame_data(direction=0, debug_name="obj")

        def edit_layer(layer_number):
            layer_pos = layer_number * data.edit_diagram_size("bar")[1]
            data.edit_diagram_position("bar", y=layer_pos)

        data.edit_layer = edit_layer
        # print("layer_pos", layer_pos)

        # data.pos_add_y = pos_add_y

        def draw(info):
            px_pos, px_size = info
            data.edit_diagram_position("bar", x=px_pos)
            data.edit_diagram_size("bar", x=px_size)

            data.territory_draw()

        data.pxf.callback_operation.set_event("draw_func", draw)
        # data.pxf.set_draw_func(draw)

        def media_object_del():
            data.callback_operation.event("end", info=data.pxf.get_event_data())
            data.callback_operation.event("del", data.option_data["media_id"])

        def media_object_separate():
            data.callback_operation.event("separate", data.option_data["media_id"])

        def add_key_frame():
            bar_pos = data.edit_diagram_position("bar")
            size = data.edit_diagram_size("bar")[1] / 2
            center_x = bar_pos[0]
            center_y = bar_pos[1] - (data.edit_diagram_size("bar")[1] / 2)
            KeyFrame(data, size, center_x, center_y)

        self.popup = data.operation["plugin"]["other"]["menu_popup"].MenuPopup(data.window, popup=True)

        effect_dict = data.operation["plugin"]["effect"]

        effect_user_list = ["エフェクト"]

        for k in effect_dict.keys():
            effect_get = EffectGet(data.all_data, data.option_data["media_id"], k)
            effect_user_list.append(k)
            effect_user_list.append(effect_get.add_element)

        popup_list = [effect_user_list, ("分割", media_object_separate), ("削除", media_object_del), ("中間点追加", add_key_frame)]
        self.popup.set(popup_list)

        def right_click(event):
            mouse, _, _, xy = data.window_event_data["contact"]()
            for i in range(2):
                mouse[i] += xy[i]

            self.popup.show(mouse[0], mouse[1])

        data.add_diagram_event("bar", "Button-2", right_click)

        # popup_list = [("ファイル", "終了", self.data.window_exit), ("新規", "シーン", None, "レイヤー", new_layer), ("追加", "動画", new_obj)]
        # self.popup.set(popup_list)
        data.callback_operation = data.operation["plugin"]["other"]["callback"].CallBack()

        data.media_object_parameter_bool = True

        # def set_parameter_permit(flag_bool):
        #    data.media_object_parameter_bool = flag_bool
        #    print("非同期 :", flag_bool)

        def click_start(event):
            data.click_flag = True
            data.mouse_sta, data.mouse_touch_sta, data.diagram_join_sta = data.get_diagram_contact("bar")
            data.view_pos_sta = data.edit_diagram_position("bar")[0]
            data.view_size_sta = data.edit_diagram_size("bar")[0]

            data.edit_diagram_color("bar", "#ff0000")

            data.callback_operation.event("sta", info=data.pxf.get_event_data())

            # set_parameter_permit(False)
            print("非同期開始")
            send = (data.all_data.media_object(data.option_data["media_id"]).effect_group, data.all_data.now_time)
            func = data.all_data.callback_operation.get_event("media_lord")[0]
            thread_1 = data.all_data.threading.Thread(target=func, args=(send,))
            thread_1.start()

            print("非同期")

        def click_position(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("bar")

            # if now_mouse[0] < 0:
            #    now_mouse[0] = 0

            # if now_mouse[0] > data.edit_territory_size()[0]:
            #    now_mouse[0] = data.edit_territory_size()[0]

            now_mov_x = copy.deepcopy(now_mouse[0] - data.mouse_sta[0])
            now_mov_y = copy.deepcopy(now_mouse[1] - data.mouse_sta[1])
            pos = data.view_pos_sta + now_mov_x

            if data.mouse_touch_sta[0][0]:  # 左側移動
                data.pxf.set_px_ratio(position=pos, size=data.view_size_sta-now_mov_x)

            elif data.mouse_touch_sta[0][1]:  # 右側移動
                data.pxf.set_px_ratio(position=data.view_pos_sta, size=data.view_size_sta+now_mov_x)

            elif data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                data.pxf.set_px_ratio(position=pos, size=data.view_size_sta)
                # after_pos = data.edit_diagram_position("bar")[1] + now_mov_y
                # #print(after_pos)
                # print("発火A", data.option_data["media_id"])
                data.callback_operation.event("updown", info=(now_mov_y, data.option_data["media_id"], edit_layer, click_start))

            data.callback_operation.event("mov", info=data.pxf.get_event_data())

        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("bar", del_mouse=True)
            _, _, data.diagram_join = data.get_diagram_contact("bar", del_mouse=True)

            data.callback_operation.event("end", info=data.pxf.get_event_data())

            data.edit_diagram_color("bar", "#00ff00")

        data.add_diagram_event("bar", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_position)
        data.add_diagram_event("bar", "ButtonRelease-1", click_end)

        # data.all_del_diagram_event("bar")

        # data.del_diagram_event("bar", "ButtonRelease-1", click_end)

        # data.edit_timeline_range = edit_timeline_range

        return data


class EffectGet:
    def __init__(self, all_data, media_id, effect_key):
        self.all_data = all_data
        self.effect_key = effect_key
        self.media_id = media_id

    def add_element(self):
        self.all_data.add_effect_elements(self.media_id, self.effect_key)
