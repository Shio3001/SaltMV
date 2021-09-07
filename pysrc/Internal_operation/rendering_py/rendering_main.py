import time
import cv2
import numpy as np
import datetime
import copy
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import cv2

file_all_control = {}


class FileSystem:
    def __init__(self):
        self.file_storage = {}

    def confirmation(self, path):
        keys = list(self.file_storage.keys())
        bool_confirmation = path in keys
        return bool_confirmation

    def file_storage_add(self, path, file_data):
        self.file_storage[path] = file_data

    def file_storage_del(self, path):
        del self.file_storage[path]


class EffectPluginElements:
    def __init__(self, draw, effect_value, before_value, next_value, various_fixed, now_frame, b_now_time, editor, operation, installation_sta, installation_end, FileSystem):
        #self.draw = draw
        self.draw = draw.astype('uint8')
        self.effect_value = effect_value
        self.before_value = before_value
        self.various_fixed = various_fixed
        self.next_value = next_value
        self.now_frame = now_frame
        self.b_now_time = b_now_time
        self.editor = editor
        self.operation = operation
        self.draw_size = {"x": self.draw.shape[1], "y": self.draw.shape[0]}
        self.cv2 = cv2
        self.np = np

        self.file_system = FileSystem

        self.installation = [installation_sta, installation_end]

        #self.cpp_file = ""

    def area_expansion(self, old_draw, x=0, y=0):
        old_size_x = old_draw.shape[1]
        old_size_y = old_draw.shape[0]
        if x == 0:
            x = old_size_x
        if y == 0:
            y = old_size_y

        new_draw = np.zeros((y, x, 4))
        return new_draw

    def get_file_all_control(self, path):

        if not path in list(file_all_control.keys()):
            print("file_all_control *** get_file_all_control", path, "None")
            return None

        print("file_all_control *** get_file_all_control", path, file_all_control[path])
        return file_all_control[path]

    def add_file_all_control(self, path, file):

        print("file_all_control *** add_file_all_control", path, file)

        if not self.check_file_all_control(path):
            file_all_control[path] = file

    def check_file_all_control(self, path):
        print("file_all_control *** check_file_all_control", path in list(file_all_control.keys()))
        return path in list(file_all_control.keys())

    #self.py_Rendering_func = py_Rendering_func


class Rendering:
    def __init__(self):
        #self.rendering_scene_queue = {}
        self.operation = None
        self.scene_get = None
        self.media_object_group = None

    def set(self, operation, scene_get, media_object_group):
        self.operation = operation
        self.scene_get = scene_get
        self.media_object_group = media_object_group

    def make(self, scene_id, path):
        # print(self.operation["video_image"].image_add)
        make_data = SceneOutput(self.operation, self.scene_get, self.media_object_group, self.make, scene_id, path)
        return make_data


#read_time = datetime.datetime.now() - start_time


