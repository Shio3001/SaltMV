class TerritoryData:
    def __init__(self):
        self.size = [100, 100]
        self.position = [0, 0]
        self.blank_space = [10, 20]


class DiagramData:
    def __init__(self):
        self.size = [100, 100]
        self.position = [0, 0]
        self.fill = True


territory_data = TerritoryData()
diagram_data = DiagramData()

print("領　域 座　標 : {0}".format(territory_data.position))
print("領　域 サイズ : {0}".format(territory_data.size))

print("図　形 座　標 : {0}".format(diagram_data.position))
print("図　形 サイズ : {0}".format(diagram_data.size))

print("余　白 : {0}".format(territory_data.blank_space))

xy, size_xy = [0, 0], [0, 0]  # 領域基準

for i in range(2):
    if diagram_data.fill:  # 座標の計算
        xy[i] = territory_data.position[i]
        size_xy[i] = territory_data.size[i]

    else:
        xy[i] = territory_data.position[i] + diagram_data.position[i]
        size_xy[i] = diagram_data.size[i]

    # 左側が図形ー右側が余白反映

    if xy[i] < territory_data.blank_space[i]:
        difference = territory_data.blank_space[i] - xy[i]
        print("左上減算 : {0}".format(difference))

        xy[i] += difference
        size_xy[i] -= difference

    if xy[i] + size_xy[i] > territory_data.position[i] + territory_data.size[i] - territory_data.blank_space[i]:
        difference = (territory_data.position[i] + territory_data.size[i] - territory_data.blank_space[i]) - (xy[i] + size_xy[i])
        print("右下減算 : {0}".format(difference))

        size_xy[i] += difference

print("座　標 : {0}".format(xy))
print("サイズ : {0}".format(size_xy))
