import time
import cv2
import numpy as np
import datetime
import copy
from PIL import Image, ImageDraw, ImageFilter , ImageTk
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

class Rendering:
    def __init__(self):
        #self.rendering_scene_queue = {}
        self.operation = None
        self.scene_get = None

    def set(self,operation,scene_get):
        self.operation = operation
        self.scene_get = scene_get

    def make(self,scene_id,path):
        #print(self.operation["video_image"].image_add)
        make_data = SceneOutput(self.operation,self.scene_get,self.make ,scene_id,path)
        return make_data


#read_time = datetime.datetime.now() - start_time


class SceneOutput:
    def __init__(self,operation,scene_get,make,scene_id,path):
        self.scene_get = scene_get
        self.scene = self.scene_get(scene_id=scene_id)

        #print(scene_get,make,scene_id,path,self.scene)

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

        
        self.data_image_tk = np.zeros((self.frame))
        self.data_iamge = np.zeros((self.frame))

        self.scene_id =  copy.deepcopy(self.scene.scene_id)

        self.cpp_encode  = self.operation["cppsrc"]["video_main"].VideoExecutionCenter(self.operation,self.scene,self.func)


        self.fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)
        self.size = (self.x, self.y)
        self.writer = cv2.VideoWriter(self.path , self.fmt, self.scene.editor["fps"], self.size)  # ライター作成


    def output_main(self):
        image_list = self.cpp_encode.execution_main()

    def output_frame(self,frame=None):
        image = self.cpp_encode.execution_preview(frame)
        return image

    def output_tk(self,frame,tk_cash=True):
        if self.data_image_tk[frame] != 0 and tk_cash:
            return

        image = self.cpp_encode.execution_preview(frame)
        image_pil = Image.fromarray(image)  # RGBからPILフォーマットへ変換
        resize_size = (1280,720)
        img_resize = image_pil.resize(resize_size)
        image_tk = ImageTk.PhotoImage(img_resize)  # ImageTkフォーマットへ変換
        self.data_image_tk[frame] = image_tk

    def get_image_tk(self,frame):
        return self.data_image_tk[frame]

    def image_tk_init(self,sta,end):
        self.data_image_tk[sta:end] = np.zeros((end-sta))
        

    def output_OpenCV(self,sta=None,end=None):

        if sta is None:
            sta = 0
        if end is None:
            end = self.frame           

        if sta < 0:
            sta = 0
        if end >= self.frame - 1:
            end = self.frame - 1

        end += 1


        for f in range(sta,end):
            export_draw = self.data_iamge[f]

            if export_draw == 0:
                export_draw = np.zeros((self.y, self.x, 4))

            def percent():

                now_percent = f - sta + 1
                end_percent = end - sta + 1

                percent_rate = round(now_percent / end_percent * 100) + 1
                return percent_rate

            print("\r書き出しを行っています [python - opencv - numpy] 現在: {5} 範囲: {3} - {4} 進捗: {0} / {1} 進捗率: {2} %".format(f + 1, end, percent(),sta,end,f+1), end='')

            output_data = cv2.cvtColor(export_draw.astype('uint8'), cv2.COLOR_RGBA2BGR)
            self.writer.write(output_data)

        self.writer.release()




    



#再帰的なシーン発火をしないといけない、どうしよう？
