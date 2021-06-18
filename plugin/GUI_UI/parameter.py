

class parts:
    def UI_set(self, data):

        pos_y_normal = 25

        text_x = 0
        textbox1_x = 100
        textbox2_x = 300

        data.new_diagram("text", diagram_type="text")
        #data.edit_diagram_position("text", x=0, y=pos_y_normal)
        data.edit_diagram_size("text", x=100, y=20)
        data.edit_diagram_text("text", font_size=20)

        data.new_diagram("textbox1", diagram_type="textbox")
        #data.edit_diagram_position("textbox1", x=200, y=pos_y_normal)
        data.edit_diagram_size("textbox1", x=100, y=20)

        data.new_diagram("textbox2", diagram_type="textbox")
        #data.edit_diagram_position("textbox2", x=400, y=pos_y_normal)
        data.edit_diagram_size("textbox2", x=100, y=20)

        def textbox1(text):
            print(text)

        def textbox2(text):
            print(text)

        def parameter_ui_set(motion=False, column=0, text=None, text_a=None, text_b=None, text_a_return=None, text_b_return=None, text_fixed=None):
            pos_y = pos_y_normal * column
            data.edit_diagram_text("text", text=text)
            data.edit_diagram_text("textbox1", text=text_a,  entry_event=text_a_return)
            data.edit_diagram_text("textbox2", readonly=1-motion, text=text_b, entry_event=text_b_return)

            data.edit_diagram_position("text", x=text_x, y=pos_y)
            data.edit_diagram_position("textbox1", x=textbox1_x, y=pos_y)

            print("text_a, text_b", text_a, text_b)

            data.edit_diagram_position("textbox2", x=textbox2_x, y=pos_y)

            if text_fixed:
                data.diagram_forget("textbox2", True)
                data.edit_diagram_size("textbox1", x=textbox2_x - textbox1_x + 100)
                data.edit_diagram_text("textbox1", set_int_type=False)
                data.edit_diagram_text("textbox2", set_int_type=False)

            else:
                data.diagram_forget("textbox2", False)
                data.edit_diagram_size("textbox1", x=100, y=20)
                data.edit_diagram_text("textbox1", set_int_type=True)
                data.edit_diagram_text("textbox2", set_int_type=True)

            data.territory_draw()

        data.parameter_ui_set = parameter_ui_set

        return data
