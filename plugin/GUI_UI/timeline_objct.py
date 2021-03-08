import sys
import copy


class parts:
    def UI_set(self, data):

        data.value = 0
        data.click_flag = False

        #data.all_data.scene().editor["len"] = 各シーン長さ

        data.timeline_obj_range = [0, 100]  # フレームに対する実数表示！ タイムラインに対してどれだけ占めるかを計算します #開始地点 ,サイズ
        data.timeline_view_range = [0, 100]  # フレームに対する実数表示！ #タイムラインが、現在どこからどこまでの割合で表示しているかを"フレームに対して"記録します #開始地点 ,終了地点

        # 上二つどちらもフレームに対する実数表示にすれば楽かもしれないけど、今度はフレームに対する実数表示のための変換もいるのか、しんどすぎる

        data.new_diagram("bar")
        data.edit_diagram_size("bar", x=100, y=40)
        data.edit_diagram_position("bar", x=100, y=40)
        data.edit_diagram_color("bar", "#00ff00")
        data.territory_draw()

        def edit_timeline_range(sta, end):  # 画面サイズが変更された時
            data.timeline_view_range = [sta, end]
            data.territory_draw()

        def edit_objct_motion(now_position=None, now_size=None):
            data.edit_diagram_position("bar", x=now_position)
            data.edit_diagram_size("bar", x=now_size)
            frame_calculation(tuple(now_position, now_size))
            data.territory_draw()

        def edit_objct_percentage(position=None, size=None):
            pass

        def frame_calculation(obj_view_range):  # 実数座標(描画座標から) -> frame実数
            obj_pos, obj_size = obj_view_range

            #timeline_view_length = data.timeline_view_range[1] - data.timeline_view_range[0]

            # view_obj_sta = obj_view_range[0] / timeline_view_length  # 割合
            # view_obj_size = obj_view_range[1] / timeline_view_length  # 割合

        def coordinate_calculation():  # frame実数 -> 実数座標(描画座標へ)
            pass

        def click_start(event):
            data.click_flag = True
            data.mouse_sta, data.mouse_touch_sta, data.diagram_join_sta = data.get_diagram_contact("bar")
            data.view_pos_sta = data.edit_diagram_position("bar")
            data.view_size_sta = data.edit_diagram_size("bar")

        def click_position(event):
            if not data.click_flag:
                return
            now_mouse, _, data.diagram_join = data.get_diagram_contact("bar")

            now_mov = copy.deepcopy(now_mouse[0] - data.mouse_sta[0])

            if data.mouse_touch_sta[0][0]:
                edit_objct_motion(now_position=data.view_pos_sta[0]+now_mov, now_size=data.view_size_sta[0]-now_mov)
                print("左側移動")

            elif data.mouse_touch_sta[0][1]:
                edit_objct_motion(now_size=data.view_size_sta[0]+now_mov)
                print("右側移動")

            elif data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                edit_objct_motion(now_position=now_mov+data.view_pos_sta[0])

        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("bar", del_mouse=True)
            data.mouse, _, data.diagram_join = data.get_diagram_contact("bar", del_mouse=True)

        data.add_diagram_event("bar", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_position)
        data.add_diagram_event("bar", "ButtonRelease-1", click_end)

        return data
