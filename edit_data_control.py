import elements
import copy
import json
import pickle
import base64
import os


class Storage:
    def __init__(self):
        self.edit_data = elements.AllElements()
        self.extension = ".json"
        self.operation = None
        self.now_scene = 0
        self.elements = elements
        self.app_name = "NankokuMovieMaker"
        self.response = ["exit", "problem", "no_problem"]  # 応答リスト

        this_os = str(os.name)  # windowsか判定
        if this_os == "nt":
            self.slash = "\\"
        else:
            self.slash = "/"

        print("総合データ管理場所作成")

    def set_operation(self, send_operation):
        self.operation = send_operation

    def get(self):
        return self.edit_data

    def set(self, send):
        self.edit_data = send
        return

    def file_input(self, user_select, file_name):

        file_name = self.extension_detection(file_name)

        try:
            lordfile = open(file_name, 'rb')
            self.edit_data = pickle.load(lordfile)
            save_path = copy.deepcopy(file_name)

            self.operation["log"].write("編集ファイルを開きました ファイルパス{0}".format(save_path))

        except:
            # print("ファイルが存在しませんでした")
            self.operation["log"].write("編集ファイルが存在しませんでした")
            save_path = ""

        return save_path

        # return all_elements, save_location

    def file_output(self, user_select):
        openfile = open(user_select, 'wb')
        pickle.dump(self.edit_data, openfile, protocol=5)
        openfile.close()

        save_location = copy.deepcopy(user_select)

        return save_location

    def extension_detection(self, file_name):
        extension_len = int(len(self.extension)) * -1
        if file_name[extension_len:] != self.extension:
            file_name += self.extension

        return file_name
