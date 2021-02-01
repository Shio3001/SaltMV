class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        def layer_label_number(n):
            data.edit_canvas_text(text="layer {0}".format(n))

        data.layer_label_number = layer_label_number
        return data
