# coding:utf-8
import sys
import numpy as np
import os
import copy

import cv2


class CentralRole:
    def __init__(self):
        pass

    def type_video(self, all_elements, operation_list, user_select):  # 動画で出力

        if user_select[-4:] != ".mp4":
            user_select += ".mp4"

        editor = all_elements.editor_info

        export_draw = np.zeros((editor[1], editor[0], 4))  # numpyって指定する時縦横逆なんだな、めんどくさい #真っ黒な画面を生成

        fmt = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # ファイル形式(ここではmp4)
        size = (editor[0], editor[1])
        writer = cv2.VideoWriter(user_select, fmt, editor[2], size)  # ライター作成

        for now_frame in range(editor[3]):
            export_draw = operation_list["out"]["frame_process"]["CentralRole"].main(export_draw, all_elements, now_frame, operation_list)
            output_data = cv2.cvtColor(export_draw.astype('uint8'), cv2.COLOR_RGBA2BGR)
            writer.write(output_data)
            print(str(now_frame) + "番目のフレームの出力")

        writer.release()

    def type_image(self, all_elements, operation_list, select_time, user_select):  # 画像で出力
        pass
