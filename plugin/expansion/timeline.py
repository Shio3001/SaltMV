# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation

    # def get_all_elements(self)

    def main(self):

        self.data.new_canvas("timeline")

        self.data.new_parts("timeline", parts_name="shape")

        print(self.data.canvas_data)

        return self.data


class CentralRole:
    pass
