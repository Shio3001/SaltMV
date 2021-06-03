import time
import cv2
import numpy as np


class Rendering:
    def __init__(self):
        self.recoed_frame = {}
        self.recoed_media = {}
        self.all_data = None

    def set_all_data(self, all_data):
        self.all_data = all_data

    def video_output(self, operation, this_scene, path):
        operation["log"].stop(True)

        s, e = 0, this_scene.editor["len"]

        fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)
        size = (this_scene.editor["x"], this_scene.editor["y"])
        writer = cv2.VideoWriter(path, fmt, this_scene.editor["fps"], size)  # ライター作成
        start_time = time.time()

        for t in range(s, e):
            draw_base = np.zeros((this_scene.editor["y"], this_scene.editor["x"], 4))  # numpyって指定する時縦横逆なんだな、めんどくさい #真っ黒な画面を生成

            this_scene = self.get_media(this_scene)
            # for now_frame in range(this_scene.editor["len"]):
            print("\r進捗: {0} / {1} 進捗率: {2} %".format(t + 1, this_scene.editor["len"], round(((t + 1) / this_scene.editor["len"]) * 100)), end='')
            #operation["log"].write("進捗: {0} / {1} 進捗率: {2} %".format(t + 1, this_scene.editor["len"], round(((t + 1) / this_scene.editor["len"]) * 100)))

            export_draw = operation["rendering"]["frame"].main(self.all_data, draw_base, operation, this_scene, t)
            output_data = cv2.cvtColor(export_draw.astype('uint8'), cv2.COLOR_RGBA2BGR)
            writer.write(output_data)

        writer.release()

        print("書き出し終了")

        elapsed_time = time.time() - start_time
        operation["log"].write("**************************************")
        operation["log"].write("書き出し終了")
        operation["log"].write("")
        operation["log"].write("処理時間 : " + str(elapsed_time) + "秒")
        operation["log"].write("1フレームあたり平均処理時間" + str(elapsed_time / this_scene.editor["len"]) + "秒")
        operation["log"].write("{0}fps 1フレーム{1}".format(this_scene.editor["fps"], 1 / this_scene.editor["fps"]))
        operation["log"].write("処理数 {0}フレーム {1} から {2}".format(e - s, s, e))
        operation["log"].write("**************************************")

        return

        # for t in

    def image_output(self, this_scene, user_select_frame):
        pass

    def preview_output(self, this_scene, user_select_frame):
        pass

    def get_media(self, this_scene):
        return this_scene

    def media_record(self):
        pass

    def frame_record(self):
        pass

    def del_media_record(self):
        pass

    def del_frame_recoed(self):
        pass
