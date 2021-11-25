import sys


class parts:
    def UI_set(self, UI_auxiliary):

        pos_y_normal = 25

        text_x = 0
        textbox1_x = 100
        textbox2_x = 300

        UI_auxiliary.new_diagram("text", diagram_type="text")
        #UI_auxiliary.edit_diagram_position("text", x=0, y=pos_y_normal)
        UI_auxiliary.edit_diagram_size("text", x=100, y=20)
        UI_auxiliary.edit_diagram_text("text", font_size=20)

        UI_auxiliary.new_diagram("textbox1", diagram_type="textbox")
        #UI_auxiliary.edit_diagram_position("textbox1", x=200, y=pos_y_normal)
        UI_auxiliary.edit_diagram_size("textbox1", x=100, y=20)

        UI_auxiliary.new_diagram("textbox2", diagram_type="textbox")
        #UI_auxiliary.edit_diagram_position("textbox2", x=400, y=pos_y_normal)
        UI_auxiliary.edit_diagram_size("textbox2", x=100, y=20)

        def textbox1(text):
            print(text)

        def textbox2(text):
            print(text)

        def file_open(e=None):
            default = UI_auxiliary.get_text("textbox1")
            file_open_text = UI_auxiliary.open_file_select(default)
            UI_auxiliary.edit_diagram_text("textbox1", text=file_open_text)
            UI_auxiliary.run_entry_event_callback("textbox1")

        def request_easing(e=None):
            easing_data, media_id, effect_id, mov_key = UI_auxiliary.get_easing_func()
            info = (easing_data.gx, easing_data.gy, easing_data.rx, easing_data.ry,media_id, effect_id, mov_key)
            UI_auxiliary.edit_control_auxiliary.callback_operation.event("easing_request", info=info)

        UI_auxiliary.callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()

        UI_auxiliary.file_path_open_flag = False
        UI_auxiliary.easing_flag = False

        def file_path_open_del_button():
            if UI_auxiliary.file_path_open_flag:
                UI_auxiliary.button_parameter_control_file.del_territory()
            if UI_auxiliary.easing_flag:
                UI_auxiliary.button_parameter_control_easing.del_territory()

        UI_auxiliary.callback_operation.set_event("parameter_diagram_del", file_path_open_del_button)

        def parameter_ui_set(motion=False, column=0, text=None, text_a=None, text_b=None, text_a_return=None, text_b_return=None, text_fixed=None, file_path=False, get_easing_func=None):
            pos_y = pos_y_normal * column
            text_fixed_x_size = textbox2_x - textbox1_x + 100

            UI_auxiliary.get_easing_func = get_easing_func

            UI_auxiliary.edit_diagram_text("text", text=text)
            UI_auxiliary.edit_diagram_text("textbox1", text=text_a,  entry_event=text_a_return)
            UI_auxiliary.edit_diagram_text("textbox2", readonly=1-motion, text=text_b, entry_event=text_b_return)

            UI_auxiliary.edit_diagram_position("text", x=text_x, y=pos_y)
            UI_auxiliary.edit_diagram_position("textbox1", x=textbox1_x, y=pos_y)

            #print("text_a, text_b", text_a, text_b)

            UI_auxiliary.edit_diagram_position("textbox2", x=textbox2_x, y=pos_y)

            if text_fixed and file_path:
                print("text_fixed and file_path")

                new_button_for_parameter = UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("new_button_for_parameter", 0)
                UI_auxiliary.button_parameter_control_file = new_button_for_parameter()  # effect_controller ←40行付近呼び出し先
                UI_auxiliary.button_parameter_control_file.edit_diagram_text("text", "ファイル設定", font_size=15)
                UI_auxiliary.button_parameter_control_file.edit_territory_position(x=text_fixed_x_size+110, y=pos_y)
                UI_auxiliary.button_parameter_control_file.edit_territory_size(x=100, y=20)
                UI_auxiliary.button_parameter_control_file.edit_diagram_color("background", "#44ff44")
                UI_auxiliary.button_parameter_control_file.diagram_stack("text", True)
                UI_auxiliary.button_parameter_control_file.territory_draw()
                UI_auxiliary.button_parameter_control_file.add_diagram_event("text", "Button-1", file_open)
                UI_auxiliary.button_parameter_control_file.add_diagram_event("background", "Button-1", file_open)
                UI_auxiliary.file_path_open_flag = True

            elif UI_auxiliary.file_path_open_flag:
                UI_auxiliary.button_parameter_control_file.del_territory()

            elif UI_auxiliary.easing_flag:
                UI_auxiliary.button_parameter_control_easing.del_territory()

            if text_fixed:
                UI_auxiliary.diagram_forget("textbox2", True)
                UI_auxiliary.edit_diagram_size("textbox1", x=text_fixed_x_size)
                #UI_auxiliary.edit_diagram_text("textbox1", set_int_type=False)
                #UI_auxiliary.edit_diagram_text("textbox2", set_int_type=False)

            else:
                UI_auxiliary.diagram_forget("textbox2", False)
                UI_auxiliary.edit_diagram_size("textbox1", x=100, y=20)
                #UI_auxiliary.edit_diagram_text("textbox1", set_int_type=True)
                #UI_auxiliary.edit_diagram_text("textbox2", set_int_type=True)

                new_button_for_parameter = UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("new_button_for_parameter", 0)
                UI_auxiliary.button_parameter_control_easing = new_button_for_parameter()  # effect_controller ←40行付近呼び出し先
                UI_auxiliary.button_parameter_control_easing.edit_diagram_text("text", "イージング設定", font_size=15)
                UI_auxiliary.button_parameter_control_easing.edit_territory_position(x=text_fixed_x_size+110, y=pos_y)
                UI_auxiliary.button_parameter_control_easing.edit_territory_size(x=100, y=20)
                UI_auxiliary.button_parameter_control_easing.edit_diagram_color("background", "#44ff44")
                UI_auxiliary.button_parameter_control_easing.diagram_stack("text", True)
                UI_auxiliary.button_parameter_control_easing.territory_draw()
                UI_auxiliary.button_parameter_control_easing.add_diagram_event("text", "Button-1", request_easing)
                UI_auxiliary.button_parameter_control_easing.add_diagram_event("background", "Button-1", request_easing)
                UI_auxiliary.easing_flag = True

            UI_auxiliary.territory_draw()

        UI_auxiliary.parameter_ui_set = parameter_ui_set

        return UI_auxiliary
