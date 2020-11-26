# coding:utf-8
import sys
import numpy
import os
import copy

# GUI処分ファイル(CUI中継)


class Center:
    def __init__(self):
        self.selectlist = {0: "わりあてなし", 1: "終了", 2: "保存", 3: "プロジェクト設定", 4: "レイヤー生成", 5: "オブジェクト生成"}
        self.selectlist_keys = list(self.selectlist.keys())

    def usernextselect(self, responselist, all_elements, elements, userCUI_rally_Center):
        print("次の動作を入力 [ 番号 ] もしくは [ 文字列 ]")

        hold_all_elements = copy.deepcopy(all_elements)  # 問題があった時にはこれを返すようにすればいい

        print(self.selectlist)

        user_select = str(sys.stdin.readline().rstrip())

        if user_select == self.selectlist[1] or user_select == str(self.selectlist_keys[1]):  # 終了
            return all_elements, responselist[0]

        if user_select == self.selectlist[2] or user_select == str(self.selectlist_keys[2]):  # 保存
            return all_elements, responselist[1]

        if user_select == self.selectlist[3] or user_select == str(self.selectlist_keys[3]):  # 画面サイズなどを設定
            all_elements.editor_info = userCUI_rally_Center.seteditsize_Center.main()

            return all_elements, responselist[1]

        if user_select == self.selectlist[4] or user_select == str(self.selectlist_keys[4]):  # レイヤー生成
            print("レイヤー生成")
            all_elements.layer_group.append(elements.layerElements())
            userCUI_rally_Center.printlayer_Center.viaAll(all_elements)
            return all_elements, responselist[1]

        if user_select == self.selectlist[5] or user_select == str(self.selectlist_keys[5]):  # オブジェクト生成
            print("生成したいレイヤーを入力")
            userselect_layer = userCUI_rally_Center.layerselect_Center.layer(all_elements.layer_group)

            print("開始する時間を入力")
            return all_elements, responselist[1]

        return hold_all_elements, responselist[2]
