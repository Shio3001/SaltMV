class parts:
    def UI_set(self, data):
        data.new_territory("main")
        data.new_diagram("main", "1")

        data.edit_territory_size("main", x=1000, y=1000)
        data.edit_territory_position("main", x=0, y=0)
        data.edit_diagram_color("main", "1", color="#00ff00")
        data.edit_diagram_fill("main", "1", True)
        data.territory_draw("main")

        def test_minasan():
            print("みなさんこんにちは")

        data.add_territory_event("main", "Button-1", test_minasan)

        print(data.get_territory_contact("main"))

        return data
