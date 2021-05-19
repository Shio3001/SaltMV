import elements
import copy
import json
import pickle
import base64
import os

import inspect
import asyncio
# self.edit_data.now_scene = 0  # 現在の操作シーン
import threading
from concurrent.futures.thread import ThreadPoolExecutor


class Storage:
    def __init__(self, main_path):
        self.edit_data = None
        self.new_edit_data()
        self.app_name = "NankokuMovieMaker"
        self.extension = ".json"

        self.operation = None

        self.elements = elements

        self.os_type = ""

        self.main_path = main_path

        self.now_time = 0
        self.threading = threading
        self.threading_lock = threading.Lock()
        self.ThreadPoolExecutor = ThreadPoolExecutor
        #self.asyncio = asyncio

        #self.fill_input_callback = None
        #self.fill_output_callback = None

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

        self.callback_operation = None

        #print("now_key:", self.edit_data.now_scene)

    # def __self.edit_data_set(self, new_self.edit_data):
    #    self.edit_data = copy.deepcopy(new_self.edit_data)

    def new_edit_data(self):
        self.edit_data = elements.AllElements()
        new_scene = self.add_scene_elements()
        self.edit_data.now_scene = new_scene.scene_id

    def input_debug(self, message=None):
        #print("{0} 入力してください".format(message))

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

                #print("{0}ファイル量 : {1}".format(k, len(font_file_name)))

                for f in font_file_name:
                    # print(f)

                    path = os.path.relpath(kv, self.main_path)
                    self.font_data[f] = os.path.join(path, f)

                    f_k = f[: -4]
                    self.font_name[f_k] = f

        # print(self.font_data)
        # print(self.font_name)

    def layer_number_to_layer_id(self, layer_number):
        layer_data = self.edit_data.scenes[self.edit_data.now_scene].layer_group.layer_layer_id
        # print(layer_data.items())
        layer_id = [k for k, v in layer_data.items() if v == layer_number]
        # print(layer_id)
        return copy.deepcopy(layer_id[0])

    def layer_id_to_layer_number(self, layer_id):
        layer_number = self.edit_data.scenes[self.edit_data.now_scene].layer_group.layer_layer_id[layer_id]
        return copy.deepcopy(layer_number)

    def get_user(self):
        return os.environ.get("USER")

    def set_operation(self, send_operation):
        self.operation = send_operation
        self.callback_operation = self.operation["plugin"]["other"]["callback"].CallBack()

    def get(self):
        return copy.deepcopy(self.edit_data)

    def set(self, send):
        self.edit_data = copy.deepcopy(send)
        return

    def scene(self, data=None):
        # self.operation["log"].write("scene")

        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene] = copy.deepcopy(data)
            return
        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene])

    def layer(self, data=None):
        # self.operation["log"].write("layer")

        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group = copy.deepcopy(data)
            return

        ##print("オブジェクト数", len(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[0]))

        return copy.deepcopy(self.scene().layer_group)

    def media_object(self, object_order, data=None):
        #print("inspect", inspect.stack()[1].function)
        # self.operation["log"].write("object")

        if not data is None:
            #print("ids :", self.edit_data.now_scene, object_order)

            # print(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group)
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0] = copy.deepcopy(data)

            #print("受信しました", data.installation)
            return
        #print("oorder", object_order)
        return copy.deepcopy(self.layer().object_group[object_order][0])

    def effect(self, object_order, effect_order, data=None):
        # self.operation["log"].write("effect")

        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group[effect_order] = copy.deepcopy(data)
            return

        return copy.deepcopy(self.object(object_order).effect_group[effect_order])

    def add_scene_elements(self):
        new_scene = elements.SceneElements()
        self.edit_data.scenes[new_scene.scene_id] = new_scene

        #print("key:", new_scene.scene_id)

        return copy.deepcopy(self.edit_data.scenes[new_scene.scene_id])

    def add_layer_elements(self):
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.layer_layer_id[elements.make_id("layer")] = self.get_layer_length()

        return copy.deepcopy(self.scene().layer_group)

    def copy_object_elements(self, copy_target_id, sta=None, end=None):
        new_copy_obj = copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[copy_target_id][0])
        target_layer_id = copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[copy_target_id][1])

        if not sta is None:
            new_copy_obj.installation[0] = sta
        if not end is None:
            new_copy_obj.installation[1] = end

        new_copy_obj.obj_id = elements.make_id("obj_copy")
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id] = [None, None]
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id][0] = new_copy_obj
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id][1] = target_layer_id
        self.callback_operation.event("add_object_elements", info=())
        return copy.deepcopy(self.layer().object_group[new_copy_obj.obj_id][0]), target_layer_id

    def add_object_elements(self):
        new_obj = elements.ObjectElements()
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_obj.obj_id] = [None, None]
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_obj.obj_id][0] = new_obj
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_obj.obj_id][1] = self.layer_number_to_layer_id(0)
        self.callback_operation.event("add_object_elements", info=())
        return copy.deepcopy(self.layer().object_group[new_obj.obj_id][0])

    def add_effect_elements(self, object_order, effect_name):

        new_effect = elements.EffectElements()
        new_effect.effect_name = effect_name
        self.operation["plugin"]["effect"][effect_name].InitialValue(new_effect)
        new_effect.effect_id = self.elements.make_id("effect")

        if new_effect.effect_id is None:
            new_effect.effect_name = effect_name

        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group[new_effect.effect_id] = new_effect

        print(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group)

        return copy.deepcopy(self.media_object(object_order).effect_group[new_effect.effect_id])

    def get_now_layer_number(self, obj_id):
        #print("シーン番号", self.edit_data.scenes, self.edit_data.now_scene, self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group)
        layer_id = self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][1]
        layer_number = self.edit_data.scenes[self.edit_data.now_scene].layer_group.layer_layer_id[layer_id]
        return layer_number

    def del_scene_elements(self, scene_order):
        del self.edit_data.scenes[scene_order]

    def del_layer_elements(self):
        del self.edit_data.scenes[self.edit_data.now_scene].layer_group

    def del_object_elements(self, object_order):
        #self.callback_operation.event("del_layer_elements", info=(object_order))
        del self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order]

    def del_effect_elements(self, object_order, effect_order):
        del self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group[effect_order]

    def get_layer_length(self):
        leyer_length = len(self.edit_data.scenes[self.edit_data.now_scene].layer_group.layer_layer_id.keys())

        return copy.deepcopy(leyer_length)

    def file_input(self, user_select):

        self.callback_operation.event("file_input_before")

        user_select = self.extension_detection(user_select)

        try:
            lordfile = open(user_select, 'rb')
            self.edit_data = pickle.load(lordfile)
            save_path = copy.deepcopy(user_select)

            self.operation["log"].write("編集ファイルを開きました ファイルパス{0}".format(save_path))

            if not str(type(self.fill_input_callback)) == "<class 'function'>":
                return

            # print("input実行")

        except:
            self.operation["log"].write("編集ファイルが存在しませんでした")
            save_path = ""

        self.callback_operation.event("file_input_after")
        return save_path

        # return all_elements, save_location

    def file_output(self, user_select):

        self.callback_operation.event("file_output_before")

        # for layer in self.edit_data.scenes[self.edit_data.now_scene].layer_group.values():
        #    #print("layer_obj len:", layer.object_group)

        user_select = self.extension_detection(user_select)

        openfile = open(user_select, 'wb')
        pickle.dump(self.edit_data, openfile, protocol=5)
        openfile.close()

        save_location = copy.deepcopy(user_select)

        # if not str(type(self.fill_output_callback)) == "<class 'function'>":
        #    return
        # self.fill_output_callback()

        self.callback_operation.event("file_output_after")

        return save_location

    def extension_detection(self, file_name):  # 拡張子変更
        extension_len = int(len(self.extension)) * -1
        if file_name[extension_len:] != self.extension:
            file_name += self.extension

        return file_name
