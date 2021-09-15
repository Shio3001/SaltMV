class parts:
    def UI_set(self, UI_data):
        UI_data.edit_territory_position(x=0, y=0)
        UI_data.edit_territory_size(x=100, y=100)
        UI_data.new_diagram("0")
        UI_data.edit_diagram_fill("0", True)
        UI_data.edit_diagram_color("0", UI_data.GUI_alpha_color)
        UI_data.territory_draw()
        return UI_data
