class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        def telescopic():
            if data.mouse_touch["left"] is True:
                print("a")
                #data.edit_canvas_size(width_size=100, height_size=30)
                #data.edit_canvas_position(width_position=0, height_position=0)
                #data.edit_canvas_size(width_size=100, height_size=30)

        data.edit_view_new("base")
        data.set_view_fill("base", True)

        data.edit_canvas_text(text="動画")
        data.edit_canvas_position(width_position=0, height_position=0)
        data.edit_canvas_size(width_size=100, height_size=30)
        data.edit_view_color("base", color="#0000ff")
        data.canvas_for_event(processing=data.processing, user_event="<B1-Motion>")
        data.set_mouse_motion(True)

        print("追加")

        return data  # ボタンのベースを生成
