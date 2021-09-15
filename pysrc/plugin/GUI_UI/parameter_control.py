import copy
import asyncio
import time


class parts:
    def UI_set(self, UI_auxiliary):

        # print("インスタンス 化")

        box_size = 20
        gap = 5
        pos_y_normal = box_size + gap
        sta_point = 10

        new_button_for_parameter_control = UI_auxiliary.edit_control_auxiliary.callback_operation.get_event("new_button_for_parameter_control")[0]
        UI_auxiliary.button_parameter_control = new_button_for_parameter_control()  # effect_controller ←40行付近呼び出し先

        # UI_auxiliary.callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBackOne()

        def del_parameter_ui():
            # #print("del_parameter_ui 削除")
            UI_auxiliary.button_parameter_control.del_territory()

            del UI_auxiliary.button_parameter_control

        UI_auxiliary.callback_operation.set_event("del_parameter_ui", del_parameter_ui)

        def parameter_ui_set(column=0, text=None):
            # pos_y = pos_y_normal * column + sta_point

            UI_auxiliary.button_parameter_control.edit_diagram_text("text", text)
            UI_auxiliary.button_parameter_control.edit_territory_position(x=10, y=column*(box_size + gap) + sta_point)
            UI_auxiliary.button_parameter_control.edit_territory_size(x=200, y=box_size)
            UI_auxiliary.button_parameter_control.edit_diagram_color("background", "#44ff44")
            UI_auxiliary.button_parameter_control.diagram_stack("text", True)
            UI_auxiliary.button_parameter_control.territory_draw()

        UI_auxiliary.parameter_ui_set = parameter_ui_set
        # UI_auxiliary.del_control_ui = del_control_ui

        UI_auxiliary.click_stop = False

        #UI_auxiliary.background_mouse = [0, 0]
        #UI_auxiliary.background_now_mouse = [0, 0]

        def popup_del():
            
            UI_auxiliary.effect_del(UI_auxiliary.now_exchange)
            UI_auxiliary.shape_updown_destination_view_False()

        def click_right(event):
            click_effect_point = UI_auxiliary.now_exchange
            UI_auxiliary.color_edit(click_effect_point, push_color="#1111ff")
            UI_auxiliary.window.update()
            UI_auxiliary.edit_control_auxiliary.callback_operation.event("element_ui_all_del")

            self.popup = UI_auxiliary.operation["plugin"]["other"]["menu_popup"].MenuPopup(UI_auxiliary.window, popup=True)

            specify_destination = ["行先指定"]

            len_ui_list = UI_auxiliary.get_len_ui_list()
            for i in range(len_ui_list):
                if i == click_effect_point:
                    continue

                ui_mov = UIMov(click_effect_point, i, UI_auxiliary.effect_updown)
                specify_destination.append("{0} に移動".format(i))
                specify_destination.append(ui_mov.run)

            popup_list = [["削除", popup_del], specify_destination]
            self.popup.set(popup_list)

            # print("開始")

            UI_auxiliary.background_mouse, _, _, xy = UI_auxiliary.get_window_contact()

            mouse = [0, 0]
            for i in range(2):
                mouse[i] = UI_auxiliary.background_mouse[i] + xy[i]

            self.popup.show(mouse[0], mouse[1])

            UI_auxiliary.color_edit(click_effect_point)
            UI_auxiliary.shape_updown_destination_view_False()

        #UI_auxiliary.effect_updown(UI_auxiliary.background_mouse[1], UI_auxiliary.background_now_mouse[1],   pos_y_normal, gap, sta_point)

        UI_auxiliary.button_parameter_control.add_diagram_event("text", "Button-2", click_right)
        UI_auxiliary.button_parameter_control.add_diagram_event("background", "Button-2", click_right)

        return UI_auxiliary


class UIMov:
    def __init__(self, A, B, effect_updown):
        self.A = A
        self.B = B
        self.effect_updown = effect_updown

    def run(self):
        self.effect_updown(self.A, self.B)
