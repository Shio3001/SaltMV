# coding:utf-8
import sys
import numpy as np
import os
import copy

import json
from collections import OrderedDict
import pprint


class Center:
    def input(self, all_elements, user_select):  # 読み込み
        pass

    def input_defrost(self):
        pass

    def output(self, all_elements, user_select):  # 書き出し
        outputdata = json.dumps(all_elements, default=self.output_frozen, indent=2)
        print(outputdata)

        user_select += ".json"

        os.system("touch " + user_select)

        print(user_select)
        with open(user_select, mode='w') as f:
            f.write(outputdata)

    def output_frozen(self, item):
        if isinstance(item, object) and hasattr(item, '__dict__'):
            return item.__dict__
        else:
            raise TypeError
