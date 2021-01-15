import sys


class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        def telescopic(self):
            motion, touch, canvas_within = data.get_mouse_position()

            if data.first_touch["left"] == True:
                #trace = [data.canvas_size[0] - motion["x"], data.canvas_size[1] + motion["y"]]
                # print(trace)

                shrinked_length = data.canvas_position[0]
                data.edit_canvas_position(width_position=motion["x"])
                shrinked_length -= data.canvas_position[0]

                data.edit_canvas_size(width_size=data.canvas_size[0] + shrinked_length)
                #data.edit_canvas_size(width_size=trace[0] - data.canvas_position[0])

            elif data.first_touch["right"] == True:
                trace = [motion["x"] - data.canvas_position[0], motion["y"] - data.canvas_position[1]]
                print(trace)
                data.edit_canvas_size(width_size=trace[0])

            elif data.first_canvas_within == True and not True in list(data.first_touch.values()):
                data.edit_canvas_position(width_position=motion["x"] - data.mouse_misalignment)

        def telescopic1(self):
            data.first_motion, data.first_touch, data.first_canvas_within = data.get_mouse_position()

            data.mouse_misalignment = data.first_motion["x"] - data.canvas_position[0]
            # print("押す")

        def telescopic2(self):
            del data.first_motion, data.first_touch, data.first_canvas_within

        data.edit_view_new("base")
        data.set_view_fill("base", True)

        data.edit_canvas_text(text="動画")
        data.edit_canvas_position(width_position=10, height_position=20)
        data.edit_canvas_size(width_size=100, height_size=30)
        data.edit_view_color("base", color="#ffe44d")
        data.canvas_for_event(processing=telescopic1, user_event="Button-1")
        data.canvas_for_event(processing=telescopic, user_event="B1-Motion")
        data.canvas_for_event(processing=telescopic2, user_event="ButtonRelease-1")
        data.set_mouse_motion(True)

        print("追加")

        return data  # ボタンのベースを生成
