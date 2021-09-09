import wave
import sounddevice
import scipy
import numpy as np


class AudioControl:
    def __init__(self):
        self.fps = 0
        self.criterion_conversion_rate = 0
        self.criterion_sound_channles = 0

    def main(self, fps, criterion_conversion_rate, criterion_sound_channles):
        self.fps = fps
        self.criterion_conversion_rate = criterion_conversion_rate
        self.criterion_sound_channles = criterion_sound_channles

    def add(self, add_import_data: np.numarray, add_conversion_rate, sound_channles, start_frame):

        result_data = None

        if add_conversion_rate < self.criterion_conversion_rate:
            result_data = self.upsampling(add_import_data, add_conversion_rate)
            print("<")

        if add_conversion_rate > self.criterion_conversion_rate:
            result_data = self.downsampling(add_import_data, add_conversion_rate)
            print(">")

        if add_conversion_rate == self.criterion_conversion_rate:
            result_data = add_import_data
            print("=")

        print(result_data)

    def upsampling(self, add_import_data, add_conversion_rate):
        convert_rate = round(self.criterion_conversion_rate / add_conversion_rate)  # 1以上の値にならないといけない
        interpolation_sample_num = convert_rate - 1  # -1をしているのは

        nyqF = (add_conversion_rate*convert_rate)/2.0     # 変換後のナイキスト周波数
        cF = (add_conversion_rate/2.0-500.)/nyqF             # カットオフ周波数を設定（変換前のナイキスト周波数より少し下を設定）
        taps = 511                          # フィルタ係数（奇数じゃないとだめ）
        b = scipy.signal.firwin(taps, cF)   # LPFを用意

        after_convert_len = round(convert_rate*add_conversion_rate)

        print("/   ")
        print("interpolation_sample_num", interpolation_sample_num)
        print("add_import_data[len]", len(add_import_data))
        print("criterion_conversion_rate", self.criterion_conversion_rate)
        print("add_conversion_rate", add_conversion_rate)
        print("after_convert_len", after_convert_len)
        print("   /")

        base = np.full(after_convert_len, 0)
        base[::interpolation_sample_num] = add_import_data

        result_data = scipy.signal.lfilter(b, 1, base)
        return result_data

    def downsampling(self, add_import_data, add_conversion_rate):
        pass

    def sound_stop(self):
        sounddevice.stop()

    def sound(self, ):
        sounddevice.play()

# https://qiita.com/sumita_v09/items/808a3f8506065639cf51
