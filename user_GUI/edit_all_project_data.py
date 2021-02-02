# coding:utf-8
import sys
import os
import copy

# GUI用
# CUIと違い、一本の道筋で管理することがすごくしんどいのでここですべて管理するs


class CentralRole:
    def __init__(self):
        self.all_elements = None

    def set_all_elements(self, send_all_elements):
        self.all_elements = send_all_elements
