import copy


class UIManagement:
    def __init__(self, data):
        self.ui_list = []
        self.data = data

        self.old_elements_len = 0
        self.now_elements_len = 0

    def element_del(self, sta=0, end=None):  # UIパーツを削除する
        if end is None:
            end = int(len(self.ui_list))

        for i in range(sta, end):
            if not self.ui_list[i].te_name in self.ui_list[i].canvas_data.territory.keys():
                continue

            if self.data.operation["class_dict"](self.ui_list[i], inquiry="callback_operation"):
                self.ui_list[i].callback_operation.event("del_parameter_ui")

            self.ui_list[i].del_territory()

        del self.ui_list[sta:end]

    def new_parameter_ui(self, now, parts_name=None, canvas_name=None):  # UIパーツを追加する
        if now >= int(len(self.ui_list)):
            ui_id = self.data.edit_data_control.elements.make_id("parameter_UI")
            self.ui_list.append(None)
            self.ui_list[now] = self.data.new_parts(canvas_name, ui_id, parts_name=parts_name)

            #print("生成", now, "parts_name", parts_name, "canvas_name", canvas_name)

    def set_old_elements_len(self, set_number=None):
        if set_number is None:
            self.old_elements_len = int(len(self.ui_list))
        if not set_number is None:
            self.old_elements_len = copy.deepcopy(set_number)

    def set_now_elements_len(self, set_number=None):
        if set_number is None:
            self.old_elements_len = int(len(self.ui_list))
        if not set_number is None:
            self.old_elements_len = copy.deepcopy(set_number)

    def del_ignition(self, now):
        if self.old_elements_len > now:
            len_difference = copy.deepcopy(now)
            self.element_del(sta=len_difference)
