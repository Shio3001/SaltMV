# coding:utf-8
import sys
import numpy as np
import os
import copy

# GUI処分ファイル(CUI中継)


class Center:
    def __init__(self):
        self.selectlist = {0: "何もないよ", 1: "終了", 2: "保存", 3: "プロジェクト設定", 4: "レイヤー生成", 5: "オブジェクト生成"}
        self.selectlist_keys = list(self.selectlist.keys())

    def usernextselect(self, responselist, all_elements, elements, operation_list):
        print("次の動作を入力 [ 番号 ] もしくは [ 文字列 ]")

        hold_all_elements = copy.deepcopy(all_elements)  # 問題があった時にはこれを返すようにすればいい

        print(self.selectlist)

        user_select = str(sys.stdin.readline().rstrip())

        if user_select == self.selectlist[0] or user_select == str(self.selectlist_keys[0]):
            return all_elements, responselist[1]

        if user_select == self.selectlist[1] or user_select == str(self.selectlist_keys[1]):  # 終了
            return all_elements, responselist[0]

        if user_select == self.selectlist[2] or user_select == str(self.selectlist_keys[2]):  # 保存
            return all_elements, responselist[1]

        if user_select == self.selectlist[3] or user_select == str(self.selectlist_keys[3]):  # 画面サイズなどを設定
            print(operation_list)
            all_elements.editor_info = operation_list["CUI"]["seteditsize"]["Center"].main()

            return all_elements, responselist[1]

        if user_select == self.selectlist[4] or user_select == str(self.selectlist_keys[4]):  # レイヤー生成
            print("レイヤー生成")
            all_elements.layer_group.append(elements.layerElements())
            operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)
            return all_elements, responselist[1]

        if user_select == self.selectlist[5] or user_select == str(self.selectlist_keys[5]):  # オブジェクト生成
            if len(all_elements.layer_group) == 0:
                return hold_all_elements, responselist[2]
            print("生成したいレイヤーを入力")
            userselect_layer = operation_list["CUI"]["layerselect"]["Center"].layer(all_elements.layer_group)

            thislayer = copy.deepcopy(all_elements.layer_group[userselect_layer])  # 今回使うのはこちら!

            userselect_time = [0, 0]
            print("開始する時間を入力")
            userselect_time[0] = operation_list["CUI"]["timeselect"]["Center"].main(all_elements)

            print("終了する時間を入力")
            userselect_time[1] = operation_list["CUI"]["timeselect"]["Center"].main(all_elements)

            userselect_time.sort()
            # 次のオブジェクトの開始地点と、今のオブジェクトの終了地点を引いて、0以下であればかぶっている判定にしてあげれば勝ち

            thislayer.retention_object.append(elements.ObjectElements())

            thislayer_reobj_now = int(len(thislayer.retention_object)) - 1

            thislayer.retention_object[thislayer_reobj_now].staend_property = userselect_time

            thislayer.retention_object = sorted(thislayer.retention_object, key=lambda x: x.staend_property[0], reverse=False)

            all_elements.layer_group[userselect_layer] = thislayer  # あとで職員が美味しくいただきました(返却)

            operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)

            del thislayer
            return all_elements, responselist[1]

        return hold_all_elements, responselist[2]
