# coding:utf-8
import sys
import numpy as np
import os
import copy

import json
import pickle
import base64


class Center:
    def input(self, all_elements, elements, user_select):  # json -> class 読み込み
        if user_select[-5:] != ".json":
            user_select += ".json"
        lordfile = open(user_select, 'rb')
        #all_elements = lordfile
        all_elements = pickle.load(lordfile)
        return all_elements

    def output(self, all_elements, elements, user_select):  # class -> json書き出し
        #outputdata = json.dumps(all_elements, default=self.output_frozen, indent=2)
        # print(outputdata)

        if user_select[-5:] != ".json":
            user_select += ".json"
        user_select = self.DirectoryConversion(user_select)
        os.system("touch " + user_select)
        print(user_select)

        openfile = open(user_select, 'wb')
        pickle.dump(all_elements, openfile, protocol=5)
        openfile.close()
        # with open(user_select, mode='w') as f:
        #    f.write(outputdata)
        return all_elements

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
