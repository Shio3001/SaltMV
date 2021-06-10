

class parts:
    def UI_set(self, data):

        pos_y_normal = 25

        box_size = 20

        new_button_for_parameter_control = data.all_data.callback_operation.get_event("new_button_for_parameter_control")[0]
        data.button_parameter_control = new_button_for_parameter_control()  # effect_controller ←40行付近呼び出し先

        data.callback_operation = data.operation["plugin"]["other"]["callback"].CallBack()

        def del_parameter_ui():
            #print("del_parameter_ui 削除")
            data.button_parameter_control.del_territory()
            del data.button_parameter_control

        data.callback_operation.set_event("del_parameter_ui", del_parameter_ui)

        def parameter_ui_set(motion=False, column=0, text=None):
            pos_y = pos_y_normal * column

            data.button_parameter_control.edit_diagram_text("text", text)
            data.button_parameter_control.edit_territory_position(x=10, y=column*(box_size + 5))
            data.button_parameter_control.edit_territory_size(x=200, y=box_size)
            data.button_parameter_control.edit_diagram_color("background", "#44ff44")
            data.button_parameter_control.diagram_stack("text", True)
            data.button_parameter_control.territory_draw()

        data.parameter_ui_set = parameter_ui_set
        #data.del_control_ui = del_control_ui

        def click_start(event):
            self.background_mouse, _, _ = data.button_parameter_control.get_diagram_contact("background")

        def click_position(event):
            self.background_now_mouse, _, _ = data.button_parameter_control.get_diagram_contact("background")
            data.callback_operation.event("effect_updown", (self.background_mouse[1], self.background_now_mouse[1]))

        def click_end(event):
            self.background_mouse, _, _ = data.button_parameter_control.get_diagram_contact("background", del_mouse=True)
            self.background_now_mouse, _, _ = data.button_parameter_control.get_diagram_contact("background", del_mouse=True)

        data.button_parameter_control.add_diagram_event("background", "Button-1", click_start)
        data.button_parameter_control.window_event_data["add"]("Motion", click_position)
        data.button_parameter_control.add_diagram_event("background", "ButtonRelease-1", click_end)

        return data
