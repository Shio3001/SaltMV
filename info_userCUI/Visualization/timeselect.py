# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def __init__(self):
        pass

    def main(self):
        print("時間を入力してください")
        print("フレームでも時分秒でも可能 ただし時間分秒で入力する時には [ h ](時間) [ m ](分) [ s ](秒) [ ms ](ミリ秒をつけること)")
        print("例: 10分5秒を表したい場合 -> [ 0h10m5s ]")

        user_select = str(sys.stdin.readline().rstrip())

    def if_time(self):
        pass

    def if_flame(self):
        pass
