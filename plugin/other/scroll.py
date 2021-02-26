class CentralRole:
    def main(self, data, direction):

        data.direction = int(direction)

        data.new_territory("main")
        data.new_diagram("main", "back")
        data.edit_diagram_fill("main", "back", True)
        data.edit_diagram_color("main", "back", "#111111")

        data.new_diagram("main", "preview")
        data.edit_diagram_fill("main", "preview", False)
        data.edit_diagram_color("main", "preview", "#ff00ff")

        data.drawing_area = [0, 0]  # 実数値の描画域

        # def edit_percentage_territory(self, p):
        #    pass

        def edit_percentage_percentage(pos_p, size_p):
            drawing_area_length = data.drawing_area[1] - data.drawing_area[0]

            print(drawing_area_length)

            pos_section = drawing_area_length * (pos_p / 100) + data.drawing_area[0]
            size_section = drawing_area_length * (size_p / 100)

            print(pos_section, size_section)

            if data.direction == 0:
                data.edit_diagram_size("main", "preview", x=size_section)
                data.edit_diagram_position("main", "preview", x=pos_section)

            if data.direction == 1:
                data.edit_diagram_size("main", "preview", y=size_section)
                data.edit_diagram_position("main", "preview", y=pos_section)

            data.territory_draw("main")

        def edit_size(x=None, y=None, space=None):  # space:百分率のうち0~49
            territory_size = data.edit_territory_size("main", x=x, y=y)
            print(territory_size)
            space_length = territory_size[data.direction] * (space / 100)  # 実数値

            data.drawing_area = [space_length, territory_size[data.direction] - space_length]  # 実数値

            if data.direction == 0:
                data.edit_diagram_size("main", "preview", y=territory_size[1])
                data.edit_diagram_position("main", "preview", y=0)

            if data.direction == 1:
                data.edit_diagram_size("main", "preview", x=territory_size[1])
                data.edit_diagram_position("main", "preview", x=0)

            data.territory_draw("main")

        data.edit_size = edit_size
        data.edit_size(400, 20, 5)

        data.edit_percentage_percentage = edit_percentage_percentage
        data.edit_percentage_percentage(0, 100)

        return data
