import elements
import copy
import json
import pickle
import base64
import os

edit_data = elements.AllElements()


class Storage:
    def __init__(self):

        self.extension = ".json"
        self.operation = None

        self.elements = elements
        self.app_name = "NankokuMovieMaker"
        self.response = ["exit", "problem", "no_problem"]  # 応答リスト

        self.now_scene = 0  # 現在の操作シーン

        this_os = str(os.name)  # windowsか判定
        if this_os == "nt":
            self.slash = "\\"
        else:
            self.slash = "/"

        self.add_scene_elements()

    def set_operation(self, send_operation):
        self.operation = send_operation

    def get(self):
        return edit_data

    def set(self, send):
        edit_data = send
        return

    def scene(self, data=None):
        self.operation["log"].write("scene")

        edit_data.number += 1

        if not data is None:
            edit_data.scenes[self.now_scene] = data
            return
        return edit_data.scenes[self.now_scene]

    def layer(self, layer_order, data=None):
        self.operation["log"].write("layer")

        if not data is None:
            self.scene().layer_group[layer_order] = data
            return

        return self.scene().layer_group[layer_order]

    def object(self, layer_order, object_order, data=None):
        self.operation["log"].write("object")

        if not data is None:
            self.layer(layer_order).object_group[object_order] = data
            return
        return self.layer(layer_order).object_group[object_order]

    def effect(self, layer_order, object_order, effect_order, data=None):
        self.operation["log"].write("effect")

        if not data is None:
            self.object(layer_order, object_order).effect_group[effect_order] = data
            return

        return self.object(layer_order, object_order).effect_group[effect_order]

    def add_scene_elements(self):
        edit_data.scenes.append(elements.SceneElements())

    def add_layer_elements(self):
        edit_data.scenes[self.now_scene].layer_group.append(elements.SceneElements())

    def add_object_elements(self, layer_order):
        edit_data.scenes[self.now_scene].layer_group[layer_order].object_group.append(elements.LayerElements())

    def add_effect_elements(self, layer_order, object_order):
        edit_data.scenes[self.now_scene].layer_group[layer_order].object_group[object_order].effect_group.append(elements.ObjectElements())

    def del_scene_elements(self, scene_order):
        del edit_data.scenes[scene_order]

    def del_layer_elements(self, layer_order):
        del edit_data.scenes[self.now_scene].layer_group[layer_order]

    def del_object_elements(self, layer_order, object_order):
        del edit_data.scenes[self.now_scene].layer_group[layer_order].object_group[object_order]

    def del_effect_elements(self, layer_order, object_order, effect_order):
        del edit_data.scenes[self.now_scene].layer_group[layer_order].object_group[object_order].effect_group[effect_order]

    def file_input(self, user_select, file_name):

        file_name = self.extension_detection(file_name)

        try:
            lordfile = open(file_name, 'rb')
            edit_data = pickle.load(lordfile)
            save_path = copy.deepcopy(file_name)

            self.operation["log"].write("編集ファイルを開きました ファイルパス{0}".format(save_path))

        except:
            # print("ファイルが存在しませんでした")
            self.operation["log"].write("編集ファイルが存在しませんでした")
            save_path = ""

        return save_path

        # return all_elements, save_location

    def file_output(self, user_select):

        user_select = self.extension_detection(user_select)

        openfile = open(user_select, 'wb')
        pickle.dump(edit_data, openfile, protocol=5)
        openfile.close()

        save_location = copy.deepcopy(user_select)

        return save_location

    def extension_detection(self, file_name):  # 拡張子変更
        extension_len = int(len(self.extension)) * -1
        if file_name[extension_len:] != self.extension:
            file_name += self.extension

        return file_name
