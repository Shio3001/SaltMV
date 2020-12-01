# coding:utf-8
import sys
import numpy as np
import os
import copy

# GUI処分ファイル(CUI中継)


class Center:
    def __init__(self):
        self.selectlist = {0: "何もないよ", 1: "終了", 2: "保存", 3: "プロジェクト設定", 4: "レイヤー生成", 5: "オブジェクト生成", 6: "中間点設定"}
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
            print("生成したいレイヤーを入力 現在" + str(all_elements.layer_group) + "コ 確認")
            operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)
            userselect_layer = operation_list["CUI"]["layerselect"]["Center"].layer(all_elements.layer_group)

            all_elements.layer_group[userselect_layer] = operation_list["CUI"]["makeobject"]["Center"].main(all_elements, elements, copy.deepcopy(
                all_elements.layer_group[userselect_layer]), operation_list, responselist, self.selectlist)
            return all_elements, responselist[1]

        if user_select == self.selectlist[6] or user_select == str(self.selectlist_keys[6]):  # 中間点設定
            operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)
            userselect_layer = operation_list["CUI"]["layerselect"]["Center"].layer(all_elements.layer_group)
            if len(all_elements.layer_group) == 0:
                return hold_all_elements, responselist[2]

            print("設定したいオブジェクトがあるレイヤーを選択 現在" + str(all_elements.layer_group) + "コ 確認")
            userselect_layer = operation_list["CUI"]["layerselect"]["Center"].layer(all_elements.layer_group)

        return hold_all_elements, responselist[2]
