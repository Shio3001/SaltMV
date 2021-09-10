import wave
import sounddevice

import numpy as np

import scipy
import scipy.signal as signal
import math
import copy


class AudioIndividual:
    def __init__(self, audio_data: np.numarray, sound_channles, sta_frame, end_frame):
        self.audio_data = audio_data
        self.sound_channles = sound_channles
        self.sta_frame = sta_frame
        self.end_frame = end_frame


class AudioControl:
    def __init__(self):
        self.fps = 0
        self.criterion_conversion_rate = 0
        self.criterion_sound_channles = 0

        self.audio_individual_data = {}

        self.one_fps_samplingsize = 1

        self.combined = np.full(1, 0, dtype=np.int16)

        #self.audio_data = 0

    def main(self, fps, frame_len, criterion_conversion_rate, criterion_sound_channles):
        self.fps = fps
        self.frame_len = frame_len
        self.criterion_conversion_rate = criterion_conversion_rate
        self.criterion_sound_channles = criterion_sound_channles

        self.one_fps_samplingsize = round(criterion_conversion_rate / fps)

        self.combined_size = frame_len * self.criterion_conversion_rate * self.criterion_sound_channles
        self.combined = np.full(self.combined_size, 0, dtype=np.int16)

    def add(self, effect_id, add_import_data: np.numarray, add_conversion_rate, sound_channles, sta_frame, end_frame):

        result_data = None

        if add_conversion_rate != self.criterion_conversion_rate:

            lcm = math.lcm(add_conversion_rate, self.criterion_conversion_rate)

            lcm_data = self.upsampling(add_import_data, add_conversion_rate, lcm)
            print("lcm_data", lcm_data)
            result_data = self.downsampling(lcm_data, add_conversion_rate)
            print("result_data", result_data)

        if add_conversion_rate == self.criterion_conversion_rate:
            result_data = add_import_data
            print("=")

        print(result_data)

        self.audio_individual_data[effect_id] = AudioIndividual(result_data, sound_channles, sta_frame, end_frame)

    def del_audio_individual_data(self, effect_id):
        del self.audio_individual_data[effect_id]

    def addition_process(self):

        self.combined = np.full(self.combined_size, 0, dtype=np.int16)

        audio_individual_data_values = list(self.audio_individual_data.values())
        for v in audio_individual_data_values:
            ss = v.sta_frame * self.one_fps_samplingsize * v.sound_channles
            es = v.end_frame * self.one_fps_samplingsize * v.sound_channles
            vss = 0
            ves = (v.end_frame - v.sta_frame) * self.one_fps_samplingsize * v.sound_channles
            print("v.audio_data", v.audio_data)
            self.combined[ss:es] = v.audio_data[vss:ves]

    def upsampling(self, add_import_data, add_conversion_rate, after_conversion_rate=None):

        print("add_import_data.dtype", add_import_data.dtype)

        if after_conversion_rate is None:
            after_conversion_rate = self.criterion_conversion_rate

        convert_rate = round(after_conversion_rate / add_conversion_rate)  # 1以上の値にならないといけない
        interpolation_sample_num = convert_rate - 1  # -1をしているのは

        nyqF = (add_conversion_rate*convert_rate)/2.0     # 変換後のナイキスト周波数
        cF = (add_conversion_rate/2.0-500.)/nyqF             # カットオフ周波数を設定（変換前のナイキスト周波数より少し下を設定）
        taps = 511                          # フィルタ係数（奇数じゃないとだめ）
        b = signal.firwin(taps, cF)   # LPFを用意

        #after_convert_len = round(convert_rate*add_conversion_rate)

        print("/   ")
        print(" interpolation_sample_num", interpolation_sample_num)
        print(" add_import_data[len]", len(add_import_data))
        print(" after_conversion_rate", after_conversion_rate)
        print(" add_conversion_rate", add_conversion_rate)
        print(" convert_rate", convert_rate)
        #print(" after_convert_len", after_convert_len)
        print("   /")

        principal_len = len(add_import_data)
        shape_size = principal_len * convert_rate

        pattern = convert_rate  # パターン等間隔設定

        base = np.full(shape_size, 0)
        base[::pattern] = add_import_data

        result_data = signal.lfilter(b, 1, base)
        return result_data

    def downsampling(self, add_import_data, add_conversion_rate):
        convert_rate = round(self.criterion_conversion_rate / add_conversion_rate)  # 1以上の値にならないといけない
        interpolation_sample_num = convert_rate - 1  # -1をしているのは

        nyqF = (add_conversion_rate*convert_rate)/2.0     # 変換後のナイキスト周波数
        cF = (add_conversion_rate/2.0-500.)/nyqF             # カットオフ周波数を設定（変換前のナイキスト周波数より少し下を設定）
        taps = 511                          # フィルタ係数（奇数じゃないとだめ）
        b = signal.firwin(taps, cF)   # LPFを用意

        result_data = signal.lfilter(b, 1, add_import_data)
        pattern = -1 * convert_rate  # 削除パターン生成
        new_base = np.delete(result_data, pattern, 0)

        return new_base

    def sound_stop(self):
        sounddevice.stop()

    def sound_run(self):
        sounddevice.play(self.combined, self.criterion_conversion_rate)

# https://qiita.com/sumita_v09/items/808a3f8506065639cf51
