class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        def layer_label_number(n):
            data.edit_canvas_text(text="layer {0}".format(n))

        data.edit_view_new("base")
        data.edit_view_fill("base", True)
        data.edit_view_color("base", color="#c0c0c0")

        #data.window_for_event(processing=click_start, user_event="Button-1")
        data.layer_label_number = layer_label_number
        return data
