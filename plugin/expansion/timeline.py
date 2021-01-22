# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.timeline = data

    def main(self):

        def exit():
            self.timeline.window.destroy()

        # timeline_menubar_list = [
        #    ("ウインドウ", [("閉じる", exit)])
        # ]

        display_size = self.timeline.display_size_get()
        self.timeline.window_title_set("タイムライン")
        size = [1000, 400]
        self.timeline.window_size_set(size)
        # self.timeline.menubar_set(timeline_menubar_list)
        print(display_size)

        timeline_height = 50

        ui_parts = []

        ui_parts.append(self.timeline.new_parts(parts_name="shape"))

        # ui_parts[0].tag_raise()

        def ui_parts_0_resize(event):  # 画面上側の灰色
            canvas_log = ui_parts[0].get_window_data()
            ui_parts[0].edit_canvas_position(width_position=0, height_position=0)
            ui_parts[0].edit_canvas_size(width_size=canvas_log["size"][0], height_size=30)
        ui_parts[0].window_for_event(processing=ui_parts_0_resize, user_event="Configure")

        ui_parts.append(self.timeline.new_parts(parts_name="shape"))

        # ui_parts[1].tag_raise()

        def ui_parts_1_resize(event):  # 画面下側の灰色
            canvas_log = ui_parts[1].get_window_data()
            ui_parts[1].edit_canvas_position(width_position=0, height_position=30)
            ui_parts[1].edit_canvas_size(width_size=100, height_size=canvas_log["size"][1] - 30)
        ui_parts[1].window_for_event(processing=ui_parts_1_resize, user_event="Configure")

        # ----

        # ----

        timeline_seekbar = self.timeline.new_parts(parts_name="timeline_nowtime")
        timeline_seekbar.edit_canvas_position(width_position=100)

        if timeline_seekbar.nowtime_mov == False:
            return

        # ----

        timeline_bar = []

        timeline_bar.append(self.timeline.new_parts(parts_name="timeline_bar"))
        timeline_bar[0].edit_timeline_height(timeline_height)

        timeline_bar.append(self.timeline.new_parts(parts_name="timeline_bar"))
        timeline_bar[0].edit_canvas_position(width_position=300)
        timeline_bar[1].edit_timeline_height(timeline_height)

        def timeline_bar_click(evet):

            print("barの数: {0}".format(len(timeline_bar)))

            for tlb_one in timeline_bar:
                bar_touch = tlb_one.first_touch
                bar_within = tlb_one.first_canvas_within
                this_motion, this_touch, this_within = timeline_seekbar.get_mouse_position()
                if not bar_within["xy"] and not bar_touch["left"] and not bar_touch["right"]:
                    pass
                else:
                    return

            timeline_seekbar.edit_canvas_position(width_position=this_motion["x"])

        timeline_seekbar.window_for_event(processing=timeline_bar_click, user_event="B1-Motion")
        timeline_seekbar.window_for_event(processing=timeline_bar_click, user_event="Button-1")

        test_frame = []

        for i in range(20):
            test_frame.append(None)
            test_frame[i] = self.timeline.new_parts(parts_name="timeline_frame")
            test_frame[i].edit_canvas_position(height_position=i * timeline_height)
            # test_frame[i].edit_canvas_size(height_size=5)

        return self.timeline


class CentralRole:
    pass
