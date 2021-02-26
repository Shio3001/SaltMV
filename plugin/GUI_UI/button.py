class parts:
    def __init__(self):
        print("")

    def UI_set(self, data):
        data.new_territory("main")
        data.edit_territory_position("main", x=100, y=100)
        data.edit_territory_size("main", x=100, y=100)
        data.new_diagram("main", "0")
        data.edit_diagram_fill("main", "0", True)
        data.edit_diagram_color("main", "0", "#ffffff")
        data.territory_draw("main")

        return data
