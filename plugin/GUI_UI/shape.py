class parts:
    def UI_set(self, data):
        data.new_territory("main")
        data.new_diagram("main", "1")
        #data.new_diagram("main", "2")
        #data.new_diagram("main", "3")
        #data.new_diagram("main", "4")
        #data.new_diagram("main", "5")

        data.edit_territory_size("main", x=10, y=10)
        data.edit_territory_position("main", x=50, y=50)
        data.edit_diagram_color("main", "1", color="#00ff00")
        data.edit_diagram_fill("main", "1", True)
        data.territory_draw("main")

        def test_minasan(event):
            print("みなさんこんにちは")

        def test_minasan_konnbanha(event):
            print("みなさんこんばんは")

        data.add_diagram_event("main", "1", "Button-1", test_minasan)
        data.del_diagram_event("main", "1", "Button-1", test_minasan)

        print("a")

        print(data.get_territory_event("main"))

        #data.add_territory_event("main", "Button-1", test_minasan_konnbanha)
        #data.del_territory_event("main", "Button-1", test_minasan_konnbanha)

        print(data.get_territory_event("main"))

        print("b")

        #print(data.get_territory_event("main"), "こんばんは")
        return data
