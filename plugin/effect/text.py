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
        setting_example = elements.effectElements()
        setting_example.effectname = str(os.path.basename(__file__)).replace('.py', '')
        setting_example.effectPoint = [{"time": 0, "letter_spacing": 0}]
        setting_example.various_fixed = {"placement_width": 0, "placement_height": 0}
        setting_example.procedurelist = CentralRole()
        setting_example.calculation_mode = True

        return setting_example


class CentralRole:
    def __init__(self):
        pass

    def main(self, adjusted_draw, whereabouts):
        return adjusted_draw
