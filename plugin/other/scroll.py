class CentralRole:
    def main(self, data, direction):

        data.direction = int(direction)

        data.new_territory("main")
        data.new_diagram("main", "back")
        data.edit_diagram_fill("main", "back", True)
        data.edit_diagram_color("main", "back", "#111111")

        data.new_diagram("main", "preview")
        data.edit_diagram_fill("main", "preview", False)
        data.edit_diagram_color("main", "preview", "#00aaaa")

        data.drawing_area = [0, 0]  # 実数値の描画域

        data.percentage = [0, 100]  # pos,size

        def edit_percentage_percentage(position=None, size=None):

            data.percentage = data.common_control.xy_compilation(data.percentage, x=position, y=size)

            print("率", data.percentage)

            drawing_area_length = data.drawing_area[1] - data.drawing_area[0]
            size_section = drawing_area_length * (data.percentage[1] / 100)
            pos_section = drawing_area_length * (data.percentage[0] / 100) + data.drawing_area[0]  # 描画域をたすよ

            print(pos_section)

            if data.direction == 0:
                data.edit_diagram_position("main", "preview", x=pos_section)
                data.edit_diagram_size("main", "preview", x=size_section)

            if data.direction == 1:
                data.edit_diagram_position("main", "preview", y=pos_section)
                data.edit_diagram_size("main", "preview", y=size_section)

            data.diagram_draw("main", "preview")

        def edit_size(x=None, y=None, space=None):  # space:百分率のうち0~49
            territory_size = data.edit_territory_size("main", x=x, y=y)
            print(territory_size)
            space_length = territory_size[data.direction] * (space / 100)  # 実数値 一つ当たりの余白

            data.drawing_area = [space_length, territory_size[data.direction] - space_length]  # 実数値 #スクロールバーが動く範囲

            print("描画範囲決定: {0}".format(data.drawing_area))

            # ここから xの時y,yの時xに数値固定をさせるために

            size = [None, None]
            pos = [None, None]
            size[1-data.direction] = territory_size[1-data.direction]
            pos[1-data.direction] = 0

            data.edit_diagram_size("main", "preview", x=size[0], y=size[1])
            data.edit_diagram_position("main", "preview", x=pos[0], y=pos[1])

            # ここまで

            data.territory_draw("main")

        def click_sta(event):
            data.preview_mouse_sta, _, data.preview_join_sta = data.get_diagram_contact("main", "preview")
            data.start_distance = data.preview_mouse_sta[data.direction] - data.edit_diagram_position("main", "preview")[data.direction]

            print("差分", data.start_distance)

        def click_mov(event):
            if data.preview_join_sta[2]:
                preview_mouse, _, _ = data.get_diagram_contact("main", "preview")
                pos_percentage = (preview_mouse[data.direction] - data.start_distance - data.drawing_area[0]) / (data.drawing_area[1] - data.drawing_area[0])

                data.edit_percentage_percentage(position=pos_percentage * 100)

        def click_end(event):
            _, _, data.preview_join_sta = data.get_diagram_contact("main", "preview", del_mouse=True)

        data.add_diagram_event("main", "preview", "Button-1", click_sta)
        data.add_diagram_event("main", "preview", "B1-Motion", click_mov)
        data.add_diagram_event("main", "preview", "ButtonRelease-1", click_end)

        data.edit_size = edit_size
        data.edit_percentage_percentage = edit_percentage_percentage
        data.edit_size(0, 0, 0)
        data.edit_percentage_percentage(position=0, size=50)

        return data
