# coding:utf-8
import sys
import os
import copy
import cv2
# 削除厳禁！

import sounddevice
import wave
import numpy as np


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

        self.rendering_main_data = None

        self.sound_file = None
        self.import_data = None
        self.sound_sampling_rate = None
        self.sound_frame = 0
        self.sound_channles = 0

    def setup(self, file_name):
        try:
            #data, samplerate = sf.read('existing_file.wav')
            self.sound_file = wave.open(file_name)
            self.sound_sampling_rate = self.sound_file.getframerate()
            self.sound_frame = self.sound_file.getnframes()  # フレーム数を取得
            self.sound_channles = self.sound_file.getnchannels()

            sound_data = self.sound_file.readframes(self.sound_frame)  # 指定したフレーム数の読み込み
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
        self.rendering_main_data = rendering_main_data
        path = self.rendering_main_data.various_fixed["path"]

        if path != self.now_file or not self.open_status:
            self.setup(path)

        self.sound(self.rendering_main_data.b_now_time)

        return self.rendering_main_data.draw, self.starting_point

    def sound(self, now_frame, sta_bool=False):

        if sta_bool:
            now_frame -= self.rendering_main_data.installation[0]

        now_second = now_frame / self.rendering_main_data.editor["fps"]

        print("sound", now_frame, now_second)

        zero_safe = now_second != 0 and now_second >= 1

        if zero_safe:
            if now_second % round(now_second) != 0:
                print("now_second // round(now_second)返却", now_second % round(now_second))
                return

        conversion_rate = self.sound_channles * self.sound_sampling_rate

        now_sound_rate = round(now_second * conversion_rate)
        now_sound_rate_1 = round((now_second + 1) * conversion_rate)

        print(now_sound_rate, now_sound_rate_1)

        sounddevice.play(self.import_data[now_sound_rate:now_sound_rate_1], self.sound_sampling_rate)


# numpy wav:ステレオ時の構造は、左チャンネルと右チャンネルで交互になっている
