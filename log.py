import datetime
import inspect


class LogPrint:
    def __init__(self, directory):
        self.directory = directory
        self.time = datetime.datetime.now()
        self.path = self.directory.path_support("../log/log_{0}.txt".format(self.time))
        self.logfile = self.new_file(self.path)

        self.permit = True

    def write(self, *text):
        return
        if not self.permit:
            return  # 書き込みが許可されていない

        for t in text:
            self.logfile.write("{0} : {1}\n".format(self.get_nowtime(), t))
        return

    def end(self):
        self.logfile.close()
        return

    def stop(self, permit):
        self.permit = permit  # 書き込みを許可するか許可しないか
        self.logfile.write(" * * * {0} 書き込み許可が変更 {1} * * * \n".format(self.get_nowtime(), self.permit))
        return

    def get_nowtime(self):
        nowtime = datetime.datetime.now()
        return nowtime

    def write_func_list(self, class_data):
        return
        """
        path_func = self.directory.path_support("../log/{0}.txt".format(str(class_data)))

        logfile_func = self.new_file(path_func)
        logfile_func.write(" * * * {0} 関数表記 {1} {2} * * * \n".format(self.get_nowtime(), inspect.stack()[1].function, str(class_data)))
        for i in inspect.getmembers(class_data):
            # print(i)
            logfile_func.write(str(i))

        logfile_func.close()
        """

    def new_file(self, path):
        file = open(path, mode='a')
        return file
