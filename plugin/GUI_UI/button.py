# coding:utf-8
import sys
import os
import copy


class parts:
    def UI_set(self, UI_operation, processing=None, user_event=None):

        data = UI_operation

        data.edit_canvas_text(text=data.text)
        data.edit_canvas_position(width_position=data.canvas_position[0], height_position=data.canvas_position[1])
        data.edit_canvas_size(width_size=data.canvas_size[0], height_size=data.canvas_size[1])
        data.edit_canvas_color(color="#adff2f")

        if not processing is None and not user_event is None:
            data.canvas_for_button(processing=processing, user_event=user_event)

        data.canvas_update()

        print("追加")

        return data  # ボタンのベースを生成
