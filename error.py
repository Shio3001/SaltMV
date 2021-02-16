import inspect


class ErrorAction:
    def __init__(self, log):
        self.log = log

    def action(self, message=None):
        func_name = inspect.stack()[1].function

        out = "error : {0} {1} ".format(func_name, message)

        self.log.write(out)

        raise ValueError(out)
