class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        data.edit_view_new("a")
        data.set_view_fill("a", True)

        data.edit_canvas_text(text="tukareta")
        data.edit_canvas_position(width_position=0, height_position=0)
        data.edit_canvas_size(width_size=100, height_size=20)
        data.edit_view_color("a", color="#0000ff")
        data.canvas_for_button(processing=data.processing, user_event=data.user_event)

        print("追加")

        return data  # ボタンのベースを生成
