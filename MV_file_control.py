import ffmpeg
import cv2
import numpy as np
import librosa
import traceback
import copy
import sys


class videoDATA:
    def __init__(self, cap, file_name, width, height, video_fps, video_frame):
        self.cap = cap
        self.video = [None] * video_frame
        self.file_name = copy.deepcopy(file_name)
        self.width = copy.deepcopy(width)
        self.height = copy.deepcopy(height)
        self.video_fps = copy.deepcopy(video_fps)
        self.video_frame = copy.deepcopy(video_frame)
        self.type = "video"

        print("videoDATA", self.file_name)

        sys.exit()

    def data_get(self, frame):

        if self.video_frame <= frame:
            frame = self.video_frame - 1

        print(len(self.video[frame]), frame)

        if self.video[frame] is None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ret, video_dataBGR = self.cap.read()
            print("ret", ret)
            self.video[frame] = cv2.cvtColor(video_dataBGR.astype('uint8'), cv2.COLOR_BGR2RGBA)

        return self.video[frame]


class imageDATA:
    def __init__(self, image, file_name):
        self.image = copy.deepcopy(image)
        self.file_name = copy.deepcopy(file_name)
        self.type = "image"

    def data_get(self):
        return self.iamge


class audioDATA:
    def __init__(self, audio, file_name, channel, frame, sampling_rate):
        self.audio = copy.deepcopy(audio)
        self.file_name = copy.deepcopy(file_name)
        self.channel = copy.deepcopy(channel)
        self.frame = copy.deepcopy(frame)
        self.sampling_rate = copy.deepcopy(sampling_rate)
        self.type = "audio"

    def data_get(self):
        pass


class SaltFile:
    def __init__(self):
        self.DATA = {}

    def __confirmation_key(self, file_name):  # 存在するかどうかを確認
        data_key = self.DATA.keys()

        ans = file_name in data_key

        return ans

    def analysis(self, scenes):
        object_group = scenes.layer_group.object_group
        object_group_key = object_group.keys()
        object_group_val = object_group.values()

        for ogi in object_group_val:
            effect_group = ogi[0].effect_group

            effect_group_key = effect_group.keys()
            effect_group_val = effect_group.values()

            for egi in effect_group_val:
                various_fixed = egi.various_fixed
                path_type = egi.path_type

                path_type_key = list(path_type.keys())
                path_type_val = list(path_type.values())
                path_type_len = len(path_type)

                for pti in range(path_type_len):
                    ptk = path_type_key[pti]
                    ptv = path_type_val[pti]

                    vff = various_fixed[ptk]

                    if ptv == "video":
                        self.input_video(vff)

                    if ptv == "image":
                        self.input_image(vff)

                    if ptv == "audio":
                        self.input_audio(vff)

    def input_video(self, file_name):

        ans = self.__confirmation_key(file_name)
        if ans:
            return

        try:
            # video_info = ffmpeg.probe(file_name)
            # width = round(video_info["streams"][0]["width"])
            # height = round(video_info["streams"][0]["height"])
            # video_fps = round(eval(video_info["streams"][0]["r_frame_rate"]))

            cap = cv2.VideoCapture(file_name)

            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            video_fps = cap.get(cv2.CAP_PROP_FPS)
            video_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            print("RGB変換終了", width, height, video_fps, video_frame)

            video_data_class = videoDATA(cap, file_name, width, height, video_fps, video_frame)

            self.DATA[file_name] = video_data_class

        except:
            traceback.print_exc()

    def input_image(self, file_name):

        ans = self.__confirmation_key(file_name)
        if ans:
            return

        try:
            image_dataBGR = cv2.imread(file_name)
            video_dataRGBA = cv2.cvtColor(image_dataBGR, cv2.COLOR_BGR2RGBA)

            image_data_class = imageDATA(video_dataRGBA, file_name)

            self.DATA[file_name] = image_data_class

        except:
            traceback.print_exc()

    def input_audio(self, file_name):
        ans = self.__confirmation_key(file_name)
        if ans:
            return

        try:
            import_data, sr = librosa.load(file_name, sr=44100, mono=False)  # , mono=False

            data_shape = import_data.shape

            print(len(data_shape))

            sound_channles = 0
            sound_frame = 0
            sound_sampling_rate = 44100

            if len(data_shape) == 1:
                sound_channles = 1
                sound_frame = import_data.shape[0]
            else:
                sound_channles = import_data.shape[0]
                sound_frame = import_data.shape[1]

            audio_data_class = audioDATA(import_data, file_name, sound_channles, sound_frame, sound_sampling_rate)

            self.DATA[file_name] = audio_data_class
        except:
            traceback.print_exc()

    def get_bool(self, file_name):
        return self.__confirmation_key(file_name)

    def get_data(self, file_name):
        return self.DATA[file_name]

    def get_video(self, file_name, frame):

        frame = int(frame)

        print("フレーム要求", frame)

        return_data = self.DATA[file_name].data_get(frame)

        return return_data

    def get_image(self, file_name):
        return self.DATA[file_name].image

    def get_audio(self, file_name):
        return self.DATA[file_name].audio
