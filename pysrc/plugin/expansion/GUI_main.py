# coding:utf-8
import sys
import os
import copy

import cv2
# from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont


class InitialValue:
    def __init__(self, data):
        self.window_control = data
        self.operation = self.window_control.operation
        # self.all_elements = self.window_control.all_elements
        # self.elements = self.window_control.elements
        self.tk = self.window_control.tk

        self.UI_parts = self.window_control.UI_parts  # パーツひとつひとつのデータ

        self.preview_image_tk = None

        self.save_path = None
        # self.UI_operation = self.window_control.UI_operation  # パーツを整形するためのデータ

    def main(self):

        self.window_control.new_canvas("gui_main")
        self.window_control.edit_canvas_size("gui_main", x=640, y=360)
        self.window_control.edit_canvas_position("gui_main", x=0, y=0)

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
            self.save_path = self.window_control.edit_control_auxiliary.file_input(editor_func_val)

        def send_save(editor_func_send):
            editor_func_name, editor_func_val = editor_func_send
            print("send_save", editor_func_send)
            self.save_path = self.window_control.edit_control_auxiliary.file_output(editor_func_val)

        def project_open():
            self.window_control.edit_control_auxiliary.callback_operation.set_event("text_input_end", send_open, duplicate=False)
            self.window_control.edit_control_auxiliary.callback_operation.event("set_init_val", info="")
            self.window_control.edit_control_auxiliary.callback_operation.event("text_input_request", info="ファイルを入力")

            # self.window_control.edit_control_auxiliary.add_layer_elements()

        def project_save():
            self.window_control.edit_control_auxiliary.callback_operation.set_event("text_input_end", send_save, duplicate=False)
            self.window_control.edit_control_auxiliary.callback_operation.event("set_init_val", info="")
            self.window_control.edit_control_auxiliary.callback_operation.event("text_input_request", info="保存先を入力")

        def project_overwrite_save():
            print("send_save")
            if not self.save_path is None:
                self.window_control.edit_control_auxiliary.file_output(self.save_path)
            else:
                project_save()

        preview_screen = self.window_control.new_parts("gui_main", "view", parts_name="pillow_view")
        preview_screen.size_update(640, 360)

        def preview_setup():
            self.operation["rendering_py"]["main"].set(self.operation, self.window_control.edit_control_auxiliary.scene, self.window_control.edit_control_auxiliary.media_object_group)

            scene_id = self.window_control.edit_control_auxiliary.scene_id()
            print("preview_setup", scene_id)
            self.make_preview_data = self.operation["rendering_py"]["main"].make(scene_id, "../log/test.mp4")

        self.window_control.edit_control_auxiliary.callback_operation.set_event("preview_setup", preview_setup)

        preview_setup()

        def sound_init():
            self.make_preview_data.sound_init()

        def sound_stop():
            self.make_preview_data.sound_stop()

        # def preview

        def preview_reflect():
            self.make_preview_data.re_scene()

        def preview(preview_frmae_run):
            # frame, run=False

            frame, run = None, None

            print(type(preview_frmae_run), preview_frmae_run)

            if type(preview_frmae_run) is tuple:
                frame, run = preview_frmae_run

            elif type(preview_frmae_run) is int:
                frame = preview_frmae_run

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
            self.window_control.edit_control_auxiliary.callback_operation.event("preview_reflect")

        self.window_control.edit_control_auxiliary.callback_operation.set_event("preview_reflect", preview_reflect)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("preview", preview)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("sound_init", sound_init)
        self.window_control.edit_control_auxiliary.callback_operation.set_event("sound_stop", sound_stop)
        # self.window_control.edit_control_auxiliary.callback_operation.set_event("make_preview_data", get_make_preview_data)

        def send_rendering(editor_func_send):
            editor_func_name, editor_func_val = editor_func_send
            scene_id = self.window_control.edit_control_auxiliary.scene_id()
            make_data = self.operation["rendering_py"]["main"].make(scene_id, editor_func_val)
            make_data.output_main()

        def rendering():
            self.window_control.edit_control_auxiliary.callback_operation.set_event("text_input_end", send_rendering, duplicate=False)
            self.window_control.edit_control_auxiliary.callback_operation.event("set_init_val", info="")
            self.window_control.edit_control_auxiliary.callback_operation.event("text_input_request", info="保存先を入力")

            # make_data.output_OpenCV()

        def send_section_rendering(editor_func_send):
            editor_func_name, editor_func_val = editor_func_send
            scene_id = self.window_control.edit_control_auxiliary.scene_id()
            make_data = self.operation["rendering_py"]["main"].make(scene_id, editor_func_val)

            return_val_dict = self.window_control.edit_control_auxiliary.callback_operation.event("get_timelime_scroll_status")
            scrollbar_sta_end = return_val_dict["get_timelime_scroll_status"]

            sta = scrollbar_sta_end[0]
            end = scrollbar_sta_end[1]

            # print("scroll_data.ratio_f", scroll_data.ratio_f)

            make_data.output_main(sta, end)
            # make_data.output_OpenCV()

        def section_rendering():
            self.window_control.edit_control_auxiliary.callback_operation.set_event("text_input_end", send_section_rendering, duplicate=False)
            self.window_control.edit_control_auxiliary.callback_operation.event("set_init_val", info="")
            self.window_control.edit_control_auxiliary.callback_operation.event("text_input_request", info="保存先を入力")

        def edit_data_del():
            self.window_control.edit_control_auxiliary.callback_operation.event("reset")

        self.menubar = self.operation["plugin"]["other"]["menu_popup"].MenuPopup(self.window_control.window)
        main_menubar_list = [("ファイル", "終了", self.window_control.window_exit, "新規作成", edit_data_del, "開く", project_open, "保存", project_save, "上書き", project_overwrite_save, "書き出し", rendering, "表示区間の書き出し", section_rendering, "キャッシュクリア", cash_clear)]
        self.menubar.set(main_menubar_list)

        display_size = self.window_control.display_size_get()
        self.window_control.window_title_set("メインウインドウ")
        # size = [640, 360]
        self.window_control.window_size_set(x=640, y=360)

        # def window_size_change_event(self):
        #    pass

        # self.window_control.window_event(processing=window_size_change_event, user_event="Motion")

        return self.window_control

        # self.window_control.edit_control_auxiliary.add_layer_elements()
