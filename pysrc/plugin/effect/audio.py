# coding:utf-8
import sys
import os
import copy
import cv2
# 削除厳禁！

import sounddevice
import wave
import numpy as np
import time


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = "音声"
        setting_effect.effect_point = {}
        setting_effect.various_fixed = {"path": ""}
        setting_effect.procedure = CentralRole()

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
        try:

            sound_file = None

            if rendering_main_data.check_file_all_control(file_name):
                sound_file = rendering_main_data.get_file_all_control(file_name)
            else:
                sound_file = wave.open(file_name)
                rendering_main_data.add_file_all_control(file_name, sound_file)
            #data, samplerate = sf.read('existing_file.wav')

            self.sound_sampling_rate = sound_file.getframerate()
            self.sound_frame = sound_file.getnframes()  # フレーム数を取得
            self.sound_channles = sound_file.getnchannels()

            sound_data = sound_file.readframes(self.sound_frame)  # 指定したフレーム数の読み込み
            self.import_data = np.frombuffer(sound_data, dtype='int16')

            print("サウンド", len(self.import_data), self.sound_sampling_rate, self.sound_frame)

            # print(self.import_data[0:40])

            # チャンネル数が2(ステレオ)の場合、len(self.import_data)はself.sound_frameの二倍になる

            self.now_file = copy.deepcopy(file_name)
            self.open_status = True

        except:
            self.open_status = False

        print("読み込み状況 :", self.open_status)

    def main(self, rendering_main_data):
        self.installation_sta = rendering_main_data.installation[0]
        self.installation_end = rendering_main_data.installation[1]

        self.fps = rendering_main_data.editor["fps"]
        #rendering_main_data = rendering_main_data
        path = rendering_main_data.various_fixed["path"]

        if path != self.now_file or not self.open_status:
            self.setup(rendering_main_data, path)

        # self.sound(rendering_main_data.b_now_time)

        return rendering_main_data.draw, self.starting_point

    def get_now_file(self):
        return self.now_file, self.installation_sta, self.installation_end

    def sound_init(self):
        self.run_flag = False
        self.latest_process_time = time.time()
        print("sound_init", self.latest_process_time)

    def sound_stop(self):
        sounddevice.stop()

    def sound(self, now_frame, sta_bool=False):

        if not self.installation_sta <= now_frame < self.installation_end:
            return

        if self.run_flag:
            return

        self.run_flag = True

        now_second = now_frame / self.fps
        end_second = self.installation_end / self.fps

        conversion_rate = self.sound_channles * self.sound_sampling_rate

        now_sound_rate_now = round(now_second * conversion_rate)
        now_sound_rate_end = round(end_second * conversion_rate)

        return_import_data = self.import_data[now_sound_rate_now:now_sound_rate_end]

        print("now_sound_rate_now,now_sound_rate_end", len(return_import_data), now_sound_rate_now, now_sound_rate_end)
        sounddevice.play(return_import_data, conversion_rate)
        # sounddevice.play()


# numpy wav:ステレオ時の構造は、左チャンネルと右チャンネルで交互になっている
