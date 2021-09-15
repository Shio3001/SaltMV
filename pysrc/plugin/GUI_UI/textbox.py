class parts:
    def UI_set(self, UI_data):
        UI_data.new_diagram("textbox", diagram_type="textbox")

        UI_data.edit_diagram_position("textbox", x=200, y=0)
        UI_data.edit_diagram_size("textbox", x=20, y=20)
        UI_data.territory_draw()

        return UI_data
