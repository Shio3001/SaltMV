import wave
from numpy.core.numeric import outer
import sounddevice

import numpy as np

import scipy
import scipy.signal as signal
from scipy.io.wavfile import write as scipy_write
import math
import copy
import cv2
import librosa


class AudioIndividual:
    def __init__(self, audio_data: np.numarray, sound_channles, sta_frame, end_frame, effect_id):
        self.audio_data = audio_data
        self.sound_channles = sound_channles
        self.sta_frame = sta_frame
        self.end_frame = end_frame
        self.effect_id = effect_id


class AudioControl:
    def __init__(self):

        print("     **********AudioControl __init__")

        self.fps = 0
        self.criterion_conversion_rate = 0
        self.criterion_sound_channles = 0

        self.audio_individual_data = {}

        self.one_fps_samplingsize = 1

        self.combined_for_process = np.full(1, 0, dtype=np.float32)
        self.combined_for_play = np.full(1, 0, dtype=np.float32)

        self.setup_flag = False  # 流す準備ができているかどうか
        self.run_flag = False  # 現在流しているか

        self.combined_size_1channel = 0
        self.combined_size = 0

        # self.audio_data = 0

    def main(self, fps, frame_len, criterion_conversion_rate, criterion_sound_channles):
        print("     **********AudioControl main")

        self.fps = fps
        self.frame_len = frame_len
        self.criterion_conversion_rate = int(criterion_conversion_rate)
        self.criterion_sound_channles = int(criterion_sound_channles)

        self.one_fps_samplingsize = round(criterion_conversion_rate / fps)

        self.combined_size_1channel = frame_len * self.one_fps_samplingsize
        self.combined_size = self.criterion_sound_channles * self.combined_size_1channel

        print(type(self.combined_size), self.combined_size, self.criterion_sound_channles, frame_len, self.one_fps_samplingsize)
        self.combined_for_process = np.full(self.combined_size, 0, dtype=np.float32)

    def audio_individual_data_existence(self, effect_id):
        keys = self.audio_individual_data.keys()

        existence_bool = effect_id in keys
        return existence_bool

    def add(self, effect_id, add_import_data, add_conversion_rate, sound_channles, sta_frame, end_frame):

        print("     **********AudioControl add", effect_id, " / sound_channles", sound_channles)
        self.audio_individual_data[effect_id] = AudioIndividual(add_import_data.reshape(-1), sound_channles, sta_frame, end_frame, effect_id)

    def del_audio_individual_data(self, effect_id):

        print("     **********AudioControl del_audio_individual_data")

        del self.audio_individual_data[effect_id]

    def edit_installation(self, effect_id, sta_frame, end_frame):
        self.audio_individual_data[effect_id].sta_frame = sta_frame
        self.audio_individual_data[effect_id].end_frame = end_frame

    def get_installation(self, effect_id):
        return self.audio_individual_data[effect_id].sta_frame, self.audio_individual_data[effect_id].end_frame

    def addition_process(self):
        print("     **********AudioControl addition_process", len(list(self.audio_individual_data.values())))

        self.combined_for_process = np.full(self.combined_size, 0, dtype=np.float32)

        audio_individual_data_values = list(self.audio_individual_data.values())
        for v in audio_individual_data_values:
            ss = v.sta_frame * self.one_fps_samplingsize  # * v.sound_channles
            es = v.end_frame * self.one_fps_samplingsize  # * v.sound_channles

            vss = 0
            ves = (v.end_frame - v.sta_frame) * self.one_fps_samplingsize  # * v.sound_channles

            print("v.audio_data", v.audio_data, v.audio_data.shape)
            print("ss, es, vss, ves", ss, es, vss, ves)
            print("one_fps_samplingsize", self.one_fps_samplingsize)
            print("v.sound_channles", v.sound_channles)

            if self.criterion_sound_channles == v.sound_channles:
                print(" - - - - - - - - - - - - - - - - -チャンネル数制御 一致", v.sound_channles, " -> ", self.criterion_sound_channles)

                for cpuls in range(self.criterion_sound_channles):
                    cpuls_ss = ss + cpuls * self.combined_size_1channel  # ここ間違っているような気がする
                    cpuls_es = es + cpuls * self.combined_size_1channel
                    cpuls_vss = vss + cpuls * self.combined_size_1channel
                    cpuls_ves = ves + cpuls * self.combined_size_1channel

                    self.combined_for_process[cpuls_ss:cpuls_es] += v.audio_data[cpuls_vss:cpuls_ves]

            elif self.criterion_sound_channles != v.sound_channles:  # 数合わせ：公倍数方式
                print(" - - - - - - - - - - - - - - - - -チャンネル数制御 公倍数方式", v.sound_channles, " -> ", self.criterion_sound_channles)

                # 公倍数までデータを増やす
                common_multiple = self.criterion_sound_channles * v.sound_channles
                multiple_val_riterion = v.sound_channles
                multiple_val_individual = self.criterion_sound_channles

                print("                  公倍数", multiple_val_riterion, multiple_val_riterion, multiple_val_individual)

                multiple_individual_data = copy.deepcopy(v.audio_data[vss:ves])

                print("                  A", multiple_individual_data.shape)

                loop_sta = 0
                loop_end = 0

                if v.sound_channles == 1:
                    loop_sta = 0
                    loop_end = multiple_val_individual - 1
                else:
                    loop_sta = 1
                    loop_end = multiple_val_individual

                for cplus in range(loop_sta, loop_end):  # データの個数を公倍数のところまで増やしていく , 縦方向に結合していく
                    cplus_vss = vss + self.combined_size_1channel * cplus
                    cplus_ves = ves + self.combined_size_1channel * cplus

                    print("                  B1", cplus_vss, cplus_ves, v.audio_data.shape, v.audio_data[cplus_vss:cplus_ves].shape)
                    multiple_individual_data += v.audio_data[cplus_vss:cplus_ves]
                    print("                  B2", cplus, multiple_individual_data.shape)

                multiple_individual_data /= multiple_val_individual
                self.combined_for_process[ss:es] += multiple_individual_data[:]

                # for cadd in range(multiple_val_riterion - 1):  # データの個数を公倍数のところまで増やしていく , 縦方向に結合していく
                #     multiple_individual_data.vstack(multiple_individual_data[0])
                #     print("                  C", cadd, multiple_individual_data.shape)

                print("                  D", multiple_individual_data.shape)
                print("                  E", self.combined_for_process.shape)

                # 目的の数まで減らす

            self.combined_for_play = self.combined_for_process.reshape([2, -1],order='F')

            print("combined", self.combined_for_process)
            print("self.combined_for_process[ss:es]", self.combined_for_process[ss:es])

        print("音源総和", np.sum(self.combined_for_process))

        self.setup_flag = True

    def sound_stop(self):
        print("     **********AudioControl sound_stop")

        print("停止 sound_stop")

        self.run_flag = False
        sounddevice.stop()

    def sound_run(self, now_frame):
        print("     **********AudioControl sound_run")

        if not self.setup_flag or self.run_flag:
            return

        ss = now_frame * self.one_fps_samplingsize  # * sound_channles
        combined_1dimension = self.combined_for_play[ss:-1]
        print("再生", combined_1dimension, self.criterion_conversion_rate)

        sounddevice.play(combined_1dimension, self.criterion_conversion_rate)

        self.run_flag = True

    def output_audio_file(self, path):
        print("     **********AudioControl output_audio_file")

        combined_1dimension = self.combined_for_play
        scipy_write(path, self.criterion_conversion_rate, combined_1dimension)


# https://qiita.com/sumita_v09/items/808a3f8506065639cf51
