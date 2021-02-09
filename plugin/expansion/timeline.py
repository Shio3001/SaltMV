# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation

    # def get_all_elements(self)

    def main(self):

        self.operation["log"].write("タイムライン起動")

        display_size = self.data.display_size_get()
        self.data.window_title_set("タイムライン")
        size = [1000, 400]
        self.data.window_size_set(size)
        # self.data.menubar_set(timeline_menubar_list)
        self.operation["log"].write(display_size)

        operation_range = self.data.all_UI_data.timeline_operation_range

        timeline_height = 30

        ui_parts = {}
        ui_parts["parts0"] = self.data.new_parts(parts_name="shape")
        ui_parts["parts1"] = self.data.new_parts(parts_name="shape")

        timeline_bar = []

        layer_frame = []
        layer_label = []

        # layer_frame.layer_number(20)

        for i in range(20):
            layer_frame.append(None)
            layer_frame[i] = self.data.new_parts(parts_name="timeline_frame")
            layer_frame[i].edit_canvas_position(width_position=self.data.all_UI_data.timeline_operation_range[0], height_position=self.data.all_UI_data.timeline_operation_range[1] + i * self.data.all_UI_data.timeline_size)
            canvas_log = layer_frame[i].get_window_data()
            layer_frame[i].edit_canvas_size(width_size=canvas_log["size"][0] - self.data.all_UI_data.timeline_operation_range[0], height_size=1)

            layer_label.append(None)
            layer_label[i] = self.data.new_parts(parts_name="timeline_layer_label")
            layer_label[i].edit_canvas_position(width_position=0, height_position=self.data.all_UI_data.timeline_operation_range[1] + i * self.data.all_UI_data.timeline_size)
            layer_label[i].layer_label_number(i)
            layer_label[i].edit_canvas_size(width_size=self.data.all_UI_data.timeline_operation_range[0], height_size=self.data.all_UI_data.timeline_size)

        timeline_scroll_x = self.data.new_parts(parts_name="scroll_x")
        timeline_scroll_y = self.data.new_parts(parts_name="scroll_y")
        timeline_seekbar = self.data.new_parts(parts_name="timeline_nowtime")
        timeline_seekbar.edit_canvas_position(width_position=100)

        timeline_time_percentage = self.data.new_parts(parts_name="percentage")
        timeline_time_percentage.edit_canvas_position(width_position=operation_range[0] * 0.1, height_position=operation_range[1] * 0.1)
        timeline_time_percentage.edit_canvas_size(width_size=operation_range[0] * 0.8, height_size=operation_range[1] * 0.8)

        # ここまで定義
        # ここから各種設定

        def new_layer():
            self.data.all_data.add_layer_elements()

        def new_scene():
            self.data.all_data.add_scene_elements()

        def timeline_exit():
            self.data.window_open_close(False)

        def new_obj():
            # timeline_bar.append(self.data.new_parts(parts_name="timeline_bar"))
            self.data.all_data.add_object_elements(0)

        menubar_list = [("ファイル", "閉じる", timeline_exit), ("新規", "新規シーン", new_scene, "新規レイヤー", new_layer, "動画", new_obj)]
        self.data.menubar_set(menubar_list)

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
                    operation["log"].write("timeline_seekbar 返却")

                    return

            timeline_seekbar.edit_canvas_position(width_position=this_motion["x"])

        timeline_seekbar.window_for_event(processing=timeline_seekbar_click, user_event="B1-Motion")
        timeline_seekbar.window_for_event(processing=timeline_seekbar_click, user_event="Button-1")

        operation = self.operation

        def window_size_change_event(self):

            canvas_log = ui_parts["parts0"].get_window_data()  # よこ
            ui_parts["parts0"].edit_canvas_position(width_position=0, height_position=0)
            ui_parts["parts0"].edit_canvas_size(width_size=canvas_log["size"][0], height_size=operation_range[1])

            canvas_log = ui_parts["parts1"].get_window_data()  # たて
            ui_parts["parts1"].edit_canvas_position(width_position=0, height_position=operation_range[1])
            ui_parts["parts1"].edit_canvas_size(width_size=operation_range[0], height_size=canvas_log["size"][1] - operation_range[1])

            operation["log"].write(timeline_scroll_x.scrollbar_position)

            canvas_log = timeline_scroll_x.get_window_data()
            timeline_scroll_x.edit_canvas_size(width_size=canvas_log["size"][0] - operation_range[0] - timeline_scroll_y.canvas_size[0])
            timeline_scroll_x.edit_canvas_position(width_position=operation_range[0], height_position=canvas_log["size"][1] - timeline_scroll_x.canvas_size[1])
            timeline_scroll_x.change_size_position()  # スクロールバーの割合調整

            canvas_log = timeline_scroll_y.get_window_data()
            timeline_scroll_y.edit_canvas_size(height_size=canvas_log["size"][1] - operation_range[1] - timeline_scroll_x.canvas_size[1])
            timeline_scroll_y.edit_canvas_position(width_position=canvas_log["size"][0] - timeline_scroll_y.canvas_size[0], height_position=operation_range[1])
            timeline_scroll_y.change_size_position()  # スクロールバーの割合調整

            operation["log"].write(timeline_scroll_x.scrollbar_position)

        self.data.window_event(processing=window_size_change_event, user_event="Configure")

        self.data.all_data.file_output("../log/test1.json")
        return self.data


class CentralRole:
    pass
