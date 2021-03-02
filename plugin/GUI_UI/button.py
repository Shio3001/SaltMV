class parts:
    def __init__(self):
        print("")

    def UI_set(self, data):
        data.edit_territory_position(x=100, y=100)
        data.edit_territory_size(x=100, y=100)
        data.new_diagram("0")
        data.edit_diagram_fill("0", True)
        data.edit_diagram_color("0", "#ffffff")
        data.territory_draw()

        return data
