class CentralRole:
    def main(self, data, direction):

        data.new_territory("main")
        data.new_diagram("main", "back")
        data.new_diagram("main", "view")

        data.edit_diagram_fill("main", "back", True)
        data.edit_diagram_fill("main", "view", False)

        data.drawing_area = [0, 0]
        # territory左上を0,0とした基準で、描画可能範囲を記入します
        # 配列0番 : territory起点からパーセント起点まで 実数表示!
        # 配列1番 : パーセント終点からterritory終点まで 実数表示!

        data.percent_range = [0, 0]
        # 配列0番 : territory起点からパーセント起点まで 割合表示！
        # 配列1番 : パーセント終点からterritory終点まで 割合表示！

        data.click_distance = 0
        # クリックした場所から,パーセント起点まで、どれだけの距離があるかどうかを計算 実数表示！

        def edit_size(x=None, y=None):
            pass

        def edit_percent_position(percent):
            pass

        def edit_percent_size(percent):
            pass

        def click_start(event):
            pass

        def click_mov(event):
            pass

        def click_end(event):
            pass

        data.add_diagram_event("main", "view", "Button-1", click_start)
        data.window_event_data["add"]("Motion", click_mov)
        data.add_diagram_event("main", "view", "ButtonRelease-1", click_end)

        data.territory_draw("main")

        return data
