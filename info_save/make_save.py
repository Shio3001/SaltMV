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

        inputdata = json.load(open(user_select, "r"))
        print(inputdata)

        all_elements = self.input_defrost('inputdata:{}'.format(type(inputdata)))

        return all_elements

    def input_defrost(self, before_conversion):  # 解凍

        all_elements = []

        for i in range(0):  # レイヤー単位
            all_elements.append()
            for j in range(0):  # オブジェクト単位
                for k in range(0):  # エフェクト単位
                    pass

        return all_elements

    def output(self, all_elements, user_select):  # 書き出し
        outputdata = json.dumps(all_elements, default=self.output_frozen, indent=2)
        print(outputdata)

        if user_select[-5:] != ".json":
            user_select += ".json"

        user_select = self.DirectoryConversion(user_select)

        os.system("touch " + user_select)

        print(user_select)
        with open(user_select, mode='w') as f:
            f.write(outputdata)

        return all_elements

    def output_frozen(self, item):  # 冷凍
        # if isinstance(item, object) and hasattr(item, '__dict__'):
        print("json : " + str(item.__dict__))
        return item.__dict__
        # else:
        #    raise TypeError

    def DirectoryConversion(self, user_select):
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

        return user_select
