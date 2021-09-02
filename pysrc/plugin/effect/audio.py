# coding:utf-8
import sys
import os
import copy
import cv2
# 削除厳禁！

import sounddevice as sd
import wave
import numpy as np


class InitialValue:
    def __init__(self, setting_effect):
        setting_effect.effect_name = "画像"
        setting_effect.effect_point = {}
        setting_effect.various_fixed = {"path": ""}
        setting_effect.procedure = CentralRole()

        setting_effect.audio = True


class CentralRole:
    def __init__(self):
        self.starting_point = [0, 0]

        self.now_file = None
        self.open_status = False

        self.rendering_main_data = None

        self.sound_file = None
        self.import_data = None
        self.sampling_rate = None
        self.sound_frame = 0

    def setup(self, file_name):
        try:
            #data, samplerate = sf.read('existing_file.wav')
            self.sound_file = wave.open(file_name)
            self.sampling_rate = self.sound_file.getframerate()
            self.sound_frame = self.sound_file.getnframes()  # フレーム数を取得

            sound_data = self.sound_file.readframes(self.sound_frame)  # 指定したフレーム数の読み込み
            self.import_data = np.frombuffer(sound_data, dtype='int16')

            print("サウンド", len(self.import_data), self.sampling_rate, self.sound_frame)

            # チャンネル数が2(ステレオ)の場合、len(self.import_data)はself.sound_frameの二倍になる

            self.now_file = copy.deepcopy(file_name)
            self.open_status = True

        except:
            self.open_status = False

    def main(self, rendering_main_data):
        self.rendering_main_data = rendering_main_data
        path = self.rendering_main_data.various_fixed["path"]

        if path != self.now_file or not self.open_status:
            self.setup(path)

        return self.rendering_main_data.draw, self.starting_point

    def sound(self, now_all_frame):
        now_frame = now_all_frame - self.rendering_main_data.installation[0]
        pass
