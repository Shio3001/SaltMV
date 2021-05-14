# coding:utf-8
import sys
import os
import copy

# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effect_point = [{"time": 0}]
        setting_effect.various_fixed = {"path": ""}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = 0

    def main(self, data):
        return data.draw, self.starting_point
