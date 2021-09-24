# coding:utf-8
import sys
import os
import copy
import cv2
# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effect_point = {"fps_point": 0}
        setting_effect.various_fixed = {"path": "", "frame_configuration": False}
        setting_effect.procedure = CentralRole()


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        self.now_file = ""

        self.open_status = False

    def setup(self, file_name):
        self.video_data = cv2.VideoCapture(file_name)
        self.video_fps = self.video_data.get(cv2.CAP_PROP_FPS)
        self.now_file = copy.deepcopy(file_name)
        self.open_status = self.video_data.isOpened()

        if not self.open_status:
            return

    def main(self, data):

        if data.various_fixed["path"] != self.now_file or not self.open_status:
            self.setup(data.various_fixed["path"])

        if not self.open_status:
            return data.draw, self.starting_point

        fps_point = data.effect_value["fps_point"]

        fps = data.editor["fps"]

        print("fps", fps, "video_fps", self.video_fps)

        if not data.various_fixed["frame_configuration"]:

            fps_point_editor = fps_point + data.now_frame - data.installation[0]
            fps_point = round(fps_point_editor * fps / self.video_fps)

        self.video_data.set(cv2.CAP_PROP_POS_FRAMES, fps_point)
        ret, frame = self.video_data.read()
        data.draw = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        return data.draw, self.starting_point
