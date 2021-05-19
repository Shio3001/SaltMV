class parts:
    def __init__(self):
        print("")

    def UI_set(self, data):
        data.edit_territory_position(x=100, y=100)
        data.edit_territory_size(x=100, y=20)
        data.new_diagram("background")

        data.edit_diagram_fill("background", True)
        data.edit_diagram_color("background", "#ffffff")

        data.new_diagram("text", diagram_type="text")
        data.edit_diagram_text("text", text="てすと", center=True, font_size=20)

        data.diagram_stack("text", True)

        data.territory_draw()

        return data
