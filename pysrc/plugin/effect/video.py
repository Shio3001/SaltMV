# coding:utf-8
import sys
import os
import copy
import datetime
import ffmpeg
import numpy as np
# 削除厳禁！


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = str(os.path.basename(__file__)).replace('.py', '')
        setting_effect.effect_point = {"fps_point": 0}
        setting_effect.various_fixed = {"path": "", "frame_configuration": False}
        setting_effect.effect_point_path_name = ["path"]
        setting_effect.procedure = CentralRole()
        # setting_effect.cpp = "read_video"


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        self.now_file = ""

        self.open_status = False

    def setup(self, file_name):
        # self.video_data = cv2.VideoCapture(file_name)
        # self.video_fps = self.video_data.get(cv2.CAP_PROP_FPS)
        # self.now_file = copy.deepcopy(file_name)
        # self.open_status = self.video_data.isOpened()

        self.file_name = file_name
        self.video_info = ffmpeg.probe(self.file_name)

        print(self.video_info)

        self.width = round(self.video_info["streams"][0]["width"])
        self.height = round(self.video_info["streams"][0]["height"])
        self.video_fps = round(eval(self.video_info["streams"][0]["r_frame_rate"]))

        if not self.video_info is None:
            self.open_status = True

    def frame_load(self, frame):
        out, _ = (
            ffmpeg
            .input(self.file_name, ss=40, t=0.03)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True)
        )

        self.video_data = np.frombuffer(out, np.uint8).astype('uint8').reshape(self.height, self.width, 3)

        return self.video_data[0]

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

        data.draw = self.frame_load(int(fps_point))

        return data.draw, self.starting_point
