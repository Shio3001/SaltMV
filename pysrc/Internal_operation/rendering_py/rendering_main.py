import time
import cv2
import numpy as np
import datetime
import copy
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
        self.func["tk"] = self.output_return_tk
        self.func["out"] = self.output_OpenCV

        self.image_tk = {}

        self.scene_id =  copy.deepcopy(self.scene.scene_id)

        self.cpp_encode  = self.operation["cppsrc"]["video_main"].VideoExecutionCenter(self.operation,self.scene,self.func)

    def output_main(self):
        self.cpp_encode.execution_main()

    def output_frame(self,frame=None):
        self.cpp_encode.execution_preview()

    def output_return_tk(self,frame):
        frame_image_tk = self.cpp_encode.execution_preview_return(frame)
        return frame_image_tk

    def output_OpenCV(self,sta=None,end=None):

        if sta is None:
            sta = 0
        if sta is None:
            sta = self.frame           

        if sta < 0:
            sta = 0
        if end >= self.frame - 1:
            end = self.frame - 1

        for f in range(sta,end):
            pass




    



#再帰的なシーン発火をしないといけない、どうしよう？
