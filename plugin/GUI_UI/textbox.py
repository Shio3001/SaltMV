class parts:
    def UI_set(self, data):
        data.new_diagram("textbox", diagram_type="textbox")

        data.edit_diagram_position("textbox", x=100, y=50)
        data.edit_diagram_size("textbox", x=100, y=20)
        #print("textbox class ID", data)
        data.territory_draw()

        return data
