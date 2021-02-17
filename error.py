import inspect


class ErrorAction:
    def __init__(self, log):
        self.log = log
        self.log.write("error起動")

    def action(self, message=None):
        func_name = inspect.stack()[1].function

        out = "error : {0} {1} ".format(func_name, message)

        self.log.write(out)
        self.log.write("error 強制 終了")
        self.log.end()

        raise ValueError(out)
