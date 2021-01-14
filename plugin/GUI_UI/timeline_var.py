import sys


class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        def telescopic(self):
            motion, touch, history = data.get_mouse_position()
            if touch["left"] == True:
                print("a")

                data.edit_canvas_position(width_position=motion["x"], height_position=0)

            if touch["right"] == True:
                print(history[0], "-------------------------------------------------------------------------")
                data.edit_canvas_size(width_size=data.canvas_size[0] + history[0], height_size=30)

                #data.edit_canvas_size(width_size=100, height_size=30)
                #data.edit_canvas_position(width_position=0, height_position=0)
                #data.edit_canvas_size(width_size=100, height_size=30)

        data.edit_view_new("base")
        data.set_view_fill("base", True)

        data.edit_canvas_text(text="動画")
        data.edit_canvas_position(width_position=20, height_position=20)
        data.edit_canvas_size(width_size=100, height_size=30)
        data.edit_view_color("base", color="#0000ff")
        data.canvas_for_event(processing=telescopic, user_event="B1-Motion")
        data.set_mouse_motion(True)

        print("追加")

        return data  # ボタンのベースを生成
