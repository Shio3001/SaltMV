class parts:
    def __init__(self):
        print("")

    def UI_set(self, UI_auxiliary):

        UI_auxiliary.callback_operation = UI_auxiliary.operation["plugin"]["other"]["callback"].CallBack()

        UI_auxiliary.edit_territory_position(x=100, y=100)
        UI_auxiliary.edit_territory_size(x=100, y=20)
        UI_auxiliary.new_diagram("background")

        UI_auxiliary.edit_diagram_fill("background", True)
        UI_auxiliary.edit_diagram_color("background", "#ffffff")

        UI_auxiliary.new_diagram("text", diagram_type="text")
        UI_auxiliary.edit_diagram_text("text", text="てすと", center=True, font_size=20)

        UI_auxiliary.territory_draw()

        UI_auxiliary.diagram_stack("text", True)

        def click(event=None):
            # print(UI_auxiliary.option_data)
            print("button_click通過")
            UI_auxiliary.callback_operation.event("button", info=UI_auxiliary.option_data)

        UI_auxiliary.add_territory_event("ButtonPress-1", click)

        return UI_auxiliary
