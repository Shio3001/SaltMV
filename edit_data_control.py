import elements
import copy
import json
import pickle
import base64
import os

edit_data = elements.AllElements()
# edit_data.now_scene = 0  # 現在の操作シーン


class Storage:
    def __init__(self, main_path):
        self.app_name = "NankokuMovieMaker"
        self.extension = ".json"

        self.operation = None

        self.elements = elements

        self.os_type = ""

        self.main_path = main_path

        self.fill_input_callback = None
        self.fill_output_callback = None

        this_os = str(os.name)  # windowsか判定
        if this_os == "nt":
            self.slash = "\\"
            self.os_type = "w"
        else:
            self.slash = "/"
            self.os_type = "ml"

        self.font_data = {}
        self.font_name = {}
        self.read_font()

        new_scene = self.add_scene_elements()
        edit_data.now_scene = new_scene.scene_id

        print("now_key:", edit_data.now_scene)

    def input_debug(self, message=None):
        print("{0} 入力してください".format(message))

        in_data = str(input())

        return in_data

    def get_font_path(self):

        font_path = {}

        if self.os_type == "ml":
            font_path["system"] = "/System/Library/Fonts"
            font_path["library"] = "/Library/Fonts"
            font_path["user"] = os.path.join("/Users", self.get_user(), "Library/Fonts")
        # "/System/Library/Fonts"
        # /Library/Fonts
        # /Users/maruyama/Library/Fonts
        return font_path

    def read_font(self):
        font_path = self.get_font_path()

        if self.os_type == "ml":
            for k, kv in zip(font_path.keys(), font_path.values()):
                font_file_name = os.listdir(kv)

                print("{0}ファイル量 : {1}".format(k, len(font_file_name)))

                for f in font_file_name:
                    print(f)

                    path = os.path.relpath(kv, self.main_path)
                    self.font_data[f] = os.path.join(path, f)

                    f_k = f[: -4]
                    self.font_name[f_k] = f

        print(self.font_data)
        print(self.font_name)

    def get_user(self):
        return os.environ.get("USER")

    def set_operation(self, send_operation):
        self.operation = send_operation

    def get(self):
        return copy.deepcopy(edit_data)

    def set(self, send):
        edit_data = copy.deepcopy(send)
        return

    def scene(self, data=None):
        # self.operation["log"].write("scene")

        if not data is None:
            edit_data.scenes[edit_data.now_scene] = copy.deepcopy(data)
            return
        return copy.deepcopy(edit_data.scenes[edit_data.now_scene])

    def layer(self, layer_order, data=None):
        # self.operation["log"].write("layer")

        if not data is None:
            edit_data.scenes[edit_data.now_scene].layer_group[layer_order] = copy.deepcopy(data)
            return

        return copy.deepcopy(self.scene().layer_group[layer_order])

    def media_object(self, layer_order, object_order, data=None):
        # self.operation["log"].write("object")

        if not data is None:
            print("ids :", edit_data.now_scene, layer_order, object_order)

            edit_data.scenes[edit_data.now_scene].layer_group[layer_order].object_group[object_order] = copy.deepcopy(data)

            print("受信しました", data.installation)
            return
        return copy.deepcopy(self.layer(layer_order).object_group[object_order])

    def effect(self, layer_order, object_order, effect_order, data=None):
        # self.operation["log"].write("effect")

        if not data is None:
            edit_data.scenes[edit_data.now_scene].layer_group[layer_order].object_group[object_order].effect_group[effect_order] = copy.deepcopy(data)
            return

        return copy.deepcopy(self.object(layer_order, object_order).effect_group[effect_order])

    def add_scene_elements(self):
        new_scene = elements.SceneElements()
        edit_data.scenes[new_scene.scene_id] = new_scene

        print("key:", new_scene.scene_id)

        return copy.deepcopy(edit_data.scenes[new_scene.scene_id])

    def add_layer_elements(self):
        new_layer = elements.LayerElements()
        edit_data.scenes[edit_data.now_scene].layer_group[new_layer.layer_id] = new_layer
        # print(edit_data.scenes[edit_data.now_scene].layer_group)

        return copy.deepcopy(self.scene().layer_group[new_layer.layer_id])

    def add_object_elements(self, layer_order):

        new_obj = elements.ObjectElements()
        edit_data.scenes[edit_data.now_scene].layer_group[layer_order].object_group[new_obj.obj_id] = new_obj

        return copy.deepcopy(self.layer(layer_order).object_group[new_obj.obj_id])

    def add_effect_elements(self, layer_order, object_order):

        new_effect = elements.EffectElements()
        edit_data.scenes[edit_data.now_scene].layer_group[layer_order].object_group[object_order].effect_group[new_effect.effect_id] = new_effect

        return copy.deepcopy(self.object(layer_order, object_order).effect_group[new_effect.effect_id])

    def del_scene_elements(self, scene_order):
        del edit_data.scenes[scene_order]

    def del_layer_elements(self, layer_order):
        del edit_data.scenes[edit_data.now_scene].layer_group[layer_order]

    def del_object_elements(self, layer_order, object_order):
        del edit_data.scenes[edit_data.now_scene].layer_group[layer_order].object_group[object_order]

    def del_effect_elements(self, layer_order, object_order, effect_order):
        del edit_data.scenes[edit_data.now_scene].layer_group[layer_order].object_group[object_order].effect_group[effect_order]

    def file_input(self, user_select):

        user_select = self.extension_detection(user_select)

        try:
            lordfile = open(user_select, 'rb')
            edit_data = pickle.load(lordfile)
            save_path = copy.deepcopy(user_select)

            self.operation["log"].write("編集ファイルを開きました ファイルパス{0}".format(save_path))

            if not str(type(self.fill_input_callback)) == "<class 'function'>":
                return

            print("input実行")
            self.fill_input_callback()

        except:
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

        if not str(type(self.fill_output_callback)) == "<class 'function'>":
            return
        self.fill_output_callback()

        return save_location

    def extension_detection(self, file_name):  # 拡張子変更
        extension_len = int(len(self.extension)) * -1
        if file_name[extension_len:] != self.extension:
            file_name += self.extension

        return file_name
