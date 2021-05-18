class UIManagement:
    def __init__(self, data, ui_list):
        self.ui_list = ui_list
        self.data = data

    def element_del(self, sta=0, end=None):
        if end is None:
            end = int(len(self.ui_list))

        print(sta, end)

        for i in range(sta, end):
            #print(i, "削除")
            if not self.ui_list[i].te_name in self.ui_list[i].canvas_data.territory.keys():
                continue

            self.ui_list[i].del_territory()
        del self.ui_list[sta:end]

    def new_parameter_ui(self, now):
        if now >= int(len(self.ui_list)):
            ui_id = self.data.all_data.elements.make_id("parameter_UI")
            self.ui_list.append([None, None])
            self.ui_list[now] = self.data.new_parts("parameter", ui_id, parts_name="parameter")
