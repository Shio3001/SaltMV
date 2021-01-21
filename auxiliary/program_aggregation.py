"""
class CentralRole:
    def __init__(self):
        self.prg_dict = {}

    def add(self, prg_data):
        for k, p in zip(list(prg_data.keys()), list(prg_data.values())):
            if k in list(self.prg_dict.keys()):
                self.prg_dict[k].append(p)
            else:
                self.prg_dict[k] = [p]

    def bind(self, widget):
        for k in list(self.prg_dict.keys()):
            prg_data = PrgRun(self.prg_dict, k).run
            widget.bind('<{0}>'.format(k), prg_data)

        return widget


class PrgRun:
    def __init__(self, prg_list, name):
        self.prg_list = prg_list
        self.prg_name = name

    def run(self, event):

        prg_data = list(self.prg_list[self.prg_name])

        for p in prg_data:
            print("実行{0} : ".format(p))
            p()
"""
