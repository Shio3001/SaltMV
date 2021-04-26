import elements
import copy
import json
import pickle
import base64
import os

edit_data = elements.AllElements()
now_scene = 0  # 現在の操作シーン


class Storage:
    def __init__(self, main_path):
        self.app_name = "NankokuMovieMaker"
        self.extension = ".json"

        self.operation = None

        self.elements = elements

        self.os_type = ""

        self.main_path = main_path

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

        self.add_scene_elements()

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
        return edit_data

    def set(self, send):
        edit_data = send
        return

    def scene(self, data=None):
        # self.operation["log"].write("scene")

        if not data is None:
            edit_data.scenes[now_scene] = data
            return
        return edit_data.scenes[now_scene]

    def layer(self, layer_order, data=None):
        # self.operation["log"].write("layer")

        if not data is None:
            self.scene().layer_group[layer_order] = data
            return

        return self.scene().layer_group[layer_order]

    def media_object(self, layer_order, object_order, data=None):
        # self.operation["log"].write("object")

        if not data is None:
            self.layer(layer_order).object_group[object_order] = data
            return
        return self.layer(layer_order).object_group[object_order]

    def effect(self, layer_order, object_order, effect_order, data=None):
        # self.operation["log"].write("effect")

        if not data is None:
            self.object(layer_order, object_order).effect_group[effect_order] = data
            return

        return self.object(layer_order, object_order).effect_group[effect_order]

    def add_scene_elements(self):
        edit_data.scenes.append(elements.SceneElements())

    def add_layer_elements(self):
        edit_data.scenes[now_scene].layer_group.append(elements.LayerElements())
        print(edit_data.scenes[now_scene].layer_group)

    def add_object_elements(self, layer_order):
        edit_data.scenes[now_scene].layer_group[layer_order].object_group.append(elements.ObjectElements())

    def add_effect_elements(self, layer_order, object_order):
        edit_data.scenes[now_scene].layer_group[layer_order].object_group[object_order].effect_group.append(elements.EffectElements())

    def del_scene_elements(self, scene_order):
        del edit_data.scenes[scene_order]

    def del_layer_elements(self, layer_order):
        del edit_data.scenes[now_scene].layer_group[layer_order]

    def del_object_elements(self, layer_order, object_order):
        del edit_data.scenes[now_scene].layer_group[layer_order].object_group[object_order]

    def del_effect_elements(self, layer_order, object_order, effect_order):
        del edit_data.scenes[now_scene].layer_group[layer_order].object_group[object_order].effect_group[effect_order]

    def file_input(self, user_select):

        user_select = self.extension_detection(user_select)

        try:
            lordfile = open(user_select, 'rb')
            edit_data = pickle.load(lordfile)
            save_path = copy.deepcopy(user_select)

            self.operation["log"].write("編集ファイルを開きました ファイルパス{0}".format(save_path))

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

        return save_location

    def extension_detection(self, file_name):  # 拡張子変更
        extension_len = int(len(self.extension)) * -1
        if file_name[extension_len:] != self.extension:
            file_name += self.extension

        return file_name
