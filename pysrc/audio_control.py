import wave
import sounddevice
import scipy
import numpy as np
import_data = {}


class CentralRole:
    def __init__(self):
        self.fps = 0
        self.criterion_conversion_rate = 0
        self.criterion_sound_channles = 0

    def main(self, fps, criterion_conversion_rate, criterion_sound_channles):
        self.fps = fps
        self.criterion_conversion_rate = criterion_conversion_rate
        self.criterion_sound_channles = criterion_sound_channles

    def add(self, add_import_data, add_conversion_rate, sound_channles):

        result_data = None

        if add_conversion_rate < self.criterion_conversion_rate:
            result_data = self.upsampling(add_conversion_rate)

        if add_conversion_rate > self.criterion_conversion_rate:
            result_data = self.downsampling(add_conversion_rate)

        if add_conversion_rate == self.criterion_conversion_rate:
            result_data = add_conversion_rate

    def upsampling(self, add_conversion_rate):
        convert_rate = self.criterion_conversion_rate / add_conversion_rate  # 1以上の値にならないといけない
        interpolation_sample_num = convert_rate - 1  # -1をしているのは

        nyqF = (add_conversion_rate*convert_rate)/2.0     # 変換後のナイキスト周波数
        cF = (add_conversion_rate/2.0-500.)/nyqF             # カットオフ周波数を設定（変換前のナイキスト周波数より少し下を設定）
        taps = 511                          # フィルタ係数（奇数じゃないとだめ）
        b = scipy.signal.firwin(taps, cF)   # LPFを用意

        after_convert_len = convert_rate*add_conversion_rate
        base = np.full((after_convert_len), 255)
        base[::interpolation_sample_num] = after_convert_len

        result_data = scipy.signal.lfilter(b, 1, base)
        return result_data

    def downsampling(self, add_conversion_rate):
        pass

    def sound_stop(self):
        sounddevice.stop()

    def sound(self, ):
        sounddevice.play()

# https://qiita.com/sumita_v09/items/808a3f8506065639cf51
