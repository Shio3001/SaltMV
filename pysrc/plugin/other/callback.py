import copy
import inspect
import asyncio


class FunctionStorage:
    def __init__(self, func):
        self.func = func

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

        print("呼び出し先[callback_set]", name, self.__event_data[name], inspect.stack()[1].filename, inspect.stack()[1].function, len(self.__event_data[name]))

        #print("呼び出し先[set_event]", inspect.stack()[1].filename, inspect.stack()[1].function, name, func, self.__event_data[name])

    def event(self, name, info=None):

        return_val_dict = {}

        if name in list(self.__event_data.keys()):
            print("呼び出し先[callback]", self.__event_data[name], inspect.stack()[1].filename, inspect.stack()[1].function, len(self.__event_data[name]))

        if not name in self.__event_data.keys():
            #print("返送", name, inspect.stack()[1].filename, inspect.stack()[1].function)
            return

        # print("実行")

        for d in self.__event_data[name]:
            if str(type(d.func)) == "<class 'function'>":

                return_val = None

                if not info is None:
                    return_val = d.func(info)

                elif info is None:
                    return_val = d.func()

                func_name = d.func.__name__
                return_val_dict[func_name] = return_val

        print(name, "実行終了")

        return return_val_dict
        # print("実行")

    def get_event(self, name, number):
        print("get_event")
        return self.__event_data[name][number].get()

    def del_event(self, name, func=None):
        if not name in list(self.__event_data.keys()):
            # print("削除返却")
            return

        # print("削除通過")

        if not func is None:

            num_flag = False
            len_event = len(self.__event_data[name])

            for num in range(len_event):

                if self.__event_data[name][num].func == func:
                    num_flag = True
                    break

            if num_flag:
                print("呼び出し先[callback_del] 削除 : ", name, num)
                del self.__event_data[name][num]
                return

        print("呼び出し先[callback_del]  : ", name)
        del self.__event_data[name]

    def all_del_event(self):
        print(" [ callback ] [ すべて削除 ] ", self.__event_data, len(self.__event_data), inspect.stack()[1].filename, inspect.stack()[1].function, " - - - - - - - - - - - - - - - -")
        self.__event_data = {}

    def all_get_event(self):
        return copy.deepcopy(self.__event_data)

        #data.set_event = set_event
        #data.event = event

        # data.set_event(data.event_not_func)
