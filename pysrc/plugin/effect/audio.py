# coding:utf-8
import sys
import os
import copy
import cv2
# 削除厳禁！

import sounddevice
import wave
import librosa

import numpy as np
import time
import traceback


class SendFileAudio:
    def __init__(self, audio_numpy, sound_sampling_rate, sound_frame, sound_channles):
        self.audio_numpy = audio_numpy
        self.sound_sampling_rate = sound_sampling_rate
        self.sound_frame = sound_frame
        self.sound_channles = sound_channles


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = "音声"
        setting_effect.effect_point = {}
        setting_effect.various_fixed = {"path": "", "start_f": 0}
        setting_effect.effect_point_path_name = ["path"]
        setting_effect.procedure = CentralRole()
        setting_effect.path_type = {"path": "audio"}
        setting_effect.audio = True


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]

        self.now_file = None
        self.open_status = False

        #rendering_main_data = None

        #sound_file = None
        self.import_data = None
        self.sound_sampling_rate = None
        self.sound_frame = 0
        self.sound_channles = 0

        self.installation_sta = 0
        self.installation_end = 0
        self.fps = 0

        self.latest_process_time = None

        self.run_flag = False

        #self.mode = None

    def setup(self, rendering_main_data, file_name):

        self.open_status = rendering_main_data.salt_file.get_bool(file_name)

        self.setup_audio_control(rendering_main_data, file_name)

    def setup_audio_control(self, rendering_main_data, file_name):

        if not self.open_status:
            return

        self.start_f = int(copy.deepcopy(rendering_main_data.various_fixed["start_f"]))

        now_inside_second = self.start_f / self.fps
        end_inside_second = (self.start_f + self.installation_end - self.installation_sta) / self.fps

        self.get_data = rendering_main_data.salt_file.get_data(file_name)

        self.sound_channles = self.get_data.channel
        self.sound_sampling_rate = self.get_data.sampling_rate
        self.import_data = self.get_data.audio

        conversion_rate = self.sound_channles * self.sound_sampling_rate

        now_sound_rate_now = round(now_inside_second * conversion_rate)
        now_sound_rate_end = round(end_inside_second * conversion_rate)

        return_import_data = self.import_data[now_sound_rate_now:now_sound_rate_end]

        rendering_main_data.audio_control.add(rendering_main_data.effect_id, return_import_data, self.sound_sampling_rate, self.sound_channles, self.installation_sta, self.installation_end)
        rendering_main_data.audio_control.addition_process()

    def main(self, rendering_main_data):
        self.installation_sta = rendering_main_data.installation[0]
        self.installation_end = rendering_main_data.installation[1]

        self.fps = rendering_main_data.editor["fps"]
        path = rendering_main_data.various_fixed["path"]

        existence = rendering_main_data.audio_control.audio_individual_data_existence(rendering_main_data.effect_id)

        if path != self.now_file or not self.open_status:
            self.setup(rendering_main_data, path)

        elif int(rendering_main_data.various_fixed["start_f"]) != self.start_f or not existence:
            self.setup_audio_control(rendering_main_data, path)

        if self.open_status:
            sf, ef = rendering_main_data.audio_control.get_installation(rendering_main_data.effect_id)
            installation_consistency = sf == self.installation_sta and ef == self.installation_end

            if not installation_consistency:
                self.setup_audio_control(rendering_main_data, path)

        return "AUDIO"

    def get_now_file(self):
        return self.now_file, self.installation_sta, self.installation_end

    def sound_init(self):
        self.run_flag = False
        self.latest_process_time = time.time()
        print("sound_init", self.latest_process_time)

    def sound_stop(self):
        pass

    def sound(self, now_frame, sta_bool=False):

        if not self.installation_sta <= now_frame < self.installation_end:
            return

        if self.run_flag:
            return

        self.run_flag = True

        #print("now_sound_rate_now,now_sound_rate_end", len(return_import_data), now_sound_rate_now, now_sound_rate_end)
       # sounddevice.play(return_import_data, conversion_rate)
        # sounddevice.play()


# numpy wav:ステレオ時の構造は、左チャンネルと右チャンネルで交互になっている
# 音声実装難しすぎて死にそう 画像は1/30秒とか1/60秒単位で、音声は主に1/44100秒単位で扱わないといけないからダメ
