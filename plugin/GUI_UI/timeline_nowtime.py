class parts:
    def UI_set(self, data):
        data.new_diagram("now")
        data.edit_diagram_size("now", x=100, y=20)
        data.edit_diagram_position("now", x=100, y=0)
        data.edit_diagram_color("now", "#ff0000")
        data.territory_draw()
        data.territory_stack(False)

        return data
