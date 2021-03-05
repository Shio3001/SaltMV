class parts:
    def UI_set(self, data):
        data.new_diagram("textbox", diagram_type="textbox")

        data.edit_diagram_position("textbox", x=200, y=0)
        data.edit_diagram_size("textbox", x=20, y=20)
        #print("textbox class ID", data)
        data.territory_draw()

        return data
