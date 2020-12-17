# coding:utf-8
import sys
import numpy
import os
import copy

this_os = str(os.name)
if this_os == "nt":
    slash = "¥"
else:
    slash = "/"


class CentralRole:
    def main(self, user_select):
        user_select_hold = ""
        now_directory = os.getcwd()

        for i in range(len(user_select)):
            if user_select[i-2: i+1] == "..{0}".format(slash):
                os.chdir('..{0}'.format(slash))
                user_select_hold = ""
            elif user_select[i] == "{0}".format(slash) and int(len(user_select_hold)) != 0:
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
