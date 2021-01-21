class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        def view():
            canvas_log = data.get_window_data()
            # print(canvas_log)
            data.edit_canvas_size(width_size=canvas_log["size"][0], height_size=1)

        data.edit_view_new("base")
        data.edit_view_fill("base", True)
        data.edit_view_color("base", color="#ffe44d")

        data.window_for_event(processing=view, user_event="Configure")

        return data
