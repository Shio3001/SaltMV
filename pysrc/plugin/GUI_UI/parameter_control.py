import copy


class parts:
    def UI_set(self, data):

        #print("インスタンス 化")

        box_size = 20
        gap = 5
        pos_y_normal = box_size + gap
        sta_point = 10

        new_button_for_parameter_control = data.all_data.callback_operation.get_event("new_button_for_parameter_control")[0]
        data.button_parameter_control = new_button_for_parameter_control()  # effect_controller ←40行付近呼び出し先

        # data.callback_operation = data.operation["plugin"]["other"]["callback"].CallBackOne()

        def del_parameter_ui():
            # #print("del_parameter_ui 削除")
            data.button_parameter_control.del_territory()

            del data.button_parameter_control

        data.callback_operation.set_event("del_parameter_ui", del_parameter_ui)

        def parameter_ui_set(column=0, text=None):
            # pos_y = pos_y_normal * column + sta_point

            data.button_parameter_control.edit_diagram_text("text", text)
            data.button_parameter_control.edit_territory_position(x=10, y=column*(box_size + gap) + sta_point)
            data.button_parameter_control.edit_territory_size(x=200, y=box_size)
            data.button_parameter_control.edit_diagram_color("background", "#44ff44")
            data.button_parameter_control.diagram_stack("text", True)
            data.button_parameter_control.territory_draw()

        data.parameter_ui_set = parameter_ui_set
        # data.del_control_ui = del_control_ui

        data.click_stop = False

        data.background_mouse = [0, 0]
        data.background_now_mouse = [0, 0]

        self.popup = data.operation["plugin"]["other"]["menu_popup"].MenuPopup(data.window, popup=True)

        def popup_del():
            data.effect_del(data.background_mouse[1], pos_y_normal, gap, sta_point)
            data.shape_updown_destination_view_False()

        popup_list = [("削除", popup_del)]
        self.popup.set(popup_list)

        def click_right(event):

            data.background_mouse, _, _, xy = data.get_window_contact()
            click_effect_point = (data.background_mouse[1]-sta_point) // pos_y_normal
            data.color_edit(click_effect_point, push_color="#1111ff")
            data.window.update()
            data.all_data.callback_operation.event("element_ui_all_del")

            # print("開始")

            mouse = [0, 0]
            for i in range(2):
                mouse[i] = data.background_mouse[i] + xy[i]

            self.popup.show(mouse[0], mouse[1])

            data.color_edit(click_effect_point)
            data.shape_updown_destination_view_False()
            data.click_stop = False

        def click_start(event):
            data.click_stop = True
            data.background_mouse, _, _, _ = data.get_window_contact()

        def click_position(event):
            if not data.click_stop:
                return

            data.background_now_mouse, _, _, _ = data.get_window_contact()

            data.effect_updown_destination(data.background_mouse[1], data.background_now_mouse[1], pos_y_normal, gap, sta_point)

        def click_end(event):
            data.shape_updown_destination_view_False()
            data.click_stop = False
            data.background_now_mouse, _, _, _ = data.get_window_contact()
            data.effect_updown(data.background_mouse[1], data.background_now_mouse[1],   pos_y_normal, gap, sta_point)

        data.click_end = click_end

        data.button_parameter_control.add_diagram_event("text", "Button-2", click_right)
        data.button_parameter_control.add_diagram_event("background", "Button-2", click_right)

        data.button_parameter_control.add_diagram_event("text", "Button-1", click_start)
        data.button_parameter_control.add_diagram_event("background", "Button-1", click_start)
        data.button_parameter_control.window_event_data["add"]("Motion", click_position)
        data.button_parameter_control.add_diagram_event("text", "ButtonRelease-1", click_end)
        data.button_parameter_control.add_diagram_event("background", "ButtonRelease-1", click_end)

        return data
