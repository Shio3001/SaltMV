import time
import cv2
import numpy as np
import datetime
import copy
class Rendering:
    def __init__(self):
        self.rendering_scene_queue = {}

        self.operation = None
        self.cpp_encode = None
    def setapp_init(self,operation):
        self.operation = operation

    def make_encode_scene(self,scene):
        self.rendering_scene_queue[scene.scene_id] = SceneOutput(self.operation,scene)
        #video_image_control = self.operation["video_image"]

    def playback_preview(self,scene_id):
        pass

    def video_output(self, scene_id, out_path):
        start_time = datetime.datetime.now()
        self.rendering_scene_queue[scene_id].cpp_encode.execution()
        #self.operation["plugin"]["other"]["py_effect_plugin"].EffectPluginElements()
        read_time = datetime.datetime.now() - start_time
        print(read_time)

class SceneOutput:
    def __init__(self,operation,scene):
        self.scene = scene
        self.x = scene.editor["x"]
        self.y = scene.editor["y"]
        self.fps = scene.editor["fps"]
        self.frame = scene.editor["len"]
        self.scene_id =  copy.deepcopy(scene.scene_id)
        self.operation = operation
        self.cpp_encode  = self.operation["cppsrc"]["video_main"].VideoExecutionCenter(self.operation,self.x,self.y,self.fps,self.frame)


    



#再帰的なシーン発火をしないといけない、どうしよう？
