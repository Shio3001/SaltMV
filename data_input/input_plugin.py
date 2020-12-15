
# coding:utf-8
import sys
import numpy as np
import os
import copy


class CentralRole:
    def __init__(self):
        pass

    def main(self, thislayer, elements, operation_list, inp_plugin):
        thislayer = operation_list["set"]["input_point"]["CentralRole"].effect_Initial_setting(thislayer, operation_list, elements, inp_plugin)
        return thislayer
