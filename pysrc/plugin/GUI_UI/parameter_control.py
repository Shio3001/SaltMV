import copy
import asyncio
import time


class parts:
    def UI_set(self, UI_data):

        #print("インスタンス 化")

        box_size = 20
        gap = 5
        pos_y_normal = box_size + gap
        sta_point = 10

        new_button_for_parameter_control = UI_data.all_UI_data.callback_operation.get_event("new_button_for_parameter_control")[0]
        UI_data.button_parameter_control = new_button_for_parameter_control()  # effect_controller ←40行付近呼び出し先

        # UI_data.callback_operation = UI_data.operation["plugin"]["other"]["callback"].CallBackOne()

        def del_parameter_ui():
            # #print("del_parameter_ui 削除")
            UI_data.button_parameter_control.del_territory()

            del UI_data.button_parameter_control

        UI_data.callback_operation.set_event("del_parameter_ui", del_parameter_ui)

        def parameter_ui_set(column=0, text=None):
            # pos_y = pos_y_normal * column + sta_point

            UI_data.button_parameter_control.edit_diagram_text("text", text)
            UI_data.button_parameter_control.edit_territory_position(x=10, y=column*(box_size + gap) + sta_point)
            UI_data.button_parameter_control.edit_territory_size(x=200, y=box_size)
            UI_data.button_parameter_control.edit_diagram_color("background", "#44ff44")
            UI_data.button_parameter_control.diagram_stack("text", True)
            UI_data.button_parameter_control.territory_draw()

        UI_data.parameter_ui_set = parameter_ui_set
        # UI_data.del_control_ui = del_control_ui

        UI_data.click_stop = False

        UI_data.background_mouse = [0, 0]
        UI_data.background_now_mouse = [0, 0]

        self.popup = UI_data.operation["plugin"]["other"]["menu_popup"].MenuPopup(UI_data.window, popup=True)

        def popup_del():
            UI_data.effect_del(UI_data.background_mouse[1], pos_y_normal, gap, sta_point)
            UI_data.shape_updown_destination_view_False()

        popup_list = [("削除", popup_del)]
        self.popup.set(popup_list)

        def click_right(event):

            UI_data.background_mouse, _, _, xy = UI_data.get_window_contact()
            click_effect_point = (UI_data.background_mouse[1]-sta_point) // pos_y_normal
            UI_data.color_edit(click_effect_point, push_color="#1111ff")
            UI_data.window.update()
            UI_data.all_UI_data.callback_operation.event("element_ui_all_del")

            # print("開始")

            mouse = [0, 0]
            for i in range(2):
                mouse[i] = UI_data.background_mouse[i] + xy[i]

            self.popup.show(mouse[0], mouse[1])

            UI_data.color_edit(click_effect_point)
            UI_data.shape_updown_destination_view_False()
            UI_data.click_stop = False

        #UI_data.Motion_flag = False

        UI_data.click_stop = False

        UI_data.end_to_sta_time = 0

        def click_start(event):
            bool_time = 0.1 <= time.time() - UI_data.end_to_sta_time
            if not bool_time:
                UI_data.click_stop = False
                print("parameter_control拒否")
                return

            UI_data.click_stop = True
            UI_data.background_mouse, _, _, _ = UI_data.get_window_contact()

        def click_position(event):
            if not UI_data.click_stop:
                return
            # print("押す[parameter_control]")
            # if not UI_data.Motion_flag:
            #UI_data.click_stop = True
            #UI_data.background_mouse, _, _, _ = UI_data.get_window_contact()
            #UI_data.Motion_flag = True

            # if not UI_data.click_stop:
            #    return

            # UI_data.shape_updown_destination_view_True()

            UI_data.background_now_mouse, _, _, _ = UI_data.get_window_contact()

            UI_data.effect_updown_destination(UI_data.background_mouse[1], UI_data.background_now_mouse[1], pos_y_normal, gap, sta_point)

        def click_end(event):
            print("離す[parameter_control]")
            UI_data.shape_updown_destination_view_False()
            UI_data.click_stop = False
            #UI_data.Motion_flag = False
            UI_data.background_now_mouse, _, _, _ = UI_data.get_window_contact()
            UI_data.effect_updown(UI_data.background_mouse[1], UI_data.background_now_mouse[1],   pos_y_normal, gap, sta_point)

            UI_data.end_to_sta_time = time.time()

        UI_data.click_end = click_end

        UI_data.button_parameter_control.add_diagram_event("text", "Button-2", click_right)
        UI_data.button_parameter_control.add_diagram_event("background", "Button-2", click_right)

        UI_data.button_parameter_control.add_diagram_event("text", "Button-1", click_start)
        UI_data.button_parameter_control.add_diagram_event("background", "Button-1", click_start)
        UI_data.button_parameter_control.window_event_data["add"]("B1-Motion", click_position)
        UI_data.button_parameter_control.add_diagram_event("text", "ButtonRelease-1", click_end)
        UI_data.button_parameter_control.add_diagram_event("background", "ButtonRelease-1", click_end)

        return UI_data
