class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        xy_size = [70, 20]

        direction_int = 0
        direction_str = "x"

        data.edit_view_new("a1")
        data.edit_view_fill("a1", True)

        data.edit_view_new("a2")
        #data.edit_view_blank_space("a2", width_size=10, height_size=5)

        data.edit_view_position("a2", width_position=0, height_position=0)
        data.edit_view_size("a2", width_size=xy_size[0], height_size=xy_size[1])
        #data.edit_view_fill("a2", True)

        data.edit_view_color("a1", color="#f0f8ff")
        data.edit_view_color("a2", color="#4169e1")
        data.edit_view_match("a2", "y", True)

        data.edit_canvas_position(width_position=0, height_position=0)
        data.edit_canvas_size(width_size=xy_size[0], height_size=xy_size[1])

        data.canvas_update()

        data.scrollbar_size = [0.25, data.canvas_size[direction_int]]  # 割合 , 最大サイズ

        def draw(motion):
            data.scrollbar_size[0] = (motion - data.canvas_position[direction_int]) / data.scrollbar_size[1]
            size = data.scrollbar_size[1] * data.scrollbar_size[0]
            #position = 0

            if data.scrollbar_size[0] < 0:
                data.scrollbar_size[0] = 0

            if data.scrollbar_size[0] > 1:
                data.scrollbar_size[0] = 1

            data.edit_view_size("a2", width_size=size)

            data.operation["log"].write("{0} %".format(round(data.scrollbar_size[0] * 100)))
            #data.edit_view_position("a2", width_position=position)

        data.draw = draw

        def click_start(event):
            data.first_motion, data.first_touch, data.first_canvas_within = data.get_mouse_position()

            if data.first_canvas_within["xy"] == True:
                data.draw(data.first_motion[direction_str])

        # def click_finish(event):
        #    data.first_motion, data.first_touch, data.first_canvas_within = {}, {}, {}
            # data.set_cursor()

        def click_drag(event):
            motion, touch, canvas_within = data.get_mouse_position()

            if data.first_canvas_within["xy"] == True:
                data.draw(motion[direction_str])

        data.window_for_event(processing=click_drag, user_event="B1-Motion")
        data.window_for_event(processing=click_start, user_event="Button-1")
        #data.window_for_event(processing=click_finish, user_event="ButtonRelease-1")

        return data
