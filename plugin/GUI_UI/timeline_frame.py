class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        def view(subtraction=0):
            window_log = data.get_window_data()
            data.edit_canvas_size(width_size=window_log["size"][0] - data.all_UI_data.timeline_operation_range[0]-subtraction)
            data.edit_canvas_size(height_size=1)

        data.edit_canvas_position(width_position=data.all_UI_data.timeline_operation_range[0])
        data.edit_canvas_position(height_position=data.all_UI_data.timeline_operation_range[1])

        data.view = view

        #data.window_for_event(processing=view, user_event="Configure")

        return data
