

class parts:
    def UI_set(self, data):

        pos_y_normal = 25

        text_x = 0
        textbox1_x = 100
        textbox2_x = 200

        #data.new_diagram("text", diagram_type="text")
        #data.edit_diagram_size("text", x=180, y=20)
        #data.edit_diagram_text("text", font_size=20)

        new_button_for_parameter_control = data.all_data.callback_operation.get_event("new_button_for_parameter_control")[0]
        data.button_parameter_control = new_button_for_parameter_control()

        data.callback_operation = data.operation["plugin"]["other"]["callback"].CallBack()

        def del_parameter_ui():
            print("del_parameter_ui 削除")
            data.button_parameter_control.del_territory()
            del data.button_parameter_control

        data.callback_operation.set_event("del_parameter_ui", del_parameter_ui)

        def parameter_ui_set(motion=False, column=0, text=None):
            pos_y = pos_y_normal * column

            data.button_parameter_control.edit_diagram_text("text", text)
            data.button_parameter_control.edit_territory_position(x=10, y=column*25)
            data.button_parameter_control.edit_territory_size(x=200, y=20)
            data.button_parameter_control.edit_diagram_color("background", "#44ff44")
            data.button_parameter_control.diagram_stack("text", True)
            data.button_parameter_control.territory_draw()

        data.parameter_ui_set = parameter_ui_set
        #data.del_control_ui = del_control_ui

        return data
