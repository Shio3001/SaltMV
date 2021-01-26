import sys


class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        data.first_motion, data.first_touch, data.first_canvas_within = {}, {}, None

        data.timeline_height = 30

        def edit_timeline_height(size):
            data.timeline_height = size
            data.edit_canvas_size(height_size=data.timeline_height)

        data.edit_timeline_height = edit_timeline_height

        def click_drag(event):
            motion, touch, canvas_within = data.get_mouse_position()
            minimum_limit = 10  # 長さの最低数値
            # print(motion["x"])

            #print(motion, touch, canvas_within)

            if data.first_touch["left"] == True and data.first_canvas_within["y"] == True:
                shrinked_length = data.canvas_position[0]
                data.edit_canvas_position(width_position=motion["x"])
                shrinked_length -= data.canvas_position[0]
                data.edit_canvas_size(width_size=data.canvas_size[0] + shrinked_length)

            elif data.first_touch["right"] == True and data.first_canvas_within["y"] == True:
                trace = [motion["x"] - data.canvas_position[0], motion["y"] - data.canvas_position[1]]
                data.edit_canvas_size(width_size=trace[0])

            else:
                pass

            if data.first_canvas_within["xy"] == True and data.first_touch["left"] == False and data.first_touch["right"] == False:
                data.edit_canvas_position(width_position=motion["x"] - data.mouse_misalignment)
                if canvas_within["xy"] == False:
                    # print("段を変更")
                    change_layer_distance = data.timeline_height
                    if motion["y"] - data.canvas_position[1] < 0:
                        change_layer_distance *= -1
                    data.edit_canvas_position(height_position=data.canvas_position[1] + change_layer_distance)

                # バーの移動

            canvas_log = data.get_canvas_data()

            # 既定値より短くなったときの対応
            if canvas_log["size"][0] <= minimum_limit:
                data.edit_canvas_size(width_size=minimum_limit)

                if data.first_touch["left"] == True:
                    log_position = canvas_log["position"][0] + canvas_log["size"][0] - minimum_limit
                    data.edit_canvas_position(width_position=log_position)

        def click_start(event):
            # print("開始")
            data.first_motion, data.first_touch, data.first_canvas_within = data.get_mouse_position()
            data.mouse_misalignment = data.first_motion["x"] - data.canvas_position[0]
            # print("押す")

        def click_finish(event):
            data.first_motion, data.first_touch, data.first_canvas_within = {}, {}, {}
            data.set_cursor()
            # print("終了")

        def motion(event):
            _, this_touch, this_within = data.get_mouse_position()
            print(data.first_touch, this_touch)
            target = [this_touch.get("left"), this_touch.get("right")]

            # print("移動検知")

            if this_within["xy"] == True and not True in target:
                data.set_cursor(name="openhand")

            elif True in target and this_within["y"] == True:
                data.set_cursor(name="resizeleftright")
                # print("カーソル変更")
            else:
                data.set_cursor()

        data.edit_view_new("base")
        data.edit_view_fill("base", True)

        data.edit_canvas_text(text="動画")
        data.edit_canvas_position(width_position=10, height_position=data.timeline_height)
        data.edit_canvas_size(width_size=100, height_size=data.timeline_height)
        data.edit_view_color("base", color="#ffe44d")
        data.window_for_event(processing=motion, user_event="Motion")
        data.window_for_event(processing=click_drag, user_event="B1-Motion")
        data.window_for_event(processing=click_start, user_event="Button-1")
        data.window_for_event(processing=click_finish, user_event="ButtonRelease-1")
        # 同じイベントを指定することはできないので注意を
        data.set_mouse_motion(True)

        print("追加")

        return data  # ボタンのベースを生成
