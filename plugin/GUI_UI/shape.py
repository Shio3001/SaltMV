class parts:
    def UI_set(self, data):
        data.new_territory("main")
        data.new_diagram("main", "1")
        data.new_diagram("main", "2")
        data.new_diagram("main", "3")
        data.new_diagram("main", "4")
        data.new_diagram("main", "5")

        data.edit_territory_size("main", x=1000, y=1000)
        data.edit_territory_position("main", x=50, y=50)
        data.edit_diagram_color("main", "1", color="#00ff00")
        data.edit_diagram_fill("main", "1", True)

        data.edit_diagram_fill("main", "2", False)
        data.edit_diagram_size("main", "2", x=20, y=30)
        data.edit_diagram_color("main", "2", color="#ffff00")
        data.edit_diagram_position("main", "2", x=100, y=80)

        data.edit_diagram_fill("main", "3", False)
        data.edit_diagram_size("main", "3", x=50, y=50)
        data.edit_diagram_color("main", "3", color="#0000FF")
        data.edit_diagram_position("main", "3", x=100, y=80)

        data.territory_draw("main")

        def test_minasan(event):
            print("みなさんこんにちは")

            data.diagram_stack("main", "3", True)

        def test_minasan_konnbanha(event):
            print("みなさんこんばんは")

            data.diagram_stack("main", "3", False)

        print("a")

        print(data.get_territory_event("main"))

        data.add_territory_event("main", "Button-1", test_minasan)
        data.add_territory_event("main", "Button-2", test_minasan_konnbanha)
        #data.add_territory_event("main", "Button-1", test_minasan)
        # data.all_del_territory_event("main")

        print(data.get_territory_event("main"))

        print("b")

        #print(data.get_territory_event("main"), "こんばんは")
        return data
