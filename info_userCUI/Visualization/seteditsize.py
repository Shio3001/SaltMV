# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def __init__(self):
        self.user_select = [0, 0, 0, 0]

    def main(self):
        print("画面サイズ・fps・動画の長さを入力")
        print("一度設定した後にfps値を変更するとおかしくなりますのでご注意ください")
        print("")

        try:
            print("画面横サイズを入力")
            self.user_select[0] = int(sys.stdin.readline().rstrip())
            print("")

            print("画面縦サイズを入力")
            self.user_select[1] = int(sys.stdin.readline().rstrip())
            print("")

            print("fps値を入力")
            self.user_select[2] = int(sys.stdin.readline().rstrip())
            print("")

            print("動画の長さを入力")
            self.user_select[3] = int(sys.stdin.readline().rstrip())
            print("")

            return self.user_select
        except ValueError:
            print("数字以外を入れるなあほ")

        except Exception:
            print("どうして" + str(sys.exc_info()))
