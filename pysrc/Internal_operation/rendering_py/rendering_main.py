import uuid
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
import ffmpeg
import os
# import subprocess


class DataStorage:
    def __init__(self):
        self.file_all_control = None
        self.data_image_tk = None
        self.tk_setup_flag = False
        self.setup_file_all_control()

    def setup_file_all_control(self):
        self.file_all_control = {}

    def setup_data_image_tk(self, tk_long):
        self.data_image_tk = [None] * tk_long
        self.tk_setup_flag = True


data_storage = DataStorage()


class EffectPluginElements:
    def __init__(self, draw, effect_id, effect_value, before_value, next_value, various_fixed, now_frame, b_now_time, editor, operation, installation_sta, installation_end):
        # self.draw = draw
        self.draw = draw.astype('uint8')
        self.effect_value = effect_value
        self.before_value = before_value
        self.various_fixed = various_fixed
        self.next_value = next_value
        self.now_frame = now_frame
        self.b_now_time = b_now_time
        self.editor = editor
        self.operation = operation
        self.audio_control = operation["audio_control"]
        self.effect_id = effect_id

        print("audio_control", self.audio_control)

        self.draw_size = {"x": self.draw.shape[1], "y": self.draw.shape[0]}
        self.cv2 = cv2
        self.np = np

        # self.file_system = FileSystem

        self.installation = [installation_sta, installation_end]

        # self.cpp_file = ""

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

        print(data_storage.file_all_control, "sta")

        if not path in list(data_storage.file_all_control.keys()):
            print("file_all_control *** get_file_all_control", path, "None")
            return None

        print("file_all_control *** get_file_all_control", path, data_storage.file_all_control[path])

        print(data_storage.file_all_control, "end")

        return data_storage.file_all_control[path]

    def add_file_all_control(self, path, file):

        print(data_storage.file_all_control, "sta")

        print("file_all_control *** add_file_all_control", path, file)

        if not self.check_file_all_control(path):
            data_storage.file_all_control[path] = copy.deepcopy(file)

        print(data_storage.file_all_control, "end")

    def check_file_all_control(self, path):

        print(data_storage.file_all_control, "sta")

        print("file_all_control *** check_file_all_control", path in list(data_storage.file_all_control.keys()))

        print(data_storage.file_all_control, "end")

        return path in list(data_storage.file_all_control.keys())

    # self.py_Rendering_func = py_Rendering_func


class Rendering:
    def __init__(self):
        # self.rendering_scene_queue = {}
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


# read_time = datetime.datetime.now() - start_time


