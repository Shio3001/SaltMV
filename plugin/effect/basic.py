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
        setting_effect.effectPoint = [{"time": 0, "x": 0, "y": 0, " z_angle ": 0, " alpha ": 100, "size": 0}]
        setting_effect.various_fixed = {}
        setting_effect.procedure = CentralRole()
        setting_effect.calculation_mode = True

        return setting_effect


class CentralRole:
    def __init__(self):
        self.starting_point = 0

    def main(self, draw, whereabouts):
        return draw, self.starting_point
