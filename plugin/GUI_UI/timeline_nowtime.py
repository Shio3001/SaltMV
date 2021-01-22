class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        data.nowtime_mov = True

        def view(event):
            canvas_log = data.get_window_data()
            # print(canvas_log)
            data.edit_canvas_size(width_size=2, height_size=canvas_log["size"][1])

        """
        def click_start(event):
            data.set_cursor(name="resizeleftright")

            data.first_motion, data.first_touch, data.first_canvas_within = data.get_mouse_position()
            data.mouse_misalignment = data.first_motion["x"] - data.canvas_position[0]

            if data.nowtime_mov == True:
                data.edit_canvas_position(width_position=data.first_motion["x"])
        """

        """

        def click_finish(event):

            data.first_motion, data.first_touch, data.first_canvas_within = {}, {}, {}
            print("終了")

        def click_drag(event):
            motion, touch, canvas_within = data.get_mouse_position()

            # if data.first_canvas_within["x"] == True:
            if data.nowtime_mov == True:
                data.edit_canvas_position(width_position=data.first_motion["x"])

        def motion(event):
            _, _, canvas_within = data.get_mouse_position()

            if canvas_within["xy"] == True:
                data.set_cursor(name="resizeleftright")
            else:
                data.set_cursor()

        """

        data.edit_view_new("base")
        data.edit_view_fill("base", True)
        data.edit_view_color("base", color="#b22222")

        data.window_for_event(processing=view, user_event="Configure")

        #data.window_for_event(processing=motion, user_event="Motion")
        #data.window_for_event(processing=click_drag, user_event="B1-Motion")
        #data.window_for_event(processing=click_drag, user_event="Button-1")
        #data.window_for_event(processing=click_finish, user_event="ButtonRelease-1")

        return data
