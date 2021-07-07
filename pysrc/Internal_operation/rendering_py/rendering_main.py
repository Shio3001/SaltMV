import time
import cv2
import numpy as np
import datetime

class Rendering:
    def __init__(self):
        self.operation = None
        self.cpp_encode = None
    def setapp_init(self,operation,scene):
        self.operation = operation
        x = scene.editor["x"]
        y = scene.editor["y"]
        fps = scene.editor["fps"]
        frame = scene.editor["len"]
        #self.cpp_encode  = self.operation["cppsrc"]["video_main"].VideoExecutionCenter(x,y,fps,frame)
        print(self.operation["cppsrc"]["video_main"])
        print(self.operation["cppsrc"]["video_main"].VideoExecutionCenter)
        self.cpp_encode  = self.operation["cppsrc"]["video_main"].VideoExecutionCenter()
        print(self.cpp_encode.execution)
        print(self.cpp_encode.sta)
        #self.cpp_encode.layer_interpretation("testtest")
        self.cpp_encode.sta(x,y,fps,frame)
        #self.cpp_encode.init(x,y,fps,frame)

    def video_output(self, scene, path):
        start_time = datetime.datetime.now()

        self.cpp_encode.execution(scene)

        read_time = datetime.datetime.now() - start_time
        print(read_time)
