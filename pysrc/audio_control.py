import wave
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

        self.combined = np.full(1, 0, dtype=np.float32)

        self.setup_flag = False  # 流す準備ができているかどうか
        self.run_flag = False  # 現在流しているか

        #self.audio_data = 0

    def main(self, fps, frame_len, criterion_conversion_rate, criterion_sound_channles):
        print("     **********AudioControl main")

        self.fps = fps
        self.frame_len = frame_len
        self.criterion_conversion_rate = criterion_conversion_rate
        self.criterion_sound_channles = criterion_sound_channles

        self.one_fps_samplingsize = round(criterion_conversion_rate / fps)

        self.combined_size = frame_len * self.one_fps_samplingsize * self.criterion_sound_channles
        self.combined = np.full(self.combined_size, 0, dtype=np.float32)

    def add(self, effect_id, add_import_data, add_conversion_rate, sound_channles, sta_frame, end_frame):

        print("     **********AudioControl add", effect_id)

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

        self.audio_individual_data[effect_id] = AudioIndividual(result_data, sound_channles, sta_frame, end_frame, effect_id)

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

        self.combined = np.full(self.combined_size, 0, dtype=np.float32)

        audio_individual_data_values = list(self.audio_individual_data.values())
        for v in audio_individual_data_values:
            ss = v.sta_frame * self.one_fps_samplingsize * v.sound_channles
            es = v.end_frame * self.one_fps_samplingsize * v.sound_channles
            vss = 0
            ves = (v.end_frame - v.sta_frame) * self.one_fps_samplingsize * v.sound_channles
            print("v.audio_data", v.audio_data)
            print("ss, es, vss, ves", ss, es, vss, ves)
            self.combined[ss:es] += v.audio_data[vss:ves]

            print("combined", self.combined)
            print("self.combined[ss:es]", self.combined[ss:es])

        print("音源総和", np.sum(self.combined))

        self.setup_flag = True

    def upsampling(self, add_import_data, add_conversion_rate, after_conversion_rate=None):
        print("     **********AudioControl upsampling")

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
        print("     **********AudioControl downsampling")

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
        print("     **********AudioControl sound_stop")

        print("停止 sound_stop")

        self.run_flag = False
        sounddevice.stop()

    def sound_run(self, now_frame):
        print("     **********AudioControl sound_run")

        if not self.setup_flag or self.run_flag:
            return

        sound_channles = 1

        ss = now_frame * self.one_fps_samplingsize * sound_channles

        print("再生", self.combined[ss:-1], self.criterion_conversion_rate)

        sounddevice.play(self.combined[ss:-1], self.criterion_conversion_rate)

        self.run_flag = True

    def output_audio_file(self, path):
        print("     **********AudioControl output_audio_file")

        #librosa.output.write_wav(path,self.combined, self.criterion_conversion_rate)
        scipy_write(path, self.criterion_conversion_rate, self.combined)


# https://qiita.com/sumita_v09/items/808a3f8506065639cf51
