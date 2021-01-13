# coding:utf-8
import sys
import os
import copy

# Buttonのテンプレートを作成


class parts:
    def UI_set(self, UI_operation):
        data = UI_operation

        data.edit_view_new("a")
        data.set_view_fill_on("a")

        data.edit_canvas_text(text="これはぼたん")
        data.edit_canvas_position(width_position=0, height_position=0)
        data.edit_canvas_size(width_size=100, height_size=20)
        data.edit_canvas_color(color="#adff2f")
        data.canvas_for_button(processing=data.processing, user_event=data.user_event)

        data.edit_view_new("b")
        data.edit_view_color("b", color="#ffff00")
        data.edit_view_size("b", width_size=20, height_size=10)
        data.edit_view_position("b", width_position=80, height_position=0)

        print("追加")

        return data  # ボタンのベースを生成
