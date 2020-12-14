# coding:utf-8
import sys
import numpy
import os
import copy


class CentralRole:
    def __init__(self):
        pass

    def edit_setting(self, thisobject_effectPoint, user_select):

        if user_select[0] in thisobject_effectPoint.keys():
            try:
                thisobject_effectPoint[user_select[0]] = user_select[1]
                print("おきかえ")
            except:
                print("そんなものないよ")
        else:
            print("keyが存在しなかったよ")

        return thisobject_effectPoint

    def several_setting(self, thisobject, operation_list, user_select, maketime):  # すでに一個以上存在してる場合

        addpoint = None
        # try:
        for i, ie in enumerate(thisobject.effects[user_select].effectPoint):
            print(i)
            print(thisobject.effects[user_select].effectPoint)
            print(thisobject.effects[user_select].effectPoint[i])
            if thisobject.effects[user_select].effectPoint[i]["time"] >= maketime:
                addpoint = copy.deepcopy(thisobject.effects[user_select].effectPoint[-1])  # 入れる予定の場所をもとに時間を検索
                print("時間検索")
                break
            # maketime以上の数を入れると取れなくなってしまうため完全に隔離した状態の時間でも対応させる必要がありそう

        if thisobject.effects[user_select].effectPoint[-1]["time"] < maketime:
            addpoint = copy.deepcopy(thisobject.effects[user_select].effectPoint[-1])

        print(addpoint)
        thisobject.effects[user_select].effectPoint.append(addpoint)  # 前のやつを複製

        del addpoint

        thisobject.effects[user_select].effectPoint[-1]["time"] = maketime
        # except:
        #    print("一つも存在しない可能性あり")
        #    print("返却" + str(sys.exc_info()))
        # thisobject = operation_list["set"]["input_point"]["CentralRole"].several_setting(thisobject, operation_list, user_select, maketime)
        return thisobject

    def Initial_setting(self, thislayer, elements, userselect_time):  # 全くなかったり、オブジェクト生成時だったりする場合

        thislayer.retention_object.append(elements.ObjectElements())
        thisobject = thislayer.retention_object[-1]
        thisobject.staend_property = userselect_time  # 開始時間、終了時間を挿入

        print(thisobject.staend_property)
        print(type(thisobject.staend_property))

        thislayer.retention_object[-1] = thisobject

        del thisobject

        return thislayer

    def effect_Initial_setting(self, thislayer, operation_list, elements, effect_name):
        thisobject = thislayer.retention_object[-1]

        if not effect_name in operation_list["plugin"]["effect"]:
            print("存在なし")
            return thislayer

        thisobject.effects.append(operation_list["plugin"]["effect"][str(effect_name)].InitialValue().main(elements))

        thislayer.retention_object[-1] = thisobject

        return thislayer
