# coding:utf-8
import sys
import os
import copy
import datetime
import ffmpeg
import numpy as np
# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effect_point = {"number": 0}
        setting_effect.various_fixed = {"name": ""}

        setting_effect.procedure = CentralRole()

        # setting_effect.cpp = "read_video"


class CentralRole:
    def __init__(self):
        pass

    def main(self, rendering_main_data):
        name = rendering_main_data.various_fixed["name"]
        number = rendering_main_data.effect_value["number"]

        return "ACCOMPANY", name, number
