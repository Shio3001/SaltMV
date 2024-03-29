from pysrc import elements
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
import datetime


class EasingData:
    def __init__(self, gx, gy, rx, ry):
        self.gx = gx
        self.gy = gy
        self.rx = rx
        self.ry = ry


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
        #self.now_time = 0
        #self.threading = threading
        #self.threading_lock = threading.Lock()
        #self.ThreadPoolExecutor = ThreadPoolExecutor
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

        self.callback_operation = None

        #self.now_time = 0

    def now_time_update(self, scroll_data=None):
        if scroll_data is None:
            return self.edit_data.scenes[self.edit_data.now_scene].now_time

        self.edit_data.scenes[self.edit_data.now_scene].now_time = copy.deepcopy(scroll_data.ratio_f[0])

        # print()
        print("現在時刻変更",  self.edit_data.scenes[self.edit_data.now_scene].now_time)

        self.callback_operation.event("preview", info=(self.get_now_time(), False))

    def get_now_time(self):
        return self.edit_data.scenes[self.edit_data.now_scene].now_time

    def change_now_scene(self, scene_name):
        ##print("現在シーン切り替え", self.edit_data.now_scene, " → ", scene_name)
        if scene_name in self.edit_data.scenes.keys():
            self.edit_data.now_scene = copy.deepcopy(scene_name)

    def get_scene_name_list(self):
        return list(self.edit_data.scenes.keys())

    def new_edit_data(self):
        self.edit_data = elements.AllElements()
        new_scene = self.add_scene_elements()
        self.edit_data.now_scene = new_scene.scene_id

    def input_debug(self, message=None):
        #print("{0} 入力してください".format(message))

        in_data = str(input())

        return in_data

    def layer_number_to_layer_id(self, layer_number):
        layer_layer_id = self.edit_data.scenes[self.edit_data.now_scene].layer_group.layer_layer_id
        # #print(layer_data.items())

        for k, v in layer_layer_id.items():
            if v == layer_number:
                return k

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

    def scene_id(self):
        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].scene_id)

    def scene_editor(self):
        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].editor)

    def scene(self, data=None, scene_id=None):
        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene] = copy.deepcopy(data)
            return
        if not scene_id is None:
            copy.deepcopy(self.edit_data.scenes[scene_id])

        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene])

    def layer(self, data=None):
        # self.operation["log"].write("layer")

        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group = copy.deepcopy(data)
            return

        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group)

    def media_object_group(self, data=None):
        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group = copy.deepcopy(data)
            return

        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group)

    def media_object(self, object_order, data=None):
        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0] = copy.deepcopy(data)
            return

        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0])

    def media_object_had_layer(self, object_order, data=None):  # stack対象
        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order] = copy.deepcopy(data)
            return

        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order])

    def effect(self, object_order, effect_order, data=None):
        if not data is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group[effect_order] = copy.deepcopy(data)
            return

        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group[effect_order])

    def get_bool_editor_select_file(self, name):
        return name in self.edit_data.scenes[self.edit_data.now_scene].editor_select_file

    def get_bool_editor_select_folder(self, name):
        return name in self.edit_data.scenes[self.edit_data.now_scene].editor_select_folder

    def get_set_scene_edior(self, editor=None, name=None, data=None):
        if not name is None and not data is None:

            if name in self.edit_data.scenes[self.edit_data.now_scene].editor_select_int:
                data = int(data)

            self.edit_data.scenes[self.edit_data.now_scene].editor[name] = data
            return

        if not editor is None and type(self.edit_data.scenes[self.edit_data.now_scene].editor) == type(editor):
            self.edit_data.scenes[self.edit_data.now_scene].editor = editor

        return self.edit_data.scenes[self.edit_data.now_scene].editor

    def add_scene_elements(self, new_scene_name=None):
        new_scene = elements.SceneElements()
        if not new_scene_name is None:
            new_scene.scene_id = str(new_scene_name)
        self.edit_data.scenes[new_scene.scene_id] = new_scene

        ##print("key:", new_scene.scene_id)

        return copy.deepcopy(self.edit_data.scenes[new_scene.scene_id])

    def add_layer_elements(self):
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.layer_layer_id[elements.make_id("layer")] = self.get_layer_length()

        return copy.deepcopy(self.scene().layer_group)

    def copy_object_elements(self, copy_target_id, sta=None, end=None):
        new_copy_obj = copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[copy_target_id][0])
        target_layer_id = copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[copy_target_id][1])
        new_copy_obj.effect_point_internal_id_time = {}
        new_copy_obj.obj_id = elements.make_id("obj_copy_{0}".format(new_copy_obj.obj_id))

        now_time = datetime.datetime.now()

        old_effect_group = copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[copy_target_id][0].effect_group)
        new_copy_obj.effect_group = {}

        for oev in old_effect_group.values():
            now_t = now_time.strftime('%y%m%H%M%S%f')
            oev.effect_id += "_copy{0}".format(now_t)
            new_copy_obj.effect_group[oev.effect_id] = oev

        del old_effect_group

        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id] = [None, None]
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id][0] = new_copy_obj
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id][1] = target_layer_id
        self.callback_operation.event("add_object_elements", info=())

        if not sta is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id][0].installation[0] = copy.deepcopy(sta)
        if not end is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id][0].installation[1] = copy.deepcopy(end)

        time = self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_copy_obj.obj_id][0].installation

        self.add_key_frame_point_onely(time[0], new_copy_obj.obj_id, "default_sta")
        self.add_key_frame_point_onely(time[1], new_copy_obj.obj_id, "default_end")

        return copy.deepcopy(self.layer().object_group[new_copy_obj.obj_id][0]), target_layer_id

    def add_object_elements(self, layer_number=0):
        new_obj = elements.ObjectElements()
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_obj.obj_id] = [None, None]
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_obj.obj_id][0] = new_obj
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_obj.obj_id][1] = self.layer_number_to_layer_id(layer_number)
        self.callback_operation.event("add_object_elements", info=())

        time = self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[new_obj.obj_id][0].installation
        self.add_key_frame_point_onely(time[0], new_obj.obj_id, "default_sta")
        self.add_key_frame_point_onely(time[1], new_obj.obj_id, "default_end")

        return copy.deepcopy(self.layer().object_group[new_obj.obj_id][0])

    def edit_object_installation(self, media_id, sta, end):
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[media_id][0].installation = copy.deepcopy([sta, end])

    def edit_effect_synthetic(self, object_order, synthetic):
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].synthetic = synthetic

    def add_effect_elements(self, object_order, effect_name):
        new_effect = elements.EffectElements()
        new_effect.effect_name = effect_name

        self.operation["plugin"]["effect"][effect_name].InitialValue(new_effect)

        new_effect.effect_id = self.elements.make_id("effect")

        if new_effect.effect_id is None:
            new_effect.effect_name = effect_name

        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group[new_effect.effect_id] = new_effect
        e = self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group[new_effect.effect_id]

        # for e in self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_group.values():
        for ek in self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[object_order][0].effect_point_internal_id_time.keys():
            e.effect_point_internal_id_point[ek] = copy.deepcopy(e.effect_point)

        for ei in new_effect.effect_point.keys():
            self.edit_easing(object_order, new_effect.effect_id, ei, 0, 0, 100, 100)
            self.set_get_accompany(object_order, new_effect.effect_id, ei, "not")

        return copy.deepcopy(self.media_object(object_order).effect_group[new_effect.effect_id])

    def add_key_frame(self, time, obj_id, key_frame_id, overwrite=True):
        self.add_key_frame_point_onely(time, obj_id, key_frame_id, overwrite)
        self.add_key_frame_inside_data(obj_id, key_frame_id, overwrite)

    def add_key_frame_point_onely(self, time, obj_id, key_frame_id, overwrite=True):
        print("add_key_frame_point_onely1", self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time)
        overwrite_bool = key_frame_id in list(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time.keys())
        if overwrite_bool and not overwrite:
            print("add_key_frame_point_onely 返却")
            return
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time[key_frame_id] = copy.deepcopy(time)
        print("add_key_frame_point_onely2", self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time)

    def add_key_frame_inside_data(self, obj_id, key_frame_id, overwrite=True):
        effect_group = self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group
        if len(effect_group) == 0:
            return

        for eg in effect_group.values():
            new_effect = copy.deepcopy(eg.effect_point)

            print("eg.effect_point_internal_id_point1", eg.effect_point_internal_id_point)

            overwrite_bool = key_frame_id in list(eg.effect_point_internal_id_point.keys())
            if overwrite_bool and not overwrite:
                print("add_key_frame_inside_data 返却")
                return
            eg.effect_point_internal_id_point[key_frame_id] = new_effect

            print("eg.effect_point_internal_id_point2", eg.effect_point_internal_id_point)

    def del_key_frame_point(self, obj_id, key_frame_id):
        print("del_key_frame_point1", self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time)

        del self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time[key_frame_id]

        print("del_key_frame_point2", self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time)

    def layer_id_set(self, obj_id, new_layer_id):
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][1] = copy.deepcopy(new_layer_id)

    def move_key_frame(self, time, obj_id, key_frame_id):
        if not key_frame_id in self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time.keys():
            self.operation["error"].action("そんなのないですよ {0}".format(key_frame_id))
        #typeA = type(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time[key_frame_id])
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time[key_frame_id] = time
        #typeB = type(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time[key_frame_id])
        # if typeA != typeB:
        #    self.operation["error"].action("方が変更されています {0} -> {1}".format(typeA, typeB))

    def edit_key_frame_val(self, obj_id, effect_id, key_frame_id, mov_key, mov_val):
        if not key_frame_id in self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time.keys():
            self.operation["error"].action("そんなのないですよ {0}".format(key_frame_id))
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].effect_point_internal_id_point[key_frame_id][mov_key] = mov_val

    def edit_easing(self, obj_id, effect_id, mov_key, gx, gy, rx, ry):
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].easing_number[mov_key] = EasingData(gx, gy, rx, ry)

    def get_easing(self, obj_id, effect_id, mov_key):
        return self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].easing_number[mov_key]

    def set_get_accompany(self, obj_id, effect_id, mov_key, target_name=None):
        if not target_name is None:
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].accompany_target[mov_key] = target_name

        return self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].accompany_target[mov_key]

    def get_key_frame(self, obj_id, data=None):
        if not data is None:
            typeA = type(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time)
            self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time = copy.deepcopy(data)
            typeB = type(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time)
            if typeA != typeB:
                self.operation["error"].action("方が変更されています {0} -> {1}".format(typeA, typeB))
            return

        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_point_internal_id_time)

    def override_key_frame_val_list(self, obj_id, effect_id, key_frame_data):
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].effect_point_internal_id_point = copy.deepcopy(key_frame_data)

    def get_key_frame_val_list(self, obj_id, effect_id):
        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].effect_point_internal_id_point)

    def get_key_frame_val(self, obj_id, effect_id, key_frame_id, mov_key):
        return copy.deepcopy(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].effect_point_internal_id_point[key_frame_id][mov_key])

    def edit_various_fixed(self, obj_id, effect_id, various_fixed_key, various_fixed_val=None):
        if various_fixed_val is None:
            print(obj_id, effect_id, various_fixed_key)
            print(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group)
            print(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group)
            return self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].various_fixed[various_fixed_key]

        if not various_fixed_key in self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].various_fixed.keys():
            self.operation["error"].action("そんなのないですよ {0}".format(various_fixed_key))
        self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].various_fixed[various_fixed_key] = copy.deepcopy(various_fixed_val)
        # #print(self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][0].effect_group[effect_id].various_fixed)

    def get_now_layer_id(self, obj_id):
        ##print("シーン番号", self.edit_data.scenes, self.edit_data.now_scene, self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group)
        layer_id = self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][1]
        return layer_id

    def get_now_layer_number(self, obj_id):
        ##print("シーン番号", self.edit_data.scenes, self.edit_data.now_scene, self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group)
        layer_id = self.edit_data.scenes[self.edit_data.now_scene].layer_group.object_group[obj_id][1]
        layer_number = self.edit_data.scenes[self.edit_data.now_scene].layer_group.layer_layer_id[layer_id]
        return layer_number

    def del_scene_elements(self, scene_order):
        del self.edit_data.scenes[scene_order]

    def del_layer_elements(self):
        del self.edit_data.scenes[self.edit_data.now_scene].layer_group

    def del_object_elements(self, object_order):
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

            print("編集ファイルを開きました ファイルパス{0}".format(save_path))

            # #print("input実行")

        except:
            print("編集ファイルが存在しませんでした")
            save_path = ""

        print("読み取り終了")

        self.callback_operation.event("preview_setup")
        self.callback_operation.event("file_input_after")

        self.callback_operation.event("cash_clear")

        return save_path

        # return all_elements, save_location

    def file_output(self, send_user_select):

        self.callback_operation.event("file_output_before")

        now_time = datetime.datetime.now()
        output_file_name = "output_" + str(now_time.strftime('%y_%m_%H_%M_%S_%f'))
        user_select = self.extension_detection(os.path.join(send_user_select, output_file_name))

        openfile = open(user_select, 'wb')
        pickle.dump(self.edit_data, openfile, protocol=5)
        openfile.close()

        save_location = copy.deepcopy(user_select)

        # if not str(type(self.fill_output_callback)) == "<class 'function'>":
        #    return
        # self.fill_output_callback()

        self.callback_operation.event("file_output_after")

        # self.data.all_data.callback_operation.event("preview_setup")

        print("書き出しました")

        return save_location

    def extension_detection(self, file_name):  # 拡張子変更
        extension_len = int(len(self.extension)) * -1
        if file_name[extension_len:] != self.extension:
            file_name += self.extension

        return file_name
