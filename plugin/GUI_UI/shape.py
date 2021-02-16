class parts:
    def UI_set(self, data):
        data.new_territory("main")
        data.new_diagram("main", "1")
        data.edit_territory_size("main", x=100, y=100)
        data.edit_territory_position("main", x=10, y=10)

        data.edit_diagram_fill("main", "1", True)
        data.edit_diagram_color("main", "1", color="#ffffff")

        data.territory_draw("main")

        print(data.get_territory_contact("main"))

        return data