class SceneOutput:
    def __init__(self, operation, scene_get, get_set_media_object_group, make, scene_id, path):
        self.scene_get = scene_get
        self.get_set_media_object_group = get_set_media_object_group
        self.scene = self.scene_get(scene_id=scene_id)

        # print(scene_get,make,scene_id,path,self.scene)

        self.x = int(self.scene.editor["x"])
        self.y = int(self.scene.editor["y"])
        self.fps = int(self.scene.editor["fps"])
        self.frame = int(self.scene.editor["len"])
        self.preview = self.scene.editor["preview"]
        print("self.scene.editor", self.scene.editor)

        self.operation = operation

        path_extension = ".mp4"

        extension_len = int(len(path_extension)) * -1
        if path[extension_len:] != path_extension:
            path += path_extension

        self.path = path

        self.func = {}
        self.func["scene_make"] = make
        self.func["main"] = self.output_main
        self.func["frame"] = self.output_frame
        self.func["tk"] = self.output_tk
        self.func["out"] = self.output_OpenCV
        self.func["layer_number"] = self.layer_id_number
        self.func["EffectPluginElements"] = EffectPluginElements
        self.func["FileSystem"] = FileSystem()

        #self.func["plugin_run"] = plugin_run

        self.data_image_tk = [None] * self.frame
        #self.data_iamge = [None] * self.frame

        self.scene_id = copy.deepcopy(self.scene.scene_id)

        self.cpp_encode = self.operation["cppsrc"]["video_main"].VideoExecutionCenter(self.operation, self.func)
        self.cpp_encode.scene_setup(self.scene)

        self.fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)
        self.size = (self.x, self.y)
        self.writer = cv2.VideoWriter(self.path, self.fmt, self.scene.editor["fps"], self.size)  # ライター作成
        self.audio_preview_function_list = []

    def re_scene(self):
        self.scene = self.scene_get(scene_id=self.scene_id)
        self.cpp_encode.scene_setup(self.scene)

    def layer_id_number(self, layer_id):
        return self.scene.layer_group.layer_layer_id[layer_id]

    def output_main(self, sta=None, end=None):

        start_time = datetime.datetime.now()

        if sta is None:
            sta = 0
        if end is None:
            end = self.frame

        #self.data_image[sta:end] = self.cpp_encode.execution_main(-1,-1)

        end_time = datetime.datetime.now()

        repair = end_time - start_time

        print("本処理 [ python C++ ] [ boost ] {0}".format(repair))

        self.output_OpenCV(sta, end)
        # s

    def output_frame(self, frame=None):
        frame = round(frame)
        image = self.cpp_encode.execution_preview(frame)
        return image

    # def get_image(self, frame):
    #    return self.data_image[frame]

    # def image_init(self, sta, end):
    #    self.data_image[sta:end] = np.zeros((end-sta))

    def sound_init(self):
        for a in self.audio_preview_function_list:
            a[1]()

        object_group = self.cpp_encode.object_group_recovery()
        self.get_set_media_object_group(data=object_group)

    def output_tk(self, frame, tk_cash=True, run=False):
        #map(lambda x: x(frame, sta_bool=True), self.audio_preview_function_list)

        # <class 'NoneType'>

        #type(self.data_image_tk[frame]) is NoneType

        cash_process_flag = False

        frame = round(frame)
        if type(self.data_image_tk[frame]) is None and tk_cash:
            print("キャッシュ生成済み")
            cash_process_flag = True

        image = None

        if not cash_process_flag:
            image = self.cpp_encode.execution_preview(frame)

            self.audio_preview_function_list = self.cpp_encode.get_audio_function_list()

        print(self.audio_preview_function_list, run)

        object_group = self.cpp_encode.object_group_recovery()
        self.get_set_media_object_group(data=object_group)

        if run:
            for a in self.audio_preview_function_list:
                a[0](frame, sta_bool=True)

        if self.preview == "opencv":
            #resize_size_opencv = (640, 360)
            #img_resize_opencv = image.resize(resize_size_opencv)
            self.data_image_tk[frame] = image.astype('uint8')
            return

        if cash_process_flag:
            return

        image_cvt = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGBA2RGB)

        #cv2.imwrite('wiwi.jpg', image.astype('uint8'))

        image_pil = Image.fromarray(image_cvt)
        resize_size = (640, 360)
        img_resize = image_pil.resize(resize_size)
        # self.image_tk_PhotoImage =
        # img_resize.show()

        self.data_image_tk[frame] = ImageTk.PhotoImage(img_resize)  # ImageTkフォーマットへ変換
        #self.data_image_tk[frame] = img_resize
        print("tk処理", frame, image.shape)

    def get_image_tk(self, frame):
        frame = round(frame)
        image_tk = self.data_image_tk[frame]
        return image_tk

    def image_tk_init(self, sta, end):
        self.data_image_tk = [None] * self.frame

    def image_stack(self):
        self.data_image_tk = [None] * self.frame
        #self.data_iamge = [None] * self.frame

    def output_OpenCV(self, sta=None, end=None):
        def print_percent():

            now_percent = f - sta + 1
            end_percent = end - sta + 1

            percent_rate = round(now_percent / end_percent * 100) + 1
            return percent_rate

        def print_time():
            now_time = datetime.datetime.now()
            return now_time - start_time

        if sta is None:
            sta = 0
        if end is None:
            end = self.frame

        if sta < 0:
            sta = 0
        if end >= self.frame - 1:
            end = self.frame - 1

        end += 1

        start_time = datetime.datetime.now()

        #np_zero = ""

        for f in range(sta, end):

            export_draw = self.cpp_encode.execution_main(f)
            #print("\r書き出しを行っています [python - opencv - numpy] 処理時間: {7} 現在: {5} 範囲: {3} - {4} 進捗: {0} / {1} 進捗率: {2} % {6}".format(f + 1, end, print_percent(), sta, end, f+1, np_zero, print_time()), end='')

            output_data = cv2.cvtColor(export_draw.astype('uint8'), cv2.COLOR_RGBA2BGR)
            self.writer.write(output_data)

        print("")
        print("終了 所要時間 : {0}".format(print_time()))
        self.writer.release()


# 再帰的なシーン発火をしないといけない、どうしよう？
