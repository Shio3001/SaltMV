# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def __init__(self):
        pass

    def several_setting(self, thisobject, user_select, maketime):  # すでに一個以上存在してる場合
        thisobject.effects[user_select].effectPoint.append(thisobject.effects[user_select].effectPoint[-1])  # 前のやつを複製

        thisobject.effects[user_select].effectPoint[-1]["time"] = maketime
        return thisobject

    def Initial_setting(self, thisobject, elements, maketime):  # 全くなかったり、オブジェクト生成時だったりする場合

        thisobject.effects.append(elements.effectElements())
        thisobject.effects[-1].effectPoint.append()
        thisobject.effects[-1].effectPoint[-1]["time"] = maketime

        return thisobject

        # thislayer.retention_object[thislayer_reobj_now].effects.append(elements.effectElements())
        #thislayer.retention_object[thislayer_reobj_now].effects.Point[-1]["time"] = settime

        # return thislayer
