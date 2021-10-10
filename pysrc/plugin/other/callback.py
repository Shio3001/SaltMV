import copy
import inspect
import asyncio


class FunctionStorage:
    def __init__(self, func):
        self.func = func

    def run(self, info):
        return_val = self.func(info)
        return return_val

    def get(self):
        return self.func


class CallBackOne:
    def __init__(self):
        self.__event_data = None

    def set_event(self, func):
        self.__event_data = func

    def event(self, info=None):

        if not info is None:
            return_val = self.__event_data(info)
        else:
            return_val = self.__event_data()

        return return_val


class CallBack:
    def __init__(self):
        self.__event_data = {}

    def set_event(self, name, func, run=False, duplicate=True):

        if not name in self.__event_data.keys():
            self.__event_data[name] = []

        func_data = FunctionStorage(func)

        if duplicate:
            self.__event_data[name].append(func_data)  # 一度に複数の関数を実行できるようにするため
        else:
            self.__event_data[name] = []
            self.__event_data[name].append(func_data)

        if run:
            func(None)

        if name == "draw_func":
            print("呼び出し先[callback_set]", self.__event_data[name], inspect.stack()[1].filename, inspect.stack()[1].function, len(self.__event_data[name]))

        #print("呼び出し先[set_event]", inspect.stack()[1].filename, inspect.stack()[1].function, name, func, self.__event_data[name])

    def event(self, name, info=None):

        return_val_dict = {}

        if name == "draw_func" and name in list(self.__event_data.keys()):
            print("呼び出し先[callback]", self.__event_data[name], inspect.stack()[1].filename, inspect.stack()[1].function, len(self.__event_data[name]))

        if not name in self.__event_data.keys():
            print("返送", name)
            return

        # print("実行")

        for d in self.__event_data[name]:
            if str(type(d)) == "<class 'function'>":

                return_val = None

                if not info is None:
                    return_val = d.run(info)
                else:
                    return_val = d.run()

                func_name = d.func.__name__
                return_val_dict[func_name] = return_val

        return return_val_dict
        # print("実行")

    def get_event(self, name):
        return self.__event_data[name].get()

    def del_event(self, name, func=None):
        if not name in list(self.__event_data.keys()):
            # print("削除返却")
            return

        # print("削除通過")

        if not func is None:
            num = self.__event_data[name].index(func)

            #print("同値削除要請 ", func, num)

            if not num is None:
                del self.__event_data[name][num]
                #print("同値検知 削除", name, " ", num)

                return

        del self.__event_data[name]

    def all_del_event(self):
        self.__event_data = {}

    def all_get_event(self):
        return copy.deepcopy(self.__event_data)

        #data.set_event = set_event
        #data.event = event

        # data.set_event(data.event_not_func)
