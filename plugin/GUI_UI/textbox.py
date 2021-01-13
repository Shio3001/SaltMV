# coding:utf-8
import sys
import os
import copy


class parts:
    def UI_set(self, UI_operation):
        data = [None, None]
        data[0] = UI_operation
        data[1] = UI_operation
        data[0].textbox_update()
        data[1].canvas_update()

        return data
