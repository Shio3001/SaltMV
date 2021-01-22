class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        data.edit_view_new("base")
        data.edit_view_fill("base", True)

        # data.edit_canvas_text(text="これはてすと")
        data.edit_canvas_position(width_position=0, height_position=0)
        data.edit_canvas_size(width_size=0, height_size=0)
        data.edit_view_color("base", color="#c0c0c0")

        return data
