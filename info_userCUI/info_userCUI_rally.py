# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def __init__(self, set_point, edit_point, printlayer):
        self.toset_edit_point_Center = edit_point.Center()
        self.toset_set_point_Center = set_point.Center()
        self.printlayer_Center = printlayer.PrintLayer()
