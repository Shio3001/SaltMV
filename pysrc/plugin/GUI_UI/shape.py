class parts:
    def UI_set(self, data):
        data.edit_territory_position(x=0, y=0)
        data.edit_territory_size(x=100, y=100)
        data.new_diagram("0")
        data.edit_diagram_fill("0", True)
        data.edit_diagram_color("0", data.GUI_alpha_color)
        data.territory_draw()
        return data
