# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def main(self, user_select):
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
