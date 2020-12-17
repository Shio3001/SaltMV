# coding:utf-8
import sys
import numpy as np
import os
import copy

# 中間点などから情報をもらってきて、それを基に現在位置を決定するやつ


class CentralRole:
    def __init__(self):
        pass

    def main(self, around_time, single_around_point, now_frame):
        #this_point_amount = int(len(this_point))
        #departure_point = 0

        old_point = single_around_point[0]
        next_point = single_around_point[1]

        old_time = around_time[0]
        next_time = around_time[1]

        distance_interval = next_point - old_point
        time_interval = next_time - old_time
        already_passed = now_frame - old_time

        position = ((distance_interval / time_interval) * already_passed) + old_point

        return position
