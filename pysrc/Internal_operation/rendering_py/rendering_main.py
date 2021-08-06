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


class EffectPluginElements:
    def __init__(self, draw, effect_value, before_value, next_value, various_fixed, now_frame, editor, operation):
        #self.draw = draw
        self.draw = draw.astype('uint8')
        self.effect_value = effect_value
        self.before_value = before_value
        self.various_fixed = various_fixed
        self.next_value = next_value
        self.now_frame = now_frame
        self.editor = editor
        self.operation = operation
        self.draw_size = {"x": self.draw.shape[1], "y": self.draw.shape[0]}
        self.cv2 = cv2
        self.np = np

    def area_expansion(self, old_draw, x=0, y=0):
        old_size_x = old_draw.shape[1]
        old_size_y = old_draw.shape[0]
        if x == 0:
            x = old_size_x
        if y == 0:
            y = old_size_y

        new_draw = np.zeros((y, x, 4))
        return new_draw

    #self.py_Rendering_func = py_Rendering_func


class Rendering:
    def __init__(self):
        #self.rendering_scene_queue = {}
        self.operation = None
        self.scene_get = None

    def set(self, operation, scene_get):
        self.operation = operation
        self.scene_get = scene_get

    def make(self, scene_id, path):
        # print(self.operation["video_image"].image_add)
        make_data = SceneOutput(self.operation, self.scene_get, self.make, scene_id, path)
        return make_data


#read_time = datetime.datetime.now() - start_time


class SceneOutput:
    def __init__(self, operation, scene_get, make, scene_id, path):
        self.scene_get = scene_get
        self.scene = self.scene_get(scene_id=scene_id)

        # print(scene_get,make,scene_id,path,self.scene)

        self.x = self.scene.editor["x"]
        self.y = self.scene.editor["y"]
        self.fps = self.scene.editor["fps"]
        self.frame = self.scene.editor["len"]
        self.operation = operation
        self.path = path

        self.func = {}
        self.func["scene_make"] = make
        self.func["main"] = self.output_main
        self.func["frame"] = self.output_frame
        self.func["tk"] = self.output_tk
        self.func["out"] = self.output_OpenCV
        self.func["layer_number"] = self.layer_id_number
        self.func["EffectPluginElements"] = EffectPluginElements

        self.data_image_tk = [None] * self.frame
        self.data_iamge = [None] * self.frame

        self.scene_id = copy.deepcopy(self.scene.scene_id)

        self.cpp_encode = self.operation["cppsrc"]["video_main"].VideoExecutionCenter(self.operation, self.scene, self.func)

        self.fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)
        self.size = (self.x, self.y)
        self.writer = cv2.VideoWriter(self.path, self.fmt, self.scene.editor["fps"], self.size)  # ライター作成

    def layer_id_number(self, layer_id):
        return self.scene.layer_group.layer_layer_id[layer_id]

    def output_main(self, sta=None, end=None):

        start_time = datetime.datetime.now()

        if sta is None:
            sta = 0
        if end is None:
            end = self.frame

        #self.data_image[sta:end] = self.cpp_encode.execution_main(-1,-1)
        draw_list = self.cpp_encode.execution_main(-1, -1)
        print(draw_list.shape)

        end_time = datetime.datetime.now()

        repair = end_time - start_time

        print("本処理 [ python C++ ] [ boost ] {0}".format(repair))

        self.output_OpenCV(sta, end, draw_list)
        # s

    def output_frame(self, frame=None):
        image = self.cpp_encode.execution_preview(frame)
        return image

    def get_image(self, frame):
        return self.data_image[frame]

    def image_init(self, sta, end):
        self.data_image[sta:end] = np.zeros((end-sta))

    def output_tk(self, frame, tk_cash=True):
        # if self.data_image_tk[frame] != None and tk_cash:
        #    return

        image = self.cpp_encode.execution_preview(frame)
        image_cvt = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGBA2RGB)

        cv2.imwrite('wiwi.jpg', image.astype('uint8'))

        image_pil = Image.fromarray(image_cvt)
        resize_size = (640, 360)
        img_resize = image_pil.resize(resize_size)
        # self.image_tk_PhotoImage =
        # img_resize.show()

        self.data_image_tk[frame] = ImageTk.PhotoImage(img_resize)  # ImageTkフォーマットへ変換
        print("tk処理", frame, image.shape)

    def get_image_tk(self, frame):
        image_tk = self.data_image_tk[frame]
        return image_tk

    def image_tk_init(self, sta, end):
        self.data_image_tk = [None] * self.frame

    def image_stack(self):
        self.data_image_tk = [None] * self.frame
        self.data_iamge = [None] * self.frame

    def output_OpenCV(self, sta=None, end=None, draw_list=None):
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

        for f in range(sta, end):

            if not draw_list is None:
                export_draw = draw_list[f]
            else:
                export_draw = self.data_iamge[f]

                if export_draw == 0:
                    export_draw = np.zeros((self.y, self.x, 4))
                    np_zero = "[ 未生成のため生成 ]"

            np_zero = ""

            print("\r書き出しを行っています [python - opencv - numpy] 処理時間: {7} 現在: {5} 範囲: {3} - {4} 進捗: {0} / {1} 進捗率: {2} % {6}".format(f + 1, end, print_percent(), sta, end, f+1, np_zero, print_time()), end='')

            output_data = cv2.cvtColor(export_draw.astype('uint8'), cv2.COLOR_RGBA2BGR)
            self.writer.write(output_data)

        print("")
        print("終了 所要時間 : {0}".format(print_time()))
        self.writer.release()


# 再帰的なシーン発火をしないといけない、どうしよう？
