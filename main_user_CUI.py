# coding:utf-8
import sys
import numpy as np
import os
import copy


# GUI処分ファイル(CUI中継)


class CentralRole:
    def __init__(self):

        # self.selectlist = {0, "何もないよ", 1: "終了", 2: "保存", 3: "プロジェクト設定", 4: "レイヤー生成", 5: "オブジェクト生成", 6: "中間点設定", 7: "設定書き出し"}

        self.selectlist = np.array([["0", "何もないよ", self.nothing],
                                    ["1", "終了", self.exit],
                                    ["2", "保存", self.save],
                                    ["2a", "上書き保存", self.overwrite_save],
                                    ["3", "取得", self.load],
                                    ["4", "プロジェクト設定", self.set_edit],
                                    ["5", "レイヤー生成", self.newlayer],
                                    ["6", "オブジェクト生成", self.newobject],
                                    ["7", "中間点生成", self.newpoint],
                                    ["8", "設定表示", self.printall],
                                    ["9", "動画の書き出し", self.export_video],
                                    ["10", "画像の書き出し", self.export_image]])

        self.save_location = ""

    def usernextselect(self, responselist, all_elements, elements, operation_list):

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("次の動作を入力 [ 番号 ] もしくは [ 文字列 ]")
        print(self.selectlist)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        user_select = str(sys.stdin.readline().rstrip())

        use_index = np.where(self.selectlist == user_select)  # 居場所は二次元配列で返されるので
        if not use_index[0]:
            return all_elements, responselist[2]
        all_elements, responselist = self.selectlist[use_index[0][0]][2](responselist, all_elements, elements, operation_list)
        # 連想配列もどきの取得部分↑
        return all_elements, responselist

    def nothing(self, responselist, all_elements, elements, operation_list):  # 0
        return all_elements, responselist[1]

    def exit(self, responselist, all_elements, elements, operation_list):  # 0
        return all_elements, responselist[0]

    def overwrite_save(self, responselist, all_elements, elements, operation_list):  # 0

        if not self.save_location:
            print("入力なし移動")
            all_elements, response = self.save(responselist, all_elements, elements, operation_list)

        else:
            user_select = self.save_location
            all_elements, self.save_location = operation_list["save"]["make_save"]["CentralRole"].output(all_elements, elements, operation_list, user_select)
            response = responselist[1]
        return all_elements, response

    def save(self, responselist, all_elements, elements, operation_list):  # 0
        print("保存先を入力")
        user_select = str(sys.stdin.readline().rstrip())

        if not user_select:
            print("入力なし返却")
            return all_elements, responselist[2]

        all_elements, self.save_location = operation_list["save"]["make_save"]["CentralRole"].output(all_elements, elements, operation_list, user_select)

        return all_elements, responselist[1]

    def load(self, responselist, all_elements, elements, operation_list):  # 0

        print("取得するファイルを入力")
        user_select = str(sys.stdin.readline().rstrip())

        all_elements, self.save_location = operation_list["save"]["make_save"]["CentralRole"].input(all_elements, elements, operation_list, user_select)
        return all_elements, responselist[1]

    def set_edit(self, responselist, all_elements, elements, operation_list):  # 0
        print(operation_list)
        all_elements.editor_info = operation_list["CUI"]["seteditsize"]["CentralRole"].main(operation_list)

        return all_elements, responselist[1]

    def newlayer(self, responselist, all_elements, elements, operation_list):  # 0
        print("レイヤー生成")
        all_elements = operation_list["set"]["new_layer"]["CentralRole"].main(all_elements, elements)
        operation_list["CUI"]["printlayer"]["CentralRole"].viaAll(all_elements)
        return all_elements, responselist[1]

    def newobject(self, responselist, all_elements, elements, operation_list):  # 0
        hold_all_elements = copy.deepcopy(all_elements)  # 問題があった時にはこれを返すようにすればいい
        if len(all_elements.layer_group) == 0:
            return hold_all_elements, responselist[2]
        print("生成したいレイヤーを入力 現在" + str(len(all_elements.layer_group)) + "コ 確認")
        operation_list["CUI"]["printlayer"]["CentralRole"].viaAll(all_elements)
        userselect_layer = operation_list["CUI"]["layerselect"]["CentralRole"].layer(all_elements.layer_group)

        all_elements.layer_group[userselect_layer] = operation_list["CUI"]["makeobject"]["CentralRole"].main(all_elements, elements, copy.deepcopy(
            all_elements.layer_group[userselect_layer]), operation_list, responselist)
        return all_elements, responselist[1]

    def newpoint(self, responselist, all_elements, elements, operation_list):  # 0

        hold_all_elements = copy.deepcopy(all_elements)  # 問題があった時にはこれを返すようにすればいい
        operation_list["CUI"]["printlayer"]["CentralRole"].viaAll(all_elements)
        if len(all_elements.layer_group) == 0:  # レイヤーがないなら帰れ
            return hold_all_elements, responselist[2]

        print("設定したいオブジェクトがあるレイヤーを選択 現在" + str(len(all_elements.layer_group)) + "コ 確認")
        userselect_layer = operation_list["CUI"]["layerselect"]["CentralRole"].layer(all_elements.layer_group)

        if len(all_elements.layer_group[userselect_layer].retention_object) == 0:  # ０オブジェクトがないなら帰れ
            print("オブジェクトが存在しません")
            return hold_all_elements, responselist[2]

        print("設定したいオブジェクトを選択 現在" + str(len(all_elements.layer_group[userselect_layer].retention_object)) + "コ 確認")
        userselect_object = operation_list["CUI"]["layerselect"]["CentralRole"].object(all_elements.layer_group[userselect_layer].retention_object)

        all_elements.layer_group[userselect_layer] = operation_list["CUI"]["usersetpoint"]["CentralRole"].main(copy.deepcopy(all_elements.layer_group[userselect_layer]),  all_elements, operation_list, userselect_object)
        return all_elements, responselist[1]

    def printall(self, responselist, all_elements, elements, operation_list):  # 0
        userselect_layer = operation_list["CUI"]["printlayer"]["CentralRole"].viaAll(all_elements)
        return all_elements, responselist[1]

    def export_video(self, responselist, all_elements, elements, operation_list):
        print("保存先を入力")
        user_select = str(sys.stdin.readline().rstrip())
        user_select = operation_list["other"]["dircon"]["CentralRole"].main(user_select)

        operation_list["out"]["output_video_image"]["CentralRole"].type_video(copy.deepcopy(all_elements), operation_list, user_select)

        return all_elements, responselist[1]

    def export_image(self, responselist, all_elements, elements, operation_list):
        print("保存先を入力")
        user_select = str(sys.stdin.readline().rstrip())
        user_select = operation_list["other"]["dircon"]["CentralRole"].main(user_select)

        print("書き出すフレームを入力")
        select_time = operation_list["CUI"]["timeselect"]["CentralRole"].main(all_elements)
        operation_list["out"]["output_video_image"]["CentralRole"].type_image(copy.deepcopy(all_elements), operation_list, select_time, user_select)

        return all_elements, responselist[1]
