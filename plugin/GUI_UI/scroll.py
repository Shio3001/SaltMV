class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        data.edit_view_new("a1")
        data.edit_view_fill("a1", True)

        data.edit_view_new("a2")
        #data.edit_view_blank_space("a2", width_size=10, height_size=5)

        data.edit_view_position("a2", width_position=0, height_position=0)
        data.edit_view_size("a2", width_size=400, height_size=20)

        data.edit_view_color("a1", color="#a9a9a9")
        data.edit_view_color("a2", color="#d3d3d3")

        data.edit_canvas_position(width_position=300, height_position=200)
        data.edit_canvas_size(width_size=400, height_size=20)

        data.canvas_update()

        data.blank_space = 5

        data.scrollbar_size = [0.25, data.canvas_size[0] - (data.blank_space * 2)]
        data.scrollbar_position = [0, data.blank_space, data.canvas_size[0] - data.blank_space]

        def scroll(motion):
            #start_distance = data.view_data["a2"].position[0] - (motion - data.canvas_position[0])

            data.scrollbar_position[0] = (motion - data.canvas_position[0]) / (data.scrollbar_position[2] - data.scrollbar_position[1])

            data.edit_view_size("a2", width_size=data.scrollbar_size[1] * data.scrollbar_size[0])
            data.edit_view_position("a2", width_position=data.scrollbar_position[1] + ((data.scrollbar_position[2] - data.scrollbar_position[1]) * data.scrollbar_position[0]))

        data.scroll = scroll

        def click_start(event):
            data.first_motion, data.first_touch, data.first_canvas_within = data.get_mouse_position()
            data.mouse_misalignment = data.first_motion["x"] - data.canvas_position[0]

            if data.first_canvas_within["xy"] == True:
                data.scroll(data.first_motion["x"])

        data.click_start = click_start

        def click_finish(event):
            data.first_motion, data.first_touch, data.first_canvas_within = {}, {}, {}
            # data.set_cursor()

        def click_drag(event):
            motion, touch, canvas_within = data.get_mouse_position()
            if data.first_canvas_within["xy"] == True:
                data.scroll(motion["x"])

        data.click_finish = click_finish
        data.click_drag = click_drag

        data.scroll(data.canvas_position[0])

        data.window_for_event(processing=click_drag, user_event="B1-Motion")
        data.window_for_event(processing=click_start, user_event="Button-1")
        data.window_for_event(processing=click_finish, user_event="ButtonRelease-1")

        # data.scrollbar_size =

        # for c , v in zip(data.choice_range , data.view_range):

        return data
