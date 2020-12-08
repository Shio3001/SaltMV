
# coding:utf-8
import sys
import numpy as np
import os
import copy


class Center:
    def __init__(self):
        pass

    def main(self, all_elements, elements):
        all_elements.layer_group.append(elements.layerElements())  # レイヤー追加
        return all_elements
