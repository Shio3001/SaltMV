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

        setting_effect.procedure = CentralRole()
        setting_effect.path_type = {"path": "video"}


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        self.now_file = ""

    def set_message(self, element, salt_file):
        path = element.various_fixed["path"]
        file_data = salt_file.get_data(path)
        message = file_data.video_frame
        return message

    def main(self, rendering_main_data):

        path = rendering_main_data.various_fixed["path"]

        fps_point = rendering_main_data.effect_value["fps_point"]
        fps_point_b = rendering_main_data.first_value["fps_point"]
        fps = rendering_main_data.editor["fps"]

        frame_configuration = str(rendering_main_data.various_fixed["frame_configuration"]) == "True"

        now_fps = 0

        return_draw = None
        if not rendering_main_data.salt_file.get_bool(path):
            return_draw = rendering_main_data.draw
        else:

            video_fps = rendering_main_data.salt_file.get_data(path).video_fps

            if frame_configuration:
                now_fps = round(fps_point)

            elif not frame_configuration:
                fps_point_editor = rendering_main_data.now_frame - rendering_main_data.installation[0]
                now_fps = round(fps_point_editor * video_fps / fps) + fps_point_b

            print("書き出し番号:fps_point", now_fps, frame_configuration)

            return_draw = rendering_main_data.salt_file.get_video(path, int(now_fps))

        return "DRAW", return_draw, self.starting_point
