import copy


class CentralRole:
    def __init__(self):
        self.prg_dict = {}

    def add(self, prg_data):
        for k, p in zip(list(prg_data.keys()), list(prg_data.values())):

            print("追加データ", p)

            if k in list(self.prg_dict.keys()):
                self.prg_dict[k].append(p)
                print("追加")
            else:
                self.prg_dict[k] = [p]
                print("新規追加")

        # self.prg_dict.update(prg_data)
        print("登録済み : {0} ".format(self.prg_dict))
        print("処理数　 : {0} ".format(len(self.prg_dict)))

    def run(self, name):
        prg_run_data = PrgRun(self.prg_dict, name).run
        return prg_run_data

    def bind(self, widget):
        for k, p_list in zip(list(self.prg_dict.keys()), list(self.prg_dict.values())):
            prg_data = self.run(k)
            widget.bind('<{0}>'.format(k), prg_data)

        return widget


class PrgRun:
    def __init__(self, prg_list, name):
        self.prg_list = prg_list
        self.prg_name = name

    def run(self, event):
        print("実行総合受付")

        prg_data = list(self.prg_list[self.prg_name])

        for p in prg_data:
            print("実行{0} : ".format(p))
            p()