class SceneOutput:
    def __init__(self, operation, scene_get, get_set_media_object_group, make, scene_id, path):

        print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - SceneOutput初期化")

        self.scene_get = scene_get
        self.get_set_media_object_group = get_set_media_object_group
        self.scene = self.scene_get(scene_id=scene_id)

        # print(scene_get,make,scene_id,path,self.scene)

        self.editor = self.scene.editor

        self.x = int(self.scene.editor["x"])
        self.y = int(self.scene.editor["y"])
        self.fps = int(self.scene.editor["fps"])
        self.frame = int(self.scene.editor["len"])
        # self.preview = self.scene.editor["preview"]
        # print("self.scene.editor", self.scene.editor)

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
        # self.func["FileSystem"] = FileSystem()

        # self.func["plugin_run"] = plugin_run

        # data_image_tk = [None] * self.frame
        # self.data_iamge = [None] * self.frame

        if not data_storage.tk_setup_flag:
            data_storage.setup_data_image_tk(self.frame)

        self.scene_id = copy.deepcopy(self.scene.scene_id)

        self.cpp_encode = self.operation["cppsrc"]["video_main"].VideoExecutionCenter(self.operation, self.func)
        self.cpp_encode.scene_setup(self.scene)

        self.fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)
        self.size = (self.x, self.y)
        self.temp_path = "pysrc/Internal_operation/rendering_py/temp"
        self.output_temp_file_path_mp4 = "{0}/temp_nonsound_temp.mp4".format(self.temp_path)
        self.output_temp_file_path_wav = "{0}/temp_nonsound_temp.wav".format(self.temp_path)

        # self.audio_preview_function_list = []

        self.audio_control = operation["audio_control"]
        # self.audio_control.wav_file_clear()
        self.audio_control.main(self.editor["fps"], self.editor["len"], self.editor["sound_sampling_rate"], self.editor["sound_channel"])

        print("audio_control", self.audio_control)

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

        # self.data_image[sta:end] = self.cpp_encode.execution_main(-1,-1)

        end_time = datetime.datetime.now()

        repair = end_time - start_time

        print("本処理 [ python / C++ ] [ boost ] {0}".format(repair))

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
        pass

    def sound_stop(self):
        self.audio_control.sound_stop()

    def output_tk(self, frame, tk_cash=True, run=False):
        # map(lambda x: x(frame, sta_bool=True), self.audio_preview_function_list)

        # <class 'NoneType'>

        # type(data_image_tk[frame]) is NoneType

        cash_process_flag = False

        frame = round(frame)

        print("tktype", type(data_storage.data_image_tk[frame]))
        print(tk_cash)

        if not data_storage.data_image_tk[frame] is None and tk_cash:
            print("キャッシュ生成済み")
            cash_process_flag = True

        output_data = None

        if not cash_process_flag:
            output_data = self.cpp_encode.execution_preview(frame).astype('uint8').reshape(self.y, self.x, 3)

            # self.audio_preview_function_list = self.cpp_encode.get_audio_function_list()

        # print(self.audio_preview_function_list, run)

        if run:
            self.audio_control.sound_run(frame)

        # object_group = self.cpp_encode.object_group_recovery()
        # self.get_set_media_object_group(data=object_group)

        if cash_process_flag:
            return

        # output_data = self.del_alpha(image)

        # image[:, :, 0] *= image[:, :, 3]
        # image[:, :, 1] *= image[:, :, 3]
        # image[:, :, 2] *= image[:, :, 3]

        # image_cvt = cv2.cvtColor(image.astype('uint8'))
        # print("B合成RGB", np.sum(image_cvt[:, :, 0:3]))

        # cv2.imwrite('wiwi.jpg', image.astype('uint8'))

        print(output_data.shape)

        image_pil = Image.fromarray(output_data)
        resize_size = (640, 360)
        img_resize = image_pil.resize(resize_size)
        # self.image_tk_PhotoImage =
        # img_resize.show()

        data_storage.data_image_tk[frame] = ImageTk.PhotoImage(img_resize)  # ImageTkフォーマットへ変換
        # data_image_tk[frame] = img_resize

    def get_image_tk(self, frame):
        frame = round(frame)
        image_tk = data_storage.data_image_tk[frame]
        return image_tk

    def image_stack(self):

        print("tkinter保管データ初期化")
        data_storage.setup_data_image_tk(self.frame)

    def output_OpenCV(self, sta=None, end=None):

        os.system("mkdir {0}".format(self.temp_path))
        self.writer = cv2.VideoWriter(self.output_temp_file_path_mp4, self.fmt, self.scene.editor["fps"], self.size)  # ライター作成

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

        # np_zero = ""

        # self.audio_control.addition_process()

        for f in range(sta, end):

            f_time_sta = datetime.datetime.now()
            export_draw = self.cpp_encode.execution_main(f).astype('uint8').reshape(self.y, self.x, 3)
            f_time_end = datetime.datetime.now()
            print("f_time", f_time_end - f_time_sta)
            # print("\r書き出しを行っています [python - opencv - numpy] 処理時間: {7} 現在: {5} 範囲: {3} - {4} 進捗: {0} / {1} 進捗率: {2} % {6}".format(f + 1, end, print_percent(), sta, end, f+1, np_zero, print_time()), end='')

            # output_data = cv2.cvtColor(export_draw.astype('uint8'), cv2.COLOR_RGBA2BGR)
            #output_dataBGR = self.del_alpha(export_draw)

            #output_data = cv2.cvtColor(export_draw, cv2.COLOR_BGR2RGB)

            self.writer.write(export_draw)

        self.writer.release()
        # file_all_control = {}
        print(data_storage.file_all_control)

        print("音源処理開始 [ffmpeg - python] *********")

        print("audio_control", self.audio_control)

        self.audio_control.addition_process()
        self.audio_control.output_audio_file(self.output_temp_file_path_wav)

        print(self.path)

        os.system("ffmpeg -i {0} -i {1} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {2}".format(self.output_temp_file_path_mp4, self.output_temp_file_path_wav, self.path))

        # # 映像の読み込み
        # instream_v = ffmpeg.input(self.output_temp_file_path_mp4)
        # # 音声の読み込み
        # instream_a = ffmpeg.input(self.output_temp_file_path_wav)
        # # コーデックと出力ファイルの指定
        # stream = ffmpeg.output(instream_v, instream_a, self.path, vcodec="copy", acodec="copy")
        # # 実行
        # ffmpeg.run(stream)

        # output_temp_file = ffmpeg.input(self.output_temp_file_path_mp4)
        # silence_audio = output_temp_file.audio

        # for a in self.audio_preview_function_list:
        #    file_name = a[3]()
        # uuid_name = self.scene.editor("sound_temp_{0}_sound".format(self.path))

        # sound_long = file_name[2] - file_name[1]

        # if sound_long >= (end - sta):
        #    sound_long = end + sta

        # now_time = datetime.datetime.now()
        # temp_sound_file_name = "{0}/{1}_{2}.wav".format(self.temp_path, str(uuid.uuid1()), str(now_time.strftime('%y%m%H%M%S%f')))
        # os.system("ffmpeg -i {0} -ss {3} -t {4} {1}".format(self.output_temp_file_path_mp4, temp_sound_file_name,sta,end))

        # file_data = ffmpeg.input(file_name)

        print("音源処理終了 [ffmpeg - python] *********")

        os.system("rm -rf {0}".format(self.temp_path))

        print("")
        print("終了 所要時間 : {0}".format(print_time()))

        # os.system("rmdir temp")


# 再帰的なシーン発火をしないといけない、どうしよう？
# https://maku77.github.io/python/env/call-external-program.html
