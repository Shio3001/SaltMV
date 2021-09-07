# coding:utf-8
import sys
import os
import copy

import cv2
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

        def send_open(editor_func_send):
            editor_func_name, editor_func_val = editor_func_send
            print("send_open", editor_func_send)
            self.data.all_data.file_input(editor_func_val)

        def send_save(editor_func_send):
            editor_func_name, editor_func_val = editor_func_send
            print("send_save", editor_func_send)
            self.data.all_data.file_output(editor_func_val)

        def project_open():
            self.data.all_data.callback_operation.set_event("text_input_end", send_open, duplicate=False)
            self.data.all_data.callback_operation.event("set_init_val", info="")
            self.data.all_data.callback_operation.event("text_input_request", info="ファイルを入力")

            # self.data.all_data.add_layer_elements()

        def project_save():
            self.data.all_data.callback_operation.set_event("text_input_end", send_save, duplicate=False)
            self.data.all_data.callback_operation.event("set_init_val", info="")
            self.data.all_data.callback_operation.event("text_input_request", info="保存先を入力")

        def project_overwrite_save():
            pass

        preview_screen = self.data.new_parts("gui_main", "view", parts_name="pillow_view")
        preview_screen.size_update(640, 360)

        def preview_setup():
            self.operation["rendering_py"]["main"].set(self.operation, self.data.all_data.scene, self.data.all_data.media_object_group)

            scene_id = self.data.all_data.scene_id()
            print("preview_setup", scene_id)
            self.make_preview_data = self.operation["rendering_py"]["main"].make(scene_id, "../log/test.mp4")

        self.data.all_data.callback_operation.set_event("preview_setup", preview_setup)

        preview_setup()

        def preview(preview_frmae_run):
            #frame, run=False

            frame, run = None, None

            print(type(preview_frmae_run), preview_frmae_run)

            if type(preview_frmae_run) is tuple:
                frame, run = preview_frmae_run

            elif type(preview_frmae_run) is int:
                frame = preview_frmae_run

            self.make_preview_data.re_scene()
            self.make_preview_data.output_tk(frame, run=run)
            self.preview_image_tk = self.make_preview_data.get_image_tk(frame)

            print("preview", frame, self.make_preview_data.preview)

            if self.make_preview_data.preview == "opencv":
                return self.preview_image_tk

            #     print("opencv描画モード")
            #     cv2.imshow('opencv preview', self.preview_image_tk)  # この時点ではウィンドウは表示されない
            #     cv2.waitKey(0)
            #     return

            preview_screen.view(self.preview_image_tk)

        def cash_clear():
            self.make_preview_data.image_stack()

        self.data.all_data.callback_operation.set_event("preview", preview)
        #self.data.all_data.callback_operation.set_event("make_preview_data", get_make_preview_data)

        def send_rendering(editor_func_send):
            editor_func_name, editor_func_val = editor_func_send
            scene_id = self.data.all_data.scene_id()
            make_data = self.operation["rendering_py"]["main"].make(scene_id, editor_func_val)
            make_data.output_main()

        def rendering():
            self.data.all_data.callback_operation.set_event("text_input_end", send_rendering, duplicate=False)
            self.data.all_data.callback_operation.event("set_init_val", info="")
            self.data.all_data.callback_operation.event("text_input_request", info="保存先を入力")

            # make_data.output_OpenCV()

        def send_section_rendering(editor_func_send):
            editor_func_name, editor_func_val = editor_func_send
            scene_id = self.data.all_data.scene_id()
            make_data = self.operation["rendering_py"]["main"].make(scene_id, editor_func_val)

            return_val_dict = self.data.all_data.callback_operation.event("get_timelime_scroll_status")
            scrollbar_sta_end = return_val_dict["get_timelime_scroll_status"]

            sta = scrollbar_sta_end[0]
            end = scrollbar_sta_end[1]

            #print("scroll_data.ratio_f", scroll_data.ratio_f)

            make_data.output_main(sta, end)
            # make_data.output_OpenCV()

        def section_rendering():
            self.data.all_data.callback_operation.set_event("text_input_end", send_section_rendering, duplicate=False)
            self.data.all_data.callback_operation.event("set_init_val", info="")
            self.data.all_data.callback_operation.event("text_input_request", info="保存先を入力")

        def edit_data_del():
            self.data.all_data.callback_operation.event("reset")

        self.menubar = self.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.data.window)
        main_menubar_list = [("ファイル", "終了", self.data.window_exit, "新規作成", edit_data_del, "開く", project_open, "保存", project_save, "上書き", project_overwrite_save, "書き出し", rendering, "表示区間の書き出し", section_rendering, "キャッシュクリア", cash_clear)]
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
