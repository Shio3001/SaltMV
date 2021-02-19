class parts:
    def UI_set(self, data):
        data.new_territory("main")
        data.new_territory("main2")

        data.edit_territory_position("main", x=0, y=0)
        data.edit_territory_position("main2", x=100, y=100)

        data.edit_territory_size("main", x=200, y=200)
        data.edit_territory_size("main2", x=200, y=200)

        data.new_diagram("main", "1")
        data.new_diagram("main2", "2")
        data.new_diagram("main2", "3")
        data.new_diagram("main2", "4")

        data.edit_diagram_fill("main", "1", True)
        data.edit_diagram_fill("main2", "2", True)

        data.edit_diagram_color("main", "1", "#00ff00")
        data.edit_diagram_color("main2", "2", "#0000ff")
        data.edit_diagram_color("main2", "3", "#ff0000")
        data.edit_diagram_color("main2", "4", "#00ffff")

        data.edit_diagram_position("main2", "3", x=50, y=50)
        data.edit_diagram_size("main2", "3", x=100, y=30)

        data.edit_diagram_position("main2", "4", x=5, y=5)
        data.edit_diagram_size("main2", "4", x=50, y=50)

        data.territory_draw("main")
        data.territory_draw("main2")

        def test_minasan(event):
            print("みなさんこんにちは")

            data.territory_stack("main2", True)

        def test_minasan_konnbanha(event):
            print("みなさんこんばんは")

            data.territory_stack("main", True)

        def move(event):
            print(data.get_territory_contact("main2"))

        data.add_territory_event("main", "Button-1", test_minasan)
        data.add_territory_event("main2", "Button-1", test_minasan_konnbanha)
        data.add_territory_event("main2", "Motion", move)

        print(data.get_territory_event("main"))

        print("b")

        #print(data.get_territory_event("main"), "こんばんは")
        return data
