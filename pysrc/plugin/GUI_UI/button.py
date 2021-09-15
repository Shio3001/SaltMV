class parts:
    def __init__(self):
        print("")

    def UI_set(self, UI_data):

        UI_data.callback_operation = UI_data.operation["plugin"]["other"]["callback"].CallBack()

        UI_data.edit_territory_position(x=100, y=100)
        UI_data.edit_territory_size(x=100, y=20)
        UI_data.new_diagram("background")

        UI_data.edit_diagram_fill("background", True)
        UI_data.edit_diagram_color("background", "#ffffff")

        UI_data.new_diagram("text", diagram_type="text")
        UI_data.edit_diagram_text("text", text="てすと", center=True, font_size=20)

        UI_data.diagram_stack("text", True)

        UI_data.territory_draw()

        def click(event=None):
            # print(UI_data.option_data)
            print("button_click通過")
            UI_data.callback_operation.event("button", info=UI_data.option_data)

        UI_data.add_territory_event("ButtonPress-1", click)

        return UI_data
