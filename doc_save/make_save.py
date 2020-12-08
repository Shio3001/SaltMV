# coding:utf-8
import sys
import numpy as np
import os
import copy

import json
import pickle
import base64


class Center:
    def __init__(self):
        self.extension = ".json"  # 拡張子

    def input(self, all_elements, elements, operation_list, user_select):  # json -> class 読み込み
        if user_select[-5:] != self.extension:
            user_select += self.extension
        lordfile = open(user_select, 'rb')
        #all_elements = lordfile
        all_elements = pickle.load(lordfile)
        save_location = copy.deepcopy(user_select)
        return all_elements, save_location

    def output(self, all_elements, elements, operation_list, user_select):  # class -> json書き出し
        #outputdata = json.dumps(all_elements, default=self.output_frozen, indent=2)
        # print(outputdata)

        if user_select[-5:] != self.extension:
            user_select += self.extension
        user_select = operation_list["other"]["dircon"]["Center"].main(user_select)
        os.system("touch " + user_select)
        print(user_select)

        openfile = open(user_select, 'wb')
        pickle.dump(all_elements, openfile, protocol=5)
        openfile.close()

        save_location = copy.deepcopy(user_select)
        # with open(user_select, mode='w') as f:
        #    f.write(outputdata)
        return all_elements, save_location
