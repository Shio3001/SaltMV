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

        data.blank_space = 10
        data.mouse_misalignment = 0

        data.scrollbar_size = [0.25, data.canvas_size[0] - (data.blank_space * 2)]
        data.scrollbar_position = [0, data.blank_space, data.canvas_size[0] - data.blank_space - (data.scrollbar_size[1] * data.scrollbar_size[0])]

        data.start_distance = 0

        def scroll_drow():
            data.edit_view_size("a2", width_size=data.scrollbar_size[1] * data.scrollbar_size[0])
            data.edit_view_position("a2", width_position=data.scrollbar_position[1] + ((data.scrollbar_position[2] - data.scrollbar_position[1]) * data.scrollbar_position[0]))

        def get_set_scrollbar_size(ratio=None):
            if ratio is None:
                return data.scrollbar_size[0]

            data.scrollbar_size[0] = ratio

            scroll_drow()

        def get_set_scrollbar_position(ratio=None):
            if ratio is None:
                return data.scrollbar_position[0]

            data.scrollbar_position[0] = ratio

            scroll_drow()

        data.get_set_scrollbar_size = get_set_scrollbar_size
        data.get_set_scrollbar_position = get_set_scrollbar_position

        def scroll(motion):
            data.scrollbar_position[0] = (motion - data.canvas_position[0] - data.start_distance) / (data.scrollbar_position[2] - data.scrollbar_position[1])

            if data.scrollbar_position[0] < 0:
                data.scrollbar_position[0] = 0

            if data.scrollbar_position[0] > 1:
                data.scrollbar_position[0] = 1

            scroll_drow()

            #print("\n{0}%".format(data.scrollbar_position[0]), end="")

        data.scroll = scroll

        def click_start(event):
            data.first_motion, data.first_touch, data.first_canvas_within = data.get_mouse_position()

            if (data.canvas_position[0] + data.view_data["a2"].position[0]) <= data.first_motion["x"] <= (data.canvas_position[0] + data.view_data["a2"].position[0] + data.view_data["a2"].size[0]):
                data.start_distance = data.first_motion["x"] - (data.canvas_position[0] + data.view_data["a2"].position[0]) + data.blank_space
            else:
                data.start_distance = data.view_data["a2"].size[0] / 2

            print("距離 : ", data.start_distance)

            if data.first_canvas_within["xy"] == True:
                data.scroll(data.first_motion["x"])

        data.click_start = click_start

        def click_finish(event):
            data.first_motion, data.first_touch, data.first_canvas_within = {}, {}, {}
            data.start_distance = 0
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
