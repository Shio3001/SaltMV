# coding:utf-8
import sys
import os
import copy


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        self.time_search = self.operation["plugin"]["other"]["time_search"].TimeSearch.time_search

    def main(self):
        self.data.window_title_set("タイムライン設定")
        self.data.callback_operation = self.data.operation["plugin"]["other"]["callback"].CallBack()

        def element_lord(send):
            elements, now_f = send

            for e in elements.values():
                print(now_f, e)
                before_point, next_point = self.time_search(now_f, e)

                if next_point is None:
                    for pk_b, pv_b in zip(before_point.keys(), before_point.values()):
                        if "time" in before_point.keys() and not pk_b == "time":
                            print(pk_b, pv_b)

                else:
                    print(before_point, next_point)
                    for pk_b, pv_b, pk_n, pv_n in zip(before_point.keys(), before_point.values(), next_point.keys(), next_point.values()):
                        if "time" in before_point.keys() and not pk_b == "time":
                            print(pk_b, pv_b, pk_n, pv_n)

                    for vk, vv in zip(e.various_fixed.keys(), e.various_fixed.values()):
                        print(vk, vv)

        self.data.all_data.callback_operation.set_event("media_lord", element_lord)

        #data.element_lord = element_lord


class CentralRole:
    pass
