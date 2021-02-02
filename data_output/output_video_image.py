# coding:utf-8
import sys
import numpy as np
import os
import copy
from PIL import Image, ImageTk
import cv2

import time


class CentralRole:
    def __init__(self):
        self.preview_memory_tk = {}

    def type_video(self, send_all_elements, operation_list, user_select):  # 動画で出力
        all_elements = copy.deepcopy(send_all_elements)
        # 読み取り専用、all_elementsに変更を加えてもいいが元のやつには反映されない
        if user_select[-4:] != ".mp4":
            user_select += ".mp4"

        editor = all_elements.editor_info

        print(editor)

        if not editor or 0 in editor:
            print("画面サイズなどがきちんと設定されていないため動画を出力できません")
            return

        export_draw_base = np.zeros((editor[1], editor[0], 4))  # numpyって指定する時縦横逆なんだな、めんどくさい #真っ黒な画面を生成

        fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)
        size = (editor[0], editor[1])
        writer = cv2.VideoWriter(user_select, fmt, editor[2], size)  # ライター作成
        print("書き出し開始")
        start_time = time.time()

        all_elements = self.get_media(all_elements)
        for now_frame in range(editor[3]):
            print("\r進捗: {0} / {1} 進捗率: {2} %".format(now_frame + 1, editor[3], round(((now_frame + 1) / editor[3]) * 100)), end='')

            export_draw = operation_list["out"]["frame_process"]["CentralRole"].main(export_draw_base, all_elements, now_frame, operation_list, editor)
            output_data = cv2.cvtColor(export_draw.astype('uint8'), cv2.COLOR_RGBA2BGR)
            writer.write(output_data)

        print("")
        print("書き出し終了")
        print("")
        elapsed_time = time.time() - start_time
        print("処理時間 : " + str(elapsed_time) + "秒")
        print("1フレームあたり平均処理時間" + str(elapsed_time / editor[3]) + "秒")
        print("{0}fps 1フレーム{1}".format(editor[2], 1 / editor[2]))
        print("")

        writer.release()

        return

    def type_image(self, send_all_elements, operation_list, select_time, user_select):  # 画像で出力
        all_elements = copy.deepcopy(send_all_elements)
        if user_select[-4:] != ".png":
            user_select += ".png"

        editor = all_elements.editor_info
        if not editor or 0 in editor:
            print("画面サイズなどがきちんと設定されていないため動画を出力できません")
            return

        export_draw_base = np.zeros((editor[1], editor[0], 4))  # numpyって指定する時縦横逆なんだな、めんどくさい #真っ黒な画面を生成

        start_time = time.time()

        all_elements = self.get_media(all_elements)
        export_draw = operation_list["out"]["frame_process"]["CentralRole"].main(export_draw_base, all_elements, int(select_time), operation_list, editor)
        output_data = cv2.cvtColor(export_draw.astype('uint8'), cv2.COLOR_RGBA2BGR)

        cv2.imwrite(user_select, output_data)

        elapsed_time = time.time() - start_time
        print("処理時間 : " + str(elapsed_time) + "秒")

        return

    def edit_changed(self, editing_range=None):  # 配列での範囲指定
        if editing_range is None:
            self.preview_memory_tk = {}
            return

        self.preview_memory_tk = {k: v for k, v in zip(self.preview_memory_tk.keys(), self.preview_memory_tk.values()) if not k in range(editing_range)}

        #del self.preview_memory_tk[editing_range_list]

    def type_preview(self, send_all_elements, operation_list, select_time, canvas_size):  # プレビュー出力
        all_elements = copy.deepcopy(send_all_elements)
        t = select_time

        if not self.preview_memory_tk[t] is None:
            return self.preview_memory_tk[t]

        editor = all_elements.editor_info

        # export_size = [canvas_size

        export_draw_base = np.zeros((editor[1], editor[0], 4))  # numpyって指定する時縦横逆なんだな、めんどくさい #真っ黒な画面を生成
        all_elements = self.get_media(all_elements)
        start_time = time.time()

        resize_position = window_size
        export_draw = operation_list["out"]["frame_process"]["CentralRole"].main(export_draw_base, all_elements, int(t), operation_list, editor)
        image_cv = cv2.resize(export_draw, (resize_position))
        image_cv_RGB = cv2.cvtColor(image_cv.astype('uint8'), cv2.COLOR_BGRA2RGB)
        image_pil = Image.fromarray(image_cv_RGB)  # RGBからPILフォーマットへ変換
        image_tk = ImageTk.PhotoImage(image_pil)  # ImageTkフォーマットへ変換

        self.preview_memory_tk[t] = image_tk

        elapsed_time = time.time() - start_time
        print("処理時間 : " + str(elapsed_time) + "秒")

        return image_tk

    def get_media(self, all_elements):

        for i_layer, this_layer in enumerate(all_elements.layer_group):
            for i_object, this_object in enumerate(this_layer.retention_object):

                if this_object.objectType == "video":
                    new_video = ""
                    try:
                        new_video = cv2.VideoCapture(this_object.document)
                    except:
                        print("読み込みに失敗 try - except")

                    if new_video.isOpened() != True:
                        print("読み込みに失敗 isOpened")
                    else:
                        video_property = {"width": new_video.get(cv2.CAP_PROP_FRAME_WIDTH), "height": new_video.get(cv2.CAP_PROP_FRAME_HEIGHT), "fps": new_video.get(cv2.CAP_PROP_FPS), "count": new_video.get(cv2.CAP_PROP_FRAME_COUNT)}
                        all_elements.layer_group[i_layer].retention_object[i_object].unique_property = video_property

                    all_elements.layer_group[i_layer].retention_object[i_object].document = new_video

                if this_object.objectType == "image":
                    new_image = ""
                    try:
                        new_image = cv2.imread(this_object.document)
                    except:
                        print("読み込みに失敗 try - except")

                    if new_image is None:
                        print("読み込みに失敗 - is None")
                    else:
                        image_property = {"width": new_image.shape[1], "height": new_image.shape[0]}
                        all_elements.layer_group[i_layer].retention_object[i_object].unique_property = image_property

                    all_elements.layer_group[i_layer].retention_object[i_object].document = new_image

        return all_elements
