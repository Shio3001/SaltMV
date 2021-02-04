# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.timeline = data
        self.basic_ope = self.timeline.operation

    # def get_all_elements(self)

    def main(self):

        self.basic_ope["log"].write("タイムライン起動")

        display_size = self.timeline.display_size_get()
        self.timeline.window_title_set("タイムライン")
        size = [1000, 400]
        self.timeline.window_size_set(size)
        # self.timeline.menubar_set(timeline_menubar_list)
        self.basic_ope["log"].write(display_size)

        timeline_height = 30

        ui_parts = {}
        ui_parts["parts0"] = self.timeline.new_parts(parts_name="shape")
        ui_parts["parts1"] = self.timeline.new_parts(parts_name="shape")

        timeline_time_percentage = self.timeline.new_parts(parts_name="percentage")

        timeline_bar = []
        """

        timeline_bar.append(self.timeline.new_parts(parts_name="timeline_bar"))
        timeline_bar.append(self.timeline.new_parts(parts_name="timeline_bar"))
        

        timeline_bar[0].edit_timeline_height(timeline_height)
        timeline_bar[0].edit_canvas_position(width_position=300)

        timeline_bar[1].edit_timeline_height(timeline_height)
        timeline_bar[1].edit_view_color("base", color="#1e90ff")
        timeline_bar[1].edit_canvas_text(text="画像")
        timeline_bar[1].edit_canvas_position(width_position=600)
        """

        timeline_time_percentage.edit_canvas_position(width_position=20, height_position=7)

        layer_frame = []
        layer_label = []

        for i in range(20):
            layer_frame.append(None)
            layer_frame[i] = self.timeline.new_parts(parts_name="timeline_frame")
            layer_frame[i].edit_canvas_position(height_position=timeline_height + i * timeline_height)

            layer_label.append(None)
            layer_label[i] = self.timeline.new_parts(parts_name="timeline_layer_label")
            layer_label[i].edit_canvas_position(width_position=0, height_position=timeline_height + i * timeline_height)
            layer_label[i].layer_label_number(i + 1)
            layer_label[i].edit_canvas_size(width_size=100, height_size=timeline_height)

        timeline_scroll_x = self.timeline.new_parts(parts_name="scroll_x")
        timeline_scroll_y = self.timeline.new_parts(parts_name="scroll_y")
        timeline_seekbar = self.timeline.new_parts(parts_name="timeline_nowtime")
        timeline_seekbar.edit_canvas_position(width_position=100)

        # ここまで定義
        # ここから各種設定

        def timeline_exit():
            self.timeline.window_open_close(False)

        def new_obj():
            timeline_bar.append(self.timeline.new_parts(parts_name="timeline_bar"))

        menubar_list = [("ファイル", "閉じる", timeline_exit), ("新規", "動画", new_obj)]
        self.timeline.menubar_set(menubar_list)

        # シークバーを移動させる時、他のオブジェクトに干渉していないか
        def timeline_seekbar_click(evet):
            this_motion, _, _ = timeline_seekbar.get_mouse_position()

            parts = []
            parts.extend(timeline_bar)  # list
            parts.append(timeline_scroll_x)
            parts.append(timeline_scroll_y)
            parts.append(timeline_time_percentage)

            print(parts)
            for r in parts:
                if r.first_canvas_within["xy"] or r.first_touch["left"] or r.first_touch["right"]:
                    basic_ope["log"].write("timeline_seekbar 返却")
                    return

            timeline_seekbar.edit_canvas_position(width_position=this_motion["x"])

        timeline_seekbar.window_for_event(processing=timeline_seekbar_click, user_event="B1-Motion")
        timeline_seekbar.window_for_event(processing=timeline_seekbar_click, user_event="Button-1")

        basic_ope = self.basic_ope

        def window_size_change_event(self):
            canvas_log = ui_parts["parts0"].get_window_data()
            ui_parts["parts0"].edit_canvas_position(width_position=0, height_position=0)
            ui_parts["parts0"].edit_canvas_size(width_size=canvas_log["size"][0], height_size=timeline_height)

            canvas_log = ui_parts["parts1"].get_window_data()
            ui_parts["parts1"].edit_canvas_position(width_position=0, height_position=timeline_height)
            ui_parts["parts1"].edit_canvas_size(width_size=100, height_size=canvas_log["size"][1] - timeline_height)

            basic_ope["log"].write(timeline_scroll_x.scrollbar_position)

            canvas_log = timeline_scroll_x.get_window_data()
            timeline_scroll_x.edit_canvas_size(width_size=canvas_log["size"][0] - 100 - 20)
            timeline_scroll_x.edit_canvas_position(width_position=100, height_position=canvas_log["size"][1] - timeline_scroll_x.canvas_size[1])
            timeline_scroll_x.change_size_position()  # スクロールバーの割合調整

            timeline_scroll_y.edit_canvas_size(height_size=canvas_log["size"][1] - timeline_height - 20)
            timeline_scroll_y.edit_canvas_position(width_position=canvas_log["size"][0] - timeline_scroll_y.canvas_size[0], height_position=timeline_height)
            timeline_scroll_y.change_size_position()  # スクロールバーの割合調整

            basic_ope["log"].write(timeline_scroll_x.scrollbar_position)

        self.timeline.window_event(processing=window_size_change_event, user_event="Configure")
        self.timeline.all_data.add_layer_elements()
        self.timeline.all_data.file_output("../log/test1.json")
        return self.timeline


class CentralRole:
    pass
