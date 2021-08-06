# coding:utf-8
import sys
import os
import copy

#import cv2
#from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont


class InitialValue:
    def __init__(self, data):
        self.data = data
        self.operation = self.data.operation
        #self.all_elements = self.data.all_elements
        #self.elements = self.data.elements
        self.tk = self.data.tk

        self.UI_parts = self.data.UI_parts  # パーツひとつひとつのデータ

        self.preview_image_tk = None
        # self.UI_operation = self.data.UI_operation  # パーツを整形するためのデータ

    def main(self):

        self.data.new_canvas("gui_main")
        self.data.edit_canvas_size("gui_main", x=640, y=360)
        self.data.edit_canvas_position("gui_main", x=0, y=0)

        self.operation["log"].write("メイン画面起動")

        """
        def get_edit():
            return self.all_elements  # データおくる

        def set_edit(send_all_elements):
            self.all_elements = send_all_elements  # データもら
            return
        """

        def project_new():
            pass

        def project_open():
            self.data.all_data.file_input(self.data.all_data.input_debug("open"))
            # self.data.all_data.add_layer_elements()

        def project_save():
            self.data.all_data.file_output(self.data.all_data.input_debug("close"))

        def project_overwrite_save():
            pass
        preview_screen = self.data.new_parts("gui_main", "tk_image", parts_name="pillow_view")
        preview_screen.size_update(640, 360)
        scene_id = self.data.all_data.scene_id()

        def preview(frame):
            make_preview_data = self.operation["rendering_py"]["main"].make(scene_id, "../log/test.mp4")
            make_preview_data.output_tk(frame)
            self.preview_image_tk = make_preview_data.get_image_tk(frame)
            preview_screen.view(self.preview_image_tk)

        self.data.all_data.callback_operation.set_event("preview", preview)

        def rendering():
            scene_id = self.data.all_data.scene_id()
            # self.operation["rendering_py"]["main"].setapp_init(self.operation,scene)

            #scene_elements.user_select_range = [0, 100]
            make_data = self.operation["rendering_py"]["main"].make(scene_id, "../log/test.mp4")
            make_data.output_main()
            # make_data.output_OpenCV()

        def edit_data_del():
            self.data.all_data.callback_operation.event("reset")

        self.menubar = self.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.data.window)
        main_menubar_list = [("ファイル", "終了", self.data.window_exit, "新規作成", edit_data_del, "開く", project_open, "保存", project_save, "上書き", project_overwrite_save, "書き出し", rendering)]
        self.menubar.set(main_menubar_list)

        display_size = self.data.display_size_get()
        self.data.window_title_set("メインウインドウ")
        #size = [640, 360]
        self.data.window_size_set(x=640, y=360)

        # def window_size_change_event(self):
        #    pass

        #self.data.window_event(processing=window_size_change_event, user_event="Motion")

        return self.data

        # self.data.all_data.add_layer_elements()
