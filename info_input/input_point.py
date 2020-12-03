# coding:utf-8
import sys
import numpy
import os
import copy


class Center:
    def __init__(self):
        pass

    def edit_setting(self, thisobject_effectPoint, user_select):

        if user_select[1] in thisobject_effectPoint == True:
            try:
                thisobject_effectPoint[user_select[0]] = user_select[1]
            except:
                print("そんなものないよ")

        return thisobject_effectPoint

    def several_setting(self, thisobject, operation_list, user_select, maketime):  # すでに一個以上存在してる場合

        addpoint = None
        # try:
        for i, ie in enumerate(thisobject.effects[user_select].effectPoint):
            print(i)
            print(thisobject.effects[user_select].effectPoint)
            print(thisobject.effects[user_select].effectPoint[i])
            if thisobject.effects[user_select].effectPoint[i]["time"] >= maketime:
                addpoint = thisobject.effects[user_select].effectPoint[-1]  # 入れる予定の場所をもとに時間を検索
                print("時間検索")
                break
            # maketime以上の数を入れると取れなくなってしまうため完全に隔離した状態の時間でも対応させる必要がありそう

        if thisobject.effects[user_select].effectPoint[-1]["time"] < maketime:
            addpoint = thisobject.effects[user_select].effectPoint[-1]

        print(addpoint)
        thisobject.effects[user_select].effectPoint.append(addpoint)  # 前のやつを複製

        del addpoint

        thisobject.effects[user_select].effectPoint[-1]["time"] = maketime
        # except:
        #    print("一つも存在しない可能性あり")
        #    print("返却" + str(sys.exc_info()))
        # thisobject = operation_list["set"]["input_point"]["Center"].several_setting(thisobject, operation_list, user_select, maketime)
        return thisobject

    def Initial_setting(self, thislayer, elements, userselect_time):  # 全くなかったり、オブジェクト生成時だったりする場合

        thislayer.retention_object.append(elements.ObjectElements())
        thisobject = thislayer.retention_object[-1]
        thisobject.staend_property = userselect_time  # 開始時間、終了時間を挿入

        thisobject.effects.append(elements.effectElements())
        thisobject.effects[-1].effectname = "Basic"

        print(thisobject.staend_property)
        print(type(thisobject.staend_property))

        # effectPointはobjectないでの時間

        thisobject.effects[-1].effectPoint.append({"time": 0})
        thisobject.effects[-1].effectPoint[-1]["x"] = 0
        thisobject.effects[-1].effectPoint[-1]["y"] = 0
        thisobject.effects[-1].effectPoint[-1]["alpha"] = 0
        thisobject.effects[-1].effectPoint[-1]["size"] = 0

        thislayer.retention_object[-1] = thisobject

        del thisobject

        return thislayer

        # thislayer.retention_object[thislayer_reobj_now].effects.append(elements.effectElements())
        # thislayer.retention_object[thislayer_reobj_now].effects.Point[-1]["time"] = settime

        # return thislayer
