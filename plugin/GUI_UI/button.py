class parts:
    def __init__(self):
        print("")

    def UI_set(self, data):

        data.button_color = "#00ff00"

        data.new_territory("main")
        data.edit_territory_position("main", x=100, y=100)
        data.edit_territory_size("main", x=100, y=100)

        data.new_diagram("main", "0")
        data.edit_diagram_fill("main", "0", False)

        data.edit_diagram_position("main", "0", x=50, y=50)
        data.edit_diagram_size("main", "0", x=50, y=50)
        data.edit_diagram_color("main", "0", "#00ff00")

        data.new_diagram("main", "1", diagram_type="text")
        data.edit_diagram_text("main", "1", "これはボタン")
        #data.edit_diagram_text("main", "0", "ねむい")

        data.territory_draw("main")

        data.add_territory_event("main", "Button-1", data.event_not_func)

        # def

        return data
