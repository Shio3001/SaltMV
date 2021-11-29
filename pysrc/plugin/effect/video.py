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
        # setting_effect.cpp = "read_video"


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]
        self.now_file = ""

    def main(self, rendering_main_data):

        if not self.open_status:
            return rendering_main_data.draw, self.starting_point

        fps_point = rendering_main_data.effect_value["fps_point"]
        fps = rendering_main_data.editor["fps"]
        print("fps", fps, "video_fps", self.video_fps)
        if not rendering_main_data.various_fixed["frame_configuration"]:
            fps_point_editor = fps_point + rendering_main_data.now_frame - rendering_main_data.installation[0]
            fps_point = round(fps_point_editor * fps / self.video_fps)

        if rendering_main_data.salt_file.get_bool(rendering_main_data.various_fixed["path"]) is False:
            pass
        else:
            rendering_main_data.draw = rendering_main_data.salt_file.get_video(rendering_main_data.various_fixed["path"], int(fps_point))

        return rendering_main_data.draw, self.starting_point
