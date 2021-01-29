import datetime


class LogPrint:
    def __init__(self, directory):
        self.time = datetime.datetime.now()
        self.path = directory.main("../log/log_{0}.txt".format(self.time))
        self.logfile = open(self.path, mode='a')

    def write(self, *text):
        nowtime = datetime.datetime.now()

        for t in text:
            self.logfile.write("{0} : {1}\n".format(nowtime, t))
        return

    def end(self):
        self.logfile.close()
        return
