import copy


class parts:
    def UI_set(self, data):

        print("インスタンス 化")

        box_size = 20
        gap = 5
        pos_y_normal = box_size + gap
        sta_point = 10

        new_button_for_parameter_control = data.all_data.callback_operation.get_event("new_button_for_parameter_control")[0]
        data.button_parameter_control = new_button_for_parameter_control()  # effect_controller ←40行付近呼び出し先

        #data.callback_operation = data.operation["plugin"]["other"]["callback"].CallBackOne()

        def del_parameter_ui():
            #print("del_parameter_ui 削除")
            data.button_parameter_control.del_territory()

            del data.button_parameter_control

        data.callback_operation.set_event("del_parameter_ui", del_parameter_ui)

        def parameter_ui_set(column=0, text=None):
            #pos_y = pos_y_normal * column + sta_point

            data.button_parameter_control.edit_diagram_text("text", text)
            data.button_parameter_control.edit_territory_position(x=10, y=column*(box_size + gap) + sta_point)
            data.button_parameter_control.edit_territory_size(x=200, y=box_size)
            data.button_parameter_control.edit_diagram_color("background", "#44ff44")
            data.button_parameter_control.diagram_stack("text", True)
            data.button_parameter_control.territory_draw()

        data.parameter_ui_set = parameter_ui_set
        #data.del_control_ui = del_control_ui

        data.click_stop = False

        data.background_mouse = [0, 0]
        data.background_now_mouse = [0, 0]

        def click_start(event):
            data.click_stop = True
            data.background_mouse, _, _, _ = data.get_window_contact()

        def click_position(event):
            if not data.click_stop:
                return
            data.background_now_mouse, _, _, _ = data.get_window_contact()
            data.effect_updown_destination(data.background_mouse[1], data.background_now_mouse[1], pos_y_normal, gap, sta_point)

        def click_end(event):
            if not data.click_stop:
                return
            print("終端処理")

            data.background_now_mouse, _, _, _ = data.get_window_contact()

            data.click_stop = False
            # print(data.button_parameter_control.callback_operation.all_get_event())
            data.effect_updown(data.background_mouse[1], data.background_now_mouse[1],   pos_y_normal, gap, sta_point)

            data.background_mouse = [0, 0]
            data.background_now_mouse = [0, 0]

        data.button_parameter_control.add_diagram_event("background", "Button-1", click_start)
        data.button_parameter_control.window_event_data["add"]("Motion", click_position)
        data.button_parameter_control.add_diagram_event("background", "ButtonRelease-1", click_end)

        return data
