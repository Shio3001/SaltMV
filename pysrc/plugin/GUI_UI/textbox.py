class parts:
    def UI_set(self, UI_auxiliary):
        UI_auxiliary.new_diagram("textbox", diagram_type="textbox")

        UI_auxiliary.edit_diagram_position("textbox", x=200, y=0)
        UI_auxiliary.edit_diagram_size("textbox", x=20, y=20)
        UI_auxiliary.territory_draw()

        return UI_auxiliary
