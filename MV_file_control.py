import ffmpeg
import cv2
import numpy as np
import librosa
import traceback


class videoDATA:
    def __init__(self, video, file_name, width, height, video_fps):
        self.video = video
        self.file_name = file_name
        self.width = width
        self.height = height
        self.video_fps = video_fps
        self.type = "video"

    def get(self, frame):
        return self.file_name[frame]


class imageDATA:
    def __init__(self, image, file_name):
        self.image = image
        self.file_name = file_name
        self.type = "image"

    def get(self):
        return self.iamge


class audioDATA:
    def __init__(self, audio, file_name, channel, frame, sampling_rate):
        self.audio = audio
        self.file_name = file_name
        self.channel = channel
        self.frame = frame
        self.sampling_rate = sampling_rate
        self.type = "audio"

    def get(self):
        pass


class SaltFile:
    def __init__(self):
        self.DATA = {}

    def __confirmation_key(self, file_name):  # 存在するかどうかを確認
        data_key = list(self.DATA.keys())

        ans = file_name in data_key

        return ans

    def input_video(self, file_name):

        ans = self.__confirmation_key(file_name)
        if ans:
            return

        try:
            video_info = ffmpeg.probe(self.file_name)
            width = round(video_info["streams"][0]["width"])
            height = round(video_info["streams"][0]["height"])
            video_fps = round(eval(video_info["streams"][0]["r_frame_rate"]))

            out, _ = (
                ffmpeg
                .input(file_name)
                .output('pipe:', format='rawvideo', pix_fmt='rgb24')
                .run(capture_stdout=True)
            )

            video_dataRGB = np.frombuffer(out, np.uint8).astype('uint8').reshape(-1, self.height, self.width, 3)
            video_dataRGBA = cv2.cvtColor(video_dataRGB, cv2.COLOR_RGB2RGBA)

            video_data_class = videoDATA(video_dataRGBA, file_name, width, height, video_fps)

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

    def get_data(self, file_name):
        return self.DATA[file_name]

    def get_video(self, file_name, frame):
        return self.DATA[file_name].video[frame]

    def get_image(self, file_name):
        return self.DATA[file_name].image

    def get_audio(self, file_name):
        return self.DATA[file_name].audio
