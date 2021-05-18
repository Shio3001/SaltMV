

class parts:
    def UI_set(self, data):

        pos_y_normal = 25

        text_x = 0
        textbox1_x = 100
        textbox2_x = 200

        data.new_diagram("text", diagram_type="text")
        #data.edit_diagram_position("text", x=0, y=pos_y_normal)
        data.edit_diagram_size("text", x=180, y=20)
        data.edit_diagram_text("text", font_size=20)

        data.new_diagram("textbox1", diagram_type="textbox")
        #data.edit_diagram_position("textbox1", x=200, y=pos_y_normal)
        data.edit_diagram_size("textbox1", x=180, y=20)

        data.new_diagram("textbox2", diagram_type="textbox")
        #data.edit_diagram_position("textbox2", x=400, y=pos_y_normal)
        data.edit_diagram_size("textbox2", x=180, y=20)
        # data.territory_draw()

        def parameter_ui_set(motion=False, column=0, text=None, text_a=None, text_b=None):
            pos_y = pos_y_normal * column
            data.edit_diagram_text("text", text=text)
            data.edit_diagram_text("textbox1", text=text_a)
            data.edit_diagram_text("textbox2", readonly=1-motion, text=text_b)
            data.edit_diagram_position("text", x=text_x, y=pos_y)
            data.edit_diagram_position("textbox1", x=textbox1_x, y=pos_y)
            data.edit_diagram_position("textbox2", x=textbox2_x, y=pos_y)

            # print("わわわ")

            data.territory_draw()

        data.parameter_ui_set = parameter_ui_set

        return data
