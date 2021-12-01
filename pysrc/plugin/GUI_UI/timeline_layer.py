import copy
import inspect


class parts:
    def UI_set(self, UI_auxiliary):

        UI_auxiliary.callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()

        timeline_left = 50  # タイムラインの左側のshape(x)
        timeline_up = 50  # タイムラインの上側のshape(y)
        timeline_size = 20  # タイムラインの幅(y)

        UI_auxiliary.edit_territory_position(x=0, y=50)
        UI_auxiliary.edit_territory_size(x=50, y=20)
        UI_auxiliary.new_diagram("background")

        UI_auxiliary.edit_diagram_fill("background", True)
        UI_auxiliary.edit_diagram_color("background", "#aaaaaa")

        UI_auxiliary.new_diagram("text", diagram_type="text")
        UI_auxiliary.edit_diagram_text("text", text="00", center=True, font_size=20)
        UI_auxiliary.edit_diagram_color("text", "#ffffff")

        UI_auxiliary.territory_draw()

        UI_auxiliary.diagram_stack("text", True)

        def add_media_obj():
            UI_auxiliary.edit_diagram_color("background", "#aaaaaa")

            print("add_media_obj")

            UI_auxiliary.timeline_nowtime_approval_False()

            UI_auxiliary.new_obj(layer_number=UI_auxiliary.num)

            UI_auxiliary.timeline_nowtime_approval_True()

        self.popup = UI_auxiliary.operation["plugin"]["other"]["menu_popup"].MenuPopup(UI_auxiliary.window, popup=True)

        def media_object_paste():
            UI_auxiliary.edit_diagram_color("background", "#aaaaaa")
            UI_auxiliary.timeline_nowtime_approval_False()
            UI_auxiliary.edit_control_auxiliary.callback_operation.event("media_object_copy_run", info=UI_auxiliary.num)
            UI_auxiliary.timeline_nowtime_approval_True()

        add_media_obj_list = ["メディアオブジェクト追加", add_media_obj]
        copy_media_obj_list = ["貼り付け", media_object_paste]

        popup_list = [add_media_obj_list, copy_media_obj_list]
        self.popup.set(popup_list)

        def set_right_click_pop(e=None):
            print("set_right_click_pop")

            UI_auxiliary.edit_diagram_color("background", "#bbbbbb")

            copy_id = UI_auxiliary.edit_control_auxiliary.callback_operation.event("media_object_get_copy_id")["media_object_get_copy_id"]

            if copy_id is None:
                self.popup.edit_bool_twice("貼り付け", False)
            else:
                self.popup.edit_bool_twice("貼り付け", True)

            mouse, _, _, xy = UI_auxiliary.window_event_data["contact"]()
            UI_auxiliary.popup_click_position, _, _ = UI_auxiliary.get_diagram_contact("background")

            for i in range(2):
                mouse[i] += xy[i]

            self.popup.show(mouse[0], mouse[1])

        def set_layer_number(num):
            UI_auxiliary.edit_territory_position(x=0, y=timeline_up+num*timeline_size)

            UI_auxiliary.edit_diagram_text("text", text="{0}".format(num), center=True, font_size=20)

            UI_auxiliary.territory_draw()

            UI_auxiliary.num = num

        UI_auxiliary.add_territory_event("ButtonPress-1", set_right_click_pop)

        UI_auxiliary.set_layer_number = set_layer_number

        return UI_auxiliary
