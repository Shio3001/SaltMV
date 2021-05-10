import copy


class CallBack:
    def __init__(self):
        self.__event_data = {}

    def set_event(self, name, func, run=False):
        if not name in self.__event_data.keys():
            self.__event_data[name] = []

        self.__event_data[name].append(func)  # 一度に複数の関数を実行できるようにするため

        if run:
            func(None)

    def event(self, name, info=None):

        if not name in self.__event_data.keys():
            # print("返送")
            return

        # print("実行")

        for d in self.__event_data[name]:
            if str(type(d)) == "<class 'function'>":
                d(info)
                # print("実行")

            """
            if str(type(self.__event_data[name])) == "<class 'list'>":
                for d in self.__event_data[name]:

                    if str(type(self.__event_data[name])) == "<class 'function'>":
                        d(info)

            elif str(type(self.__event_data[name])) == "<class 'function'>":
                self.__event_data[name](info)
            """

        #data.set_event = set_event
        #data.event = event

        # data.set_event(data.event_not_func)
