# coding:utf-8
import os


class ClassVarToDict:
    def get(self, class_data, inquiry=None):
        if not inquiry is None:
            ans = True if str(inquiry) in class_data.__dict__.keys() else False
            return ans

        dict_data = class_data.__dict__

        return dict_data
