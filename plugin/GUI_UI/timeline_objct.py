import sys
import copy


class parts:
    def UI_set(self, data):

        data.value = 0
        data.click_flag = False

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

        data.sta_end_px = [0, 0]  # 実数表示 タイムラインがどこからどこまでを表示するかpxで保管します
        data.sta_end_frame = [0, 0]  # フレーム実数表示 タイムラインがどこからどこまで表示するかをframeで表示します
        data.slope = 0

        def px_f_func(px_p, px_s=None):  # 送られたpxが何フレームか計算
            f_p = (px_p - data.sta_end_px[0]) * data.slope + data.sta_end_frame[0]

            if px_s is None:
                return f_p

            f_s = (px_p + px_s - data.sta_end_px[0]) * data.slope + data.sta_end_frame[0] - f_p
            f_ps = [f_p, f_s]
            return f_ps

        def f_px_func(f_p, f_s=None):  # 送られたframeが何pxか計算
            px_p = (f_p - data.sta_end_frame[0]) / data.slope + data.sta_end_px[0]

            if f_s is None:
                return px_p

            px_s = (f_p + f_s - data.sta_end_frame[0]) / data.slope + data.sta_end_px[0] - px_p

            px_ps = [px_p, px_s]

            return px_ps

        data.sta_end_obj_px = [0, 100]
        data.sta_end_obj_f = [px_f_func(data.sta_end_obj_px[0]), px_f_func(data.sta_end_obj_px[1])]

        data.px_f_func = px_f_func
        data.f_px_func = f_px_func

        def draw():
            pos, size = copy.deepcopy(data.sta_end_obj_px)

            data.edit_diagram_position("bar", x=pos)
            data.edit_diagram_size("bar", x=size)
            data.territory_draw()

        def edit_timeline_range(sta_px=None, end_px=None, sta_f=None, end_f=None):  # 画面サイズが変更された時 #end_pxはサイズじゃなくて右端座標だよ！！！気をつけて
            data.sta_end_px = data.common_control.xy_compilation(data.sta_end_px, x=sta_px, y=end_px)
            data.sta_end_frame = data.common_control.xy_compilation(data.sta_end_frame, x=sta_f, y=end_f)
            data.slope = (data.sta_end_frame[1] - data.sta_end_frame[0]) / (data.sta_end_px[1] - data.sta_end_px[0])  # 一次関数を計算

            draw()

        def edit_objct_motion(now_position=None, now_size=None):  # 移動量指定

            one_f_px = f_px_func(0, 1)[1]

            if not now_position is None:  # posの変更によって1フレームを下回らないようにする
                ns = now_size
                if ns is None:
                    ns = data.sta_end_obj_px[1]

                if ns < one_f_px:
                    now_position = now_position - (one_f_px - ns)

            data.sta_end_obj_px = data.common_control.xy_compilation(data.sta_end_obj_px, x=now_position, y=now_size)

            if one_f_px > data.sta_end_obj_px[1]:
                data.sta_end_obj_px[1] = one_f_px

            data.sta_end_obj_f = px_f_func(data.sta_end_obj_px[0], data.sta_end_obj_px[1])

            if data.sta_end_obj_f[0] < 0:  # もし0frame以下なら
                data.sta_end_obj_px[0] = f_px_func(0)
                data.sta_end_obj_f[0] = 0

            draw()

        def edit_objct_frame(position=None, size=None):  # フレーム実数指定
            data.sta_end_obj_f = data.common_control.xy_compilation(data.sta_end_obj_f, x=position, y=size)

            if data.sta_end_obj_f[0] < 0:  # もし0frame以下なら
                data.sta_end_obj_f[0] = 0

            data.sta_end_obj_px = f_px_func(data.sta_end_obj_f[0], data.sta_end_obj_f[1])

            draw()

        data.edit_objct_frame = edit_objct_frame
        data.edit_objct_motion = edit_objct_motion

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
                edit_objct_motion(now_position=data.view_pos_sta+now_mov, now_size=data.view_size_sta-now_mov)
                print("左側移動")

            elif data.mouse_touch_sta[0][1]:
                edit_objct_motion(now_size=data.view_size_sta+now_mov)
                print("右側移動")

            elif data.diagram_join_sta[2]:  # 範囲内に入っているか確認します この関数に限りmotion判定でwindowに欠けているので必要です
                edit_objct_motion(now_position=now_mov+data.view_pos_sta)

        def click_end(event):
            data.click_flag = False
            data.mouse_sta, _, data.diagram_join_sta = data.get_diagram_contact("bar", del_mouse=True)
            data.mouse, _, data.diagram_join = data.get_diagram_contact("bar", del_mouse=True)

        data.add_diagram_event("bar", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_position)
        data.add_diagram_event("bar", "ButtonRelease-1", click_end)

        data.edit_timeline_range = edit_timeline_range

        return data
