import sys
import copy


class parts:
    def UI_set(self, data):

        data.value = 0
        data.click_flag = False

        data.pxf = data.plus_px_frame_data()

        # sta_endがついている変数は左座標と右座標で取ってるので変換注意
        # ↑訂正
        # 座標＋サイズ方式に変更します

        # data.timeline_obj_range = [0, 100]  # フレームに対する実数表示！ タイムラインに対してどれだけ占めるかを計算します #開始地点 ,サイズ
        # data.timeline_view_range = [0, 100]  # フレームに対する実数表示！ #タイムラインが、現在どこからどこまでの割合で表示しているかを"フレームに対して"記録します #開始地点 ,終了地点

        # 上二つどちらもフレームに対する実数表示にすれば楽かもしれないけど、今度はフレームに対する実数表示のための変換もいるのか、しんどすぎる

        data.new_diagram("bar")
        data.edit_diagram_size("bar", x=100, y=40)
        data.edit_diagram_position("bar", x=100, y=40)
        data.edit_diagram_color("bar", "#00ff00")
        data.territory_draw()

        # data.sta_end_px = [0, 0]  # 実数表示 タイムラインがどこからどこまでを表示するかpxで保管します
        # data.sta_end_frame = [0, 0]  # フレーム実数表示 タイムラインがどこからどこまで表示するかをframeで表示します
        #data.slope = 0

        #data.edit_objct_frame = edit_objct_frame
        #data.edit_objct_motion = edit_objct_motion

        #data.pxf(sta_px=0, end_px=100, sta_f=5, end_f=100)

        def set_pxf_slope(sta_px=None, end_px=None, sta_f=None, end_f=None):
            #print("obj", sta_px, end_px, sta_f, end_f)
            data.pxf.edit_range(sta_px=sta_px, end_px=end_px, sta_f=sta_f, end_f=end_f)

        data.set_pxf_slope = set_pxf_slope

        def draw(pos, size):
            data.edit_diagram_position("bar", x=pos)
            data.edit_diagram_size("bar", x=size)
            data.territory_draw()

        data.pxf.set_draw_func(draw)

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
