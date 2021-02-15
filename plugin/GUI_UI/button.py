class parts:
    def __init__(self):
        print("")

    def UI_set(self, UI_operation):
        data = UI_operation

        data.new_territory("a")
        data.edit_territory_size("a", x=640, y=70)
        data.edit_territory_position("a", x=20, y=20)

        # data.edit_view_color("a1", color="#808080")

        """
        data.edit_view_new("a")
        data.edit_view_fill("a", True)

        data.edit_canvas_text(text="これはてすと")
        data.edit_canvas_position(width_position=100, height_position=200)
        data.edit_canvas_size(width_size=100, height_size=300)
        data.edit_view_color("a", color="#0000ff")

        data.canvas_for_event(processing=data.processing, user_event=data.user_event)
        """
        # data.set_mouse_motion(True)
        # data.set_cursor("none")

        print("追加")

        return data  # ボタンのベースを生成
