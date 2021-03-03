class parts:
    def __init__(self):
        print("")

    def UI_set(self, data):
        data.edit_territory_position(x=100, y=100)
        data.edit_territory_size(x=100, y=100)
        data.new_diagram("0")

        data.edit_diagram_fill("0", True)
        data.edit_diagram_color("0", "#ffffff")

        data.new_diagram("text", diagram_type="text")

        # , font_type=data.font_data["ArabicUIText.ttc"]
        #data.edit_diagram_text("text", text="これはボタン", center=True, target="0")
        data.edit_diagram_text("text", text="てすと", center=True, target="0")

        data.territory_draw()

        #data.add_territory_event(None, None)

        return data
