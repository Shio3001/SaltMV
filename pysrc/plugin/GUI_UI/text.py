class parts:
    def UI_set(self, UI_auxiliary):
        UI_auxiliary.edit_territory_position(x=0, y=0)
        UI_auxiliary.edit_territory_size(x=100, y=100)

        UI_auxiliary.new_diagram("text", diagram_type="text")
        UI_auxiliary.edit_diagram_size("text", x=0, y=0)
        UI_auxiliary.edit_diagram_text("text", text="テキスト", font_size=50)
        UI_auxiliary.edit_diagram_position("text", x=0, y=0)
        UI_auxiliary.edit_diagram_text("text", anchor=0)

        UI_auxiliary.territory_draw()

        return UI_auxiliary
