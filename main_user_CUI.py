# coding:utf-8
import sys
import numpy as np
import os
import copy

# GUI処分ファイル(CUI中継)


class Center:
    def __init__(self):

        # self.selectlist = {0, "何もないよ", 1: "終了", 2: "保存", 3: "プロジェクト設定", 4: "レイヤー生成", 5: "オブジェクト生成", 6: "中間点設定", 7: "設定書き出し"}

        self.selectlist = np.array([["0", "何もないよ", self.nothing],
                                    ["1", "終了", self.exit],
                                    ["2", "保存", self.save],
                                    ["3", "取得", self.load],
                                    ["4", "プロジェクト設定", self.set_edit],
                                    ["5", "レイヤー生成", self.newlayer],
                                    ["6", "オブジェクト生成", self.newobject],
                                    ["7", "中間点生成", self.newpoint],
                                    ["8", "設定表示", self.printall]])

    def usernextselect(self, responselist, all_elements, elements, operation_list):

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("次の動作を入力 [ 番号 ] もしくは [ 文字列 ]")
        print(self.selectlist)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        user_select = str(sys.stdin.readline().rstrip())

        use_index = np.where(self.selectlist == user_select)
        try:
            all_elements, responselist = self.selectlist[use_index[0][0]][2](responselist, all_elements, elements, operation_list)
            # 連想配列もどきの取得部分↑
            return all_elements, responselist
        except:
            return all_elements, responselist[2]

    def nothing(self, responselist, all_elements, elements, operation_list):  # 0
        return all_elements, responselist[1]

    def exit(self, responselist, all_elements, elements, operation_list):  # 0
        return all_elements, responselist[0]

    def save(self, responselist, all_elements, elements, operation_list):  # 0
        print("保存先を入力")
        user_select = str(sys.stdin.readline().rstrip())

        operation_list["save"]["make_save"]["Center"].output(all_elements, user_select)

        return all_elements, responselist[1]

    def load(self, responselist, all_elements, elements, operation_list):  # 0
        return all_elements, responselist[1]

    def set_edit(self, responselist, all_elements, elements, operation_list):  # 0
        print(operation_list)
        all_elements.editor_info = operation_list["CUI"]["seteditsize"]["Center"].main()

        return all_elements, responselist[1]

    def newlayer(self, responselist, all_elements, elements, operation_list):  # 0
        print("レイヤー生成")
        all_elements.layer_group.append(elements.layerElements())
        operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)
        return all_elements, responselist[1]

    def newobject(self, responselist, all_elements, elements, operation_list):  # 0
        hold_all_elements = copy.deepcopy(all_elements)  # 問題があった時にはこれを返すようにすればいい
        if len(all_elements.layer_group) == 0:
            return hold_all_elements, responselist[2]
        print("生成したいレイヤーを入力 現在" + str(len(all_elements.layer_group)) + "コ 確認")
        operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)
        userselect_layer = operation_list["CUI"]["layerselect"]["Center"].layer(all_elements.layer_group)

        all_elements.layer_group[userselect_layer] = operation_list["CUI"]["makeobject"]["Center"].main(all_elements, elements, copy.deepcopy(
            all_elements.layer_group[userselect_layer]), operation_list, responselist)
        return all_elements, responselist[1]

    def newpoint(self, responselist, all_elements, elements, operation_list):  # 0

        hold_all_elements = copy.deepcopy(all_elements)  # 問題があった時にはこれを返すようにすればいい
        operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)
        if len(all_elements.layer_group) == 0:  # レイヤーがないなら帰れ
            return hold_all_elements, responselist[2]

        print("設定したいオブジェクトがあるレイヤーを選択 現在" + str(len(all_elements.layer_group)) + "コ 確認")
        userselect_layer = operation_list["CUI"]["layerselect"]["Center"].layer(all_elements.layer_group)

        if len(all_elements.layer_group[userselect_layer].retention_object) == 0:  # ０オブジェクトがないなら帰れ
            print("オブジェクトが存在しません")
            return hold_all_elements, responselist[2]

        print("設定したいオブジェクトを選択 現在" + str(len(all_elements.layer_group[userselect_layer].retention_object)) + "コ 確認")
        userselect_object = operation_list["CUI"]["layerselect"]["Center"].object(all_elements.layer_group[userselect_layer].retention_object)

        all_elements.layer_group[userselect_layer] = operation_list["CUI"]["usersetpoint"]["Center"].main(copy.deepcopy(all_elements.layer_group[userselect_layer]),  all_elements, operation_list, userselect_object)
        return all_elements, responselist[1]

    def printall(self, responselist, all_elements, elements, operation_list):  # 0
        userselect_layer = operation_list["CUI"]["printlayer"]["Center"].viaAll(all_elements)
        return all_elements, responselist[1]
