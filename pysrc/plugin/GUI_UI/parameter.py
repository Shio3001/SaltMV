

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

        def parameter_ui_set(motion=False, column=0, text=None, text_a=None, text_b=None, text_a_return=None, text_b_return=None, text_fixed=None):
            pos_y = pos_y_normal * column
            UI_auxiliary.edit_diagram_text("text", text=text)
            UI_auxiliary.edit_diagram_text("textbox1", text=text_a,  entry_event=text_a_return)
            UI_auxiliary.edit_diagram_text("textbox2", readonly=1-motion, text=text_b, entry_event=text_b_return)

            UI_auxiliary.edit_diagram_position("text", x=text_x, y=pos_y)
            UI_auxiliary.edit_diagram_position("textbox1", x=textbox1_x, y=pos_y)

            #print("text_a, text_b", text_a, text_b)

            UI_auxiliary.edit_diagram_position("textbox2", x=textbox2_x, y=pos_y)

            if text_fixed:
                UI_auxiliary.diagram_forget("textbox2", True)
                UI_auxiliary.edit_diagram_size("textbox1", x=textbox2_x - textbox1_x + 100)
                #UI_auxiliary.edit_diagram_text("textbox1", set_int_type=False)
                #UI_auxiliary.edit_diagram_text("textbox2", set_int_type=False)

            else:
                UI_auxiliary.diagram_forget("textbox2", False)
                UI_auxiliary.edit_diagram_size("textbox1", x=100, y=20)
                #UI_auxiliary.edit_diagram_text("textbox1", set_int_type=True)
                #UI_auxiliary.edit_diagram_text("textbox2", set_int_type=True)

            UI_auxiliary.territory_draw()

        UI_auxiliary.parameter_ui_set = parameter_ui_set

        return UI_auxiliary
