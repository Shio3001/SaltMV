import datetime


class LogPrint:
    def __init__(self, directory):
        self.time = datetime.datetime.now()
        self.path = directory.main("../log/log_{0}.txt".format(self.time))
        self.logfile = open(self.path, mode='a')

        self.permit = True

    def write(self, *text):
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
