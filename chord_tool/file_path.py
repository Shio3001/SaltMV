# coding:utf-8
import os

this_os = str(os.name)
if this_os == "nt":
    slash = "¥"
else:
    slash = "/"


class DirectoryPath:
    def path_support(self, path):
        path_hold = ""
        now_directory = os.getcwd()

        for i in range(len(path)):
            if path[i-2: i+1] == "..{0}".format(slash):
                os.chdir('..{0}'.format(slash))
                path_hold = ""
            elif path[i] == "{0}".format(slash) and int(len(path_hold)) != 0:
                os.system("mkdir " + str(path_hold))
                os.chdir(path_hold)
                path_hold = ""

            elif path[i] == ".":
                pass
            elif path[i] == " ":
                pass
            else:
                path_hold += path[i]

        os.chdir(now_directory)

        return path
