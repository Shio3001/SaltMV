# coding:utf-8
import sys
import numpy
import os
import copy

# 削除厳禁！


class InitialValue:
    def __init__(self):
        pass

    def main(self, elements):
        setting_effect = elements.effectElements()
        setting_effect.effectname = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effectPoint = [{"time": 0, "letter_spacing": 0}]
        setting_effect.various_fixed = {"placement_width": 0, "placement_height": 0}
        setting_effect.procedure = CentralRole()
        setting_effect.calculation_mode = True

        return setting_effect


class CentralRole:
    def __init__(self):
        self.starting_point = 0

    def main(self, draw, whereabouts, now_frame, editor, draw_operation):
        return draw, self.starting_point
