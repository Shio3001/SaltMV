class parts:
    def UI_set(self, UI_auxiliary):
        UI_auxiliary.edit_territory_position(x=0, y=0)
        UI_auxiliary.edit_territory_size(x=100, y=100)
        UI_auxiliary.new_diagram("0")
        UI_auxiliary.edit_diagram_fill("0", True)
        UI_auxiliary.edit_diagram_color("0", UI_auxiliary.GUI_alpha_color)
        UI_auxiliary.territory_draw()
        return UI_auxiliary
