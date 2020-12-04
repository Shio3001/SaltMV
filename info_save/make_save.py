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
        inputdata = json.loads(user_select)

    def input_defrost(self):
        pass

    def output(self, all_elements, user_select):  # 書き出し
        outputdata = json.dumps(all_elements, default=self.output_frozen, indent=2)
        print(outputdata)

        if user_select[-5:] != ".json":
            user_select += ".json"

        user_select_hold = ""
        now_directory = os.getcwd()
        for i in range(len(user_select)):
            if user_select[i-2: i+1] == "../":
                os.chdir('../')
                user_select_hold = ""
            elif user_select[i] == "/" and int(len(user_select_hold)) != 0:
                os.system("mkdir " + str(user_select_hold))
                os.chdir(user_select_hold)
                user_select_hold = ""
            elif user_select[i] == ".":
                pass
            elif user_select[i] == " ":
                pass
            else:
                user_select_hold += user_select[i]

        os.chdir(now_directory)
        os.system("touch " + user_select)

        print(user_select)
        with open(user_select, mode='w') as f:
            f.write(outputdata)

    def output_frozen(self, item):
        # if isinstance(item, object) and hasattr(item, '__dict__'):
        print("json : " + str(item.__dict__))
        return item.__dict__
        # else:
        #    raise TypeError
